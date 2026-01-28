"""
Event-based simulation of a single-server system with two queues:

- **RT** (real-time) messages: higher priority
- **nonRT** messages: lower priority

Scheduling policy:
- Preemptive priority for RT over nonRT
- Preemptive-resume for nonRT (interrupted service resumes from remaining time)

This code follows the Project 1 description (Task 1/2) for CSC 591/ECE 592.
"""

from __future__ import annotations

import math
import random
from typing import Any, Dict, List, Optional


SERVER_IDLE = 0
SERVER_RT = 1
SERVER_NONRT = 2

EPS = 1e-10


class Simulate:
    """Discrete-event simulator for the RT/nonRT two-queue server."""
    
    def __init__(
        self,
        rt_inter_arrival: float,
        nrt_inter_arrival: float,
        rt_service: float,
        nrt_service: float,
        use_exponential: bool = False,
        seed: Optional[int] = None,
    ) -> None:
        """Create a simulator.

        Parameters are interpreted as either:
        - **constant values** (when `use_exponential=False`), or
        - **means** of exponential distributions (when `use_exponential=True`).
        """
        self.rt_inter_arrival = rt_inter_arrival
        self.nrt_inter_arrival = nrt_inter_arrival
        self.rt_service = rt_service
        self.nrt_service = nrt_service
        self.use_exponential = use_exponential
        self._print_log = True
        
        if seed is not None:
            random.seed(seed)
        
        # Initial conditions (aligned with the assignment’s example tables)
        self.MC: float = 0.0
        self.RTCL: float = 3.0
        self.nonRTCL: float = 5.0
        self.SCL: float = 4.0
        self.nRT: int = 0
        self.nnonRT: int = 0
        self.s: int = SERVER_NONRT
        
        self.preempted_service_time: Optional[float] = None
        
        self.output_log: List[Dict[str, Any]] = []
    
    def generate_inter_arrival_time(self, mean_value: float) -> float:
        """Return an inter-arrival time."""
        if self.use_exponential:
            r = random.random()
            return -mean_value * math.log(r)
        return mean_value
    
    def generate_service_time(self, mean_value: float) -> float:
        """Return a service time."""
        if self.use_exponential:
            r = random.random()
            return -mean_value * math.log(r)
        return mean_value
    
    def log_state(self) -> None:
        """Append the current state to `output_log` and optionally print it."""
        preempted_str = "" if self.preempted_service_time is None else f"{self.preempted_service_time:.2f}"
        server_status_str = {SERVER_IDLE: "idle", SERVER_RT: "s=1", SERVER_NONRT: "s=2"}.get(self.s, str(self.s))

        log_entry: Dict[str, Any] = {
            "MC": self.MC,
            "RTCL": self.RTCL,
            "nonRTCL": self.nonRTCL,
            "nRT": self.nRT,
            "nnonRT": self.nnonRT,
            "SCL": self.SCL,
            "server_status": server_status_str,
            "preempted": preempted_str,
        }
        self.output_log.append(log_entry)
        
        if self._print_log:
            print(
                f"{self.MC:6.2f} | {self.RTCL:8.2f} | {self.nonRTCL:10.2f} | "
                f"{self.nRT:3} | {self.nnonRT:6} | {self.SCL:8.2f} | "
                f"{server_status_str:15} | {preempted_str:20}"
            )
    
    def handle_rt_arrival(self) -> None:
        """Process an RT arrival event and apply preemption if needed."""
        self.MC = self.RTCL
        self.nRT += 1
        iat = self.generate_inter_arrival_time(self.rt_inter_arrival)
        self.RTCL = self.MC + iat

        if self.nRT == 1:
            if self.s == SERVER_IDLE:
                st = self.generate_service_time(self.rt_service)
                self.SCL = self.MC + st
                self.nRT -= 1
                self.s = SERVER_RT
            elif self.s == SERVER_NONRT:
                remaining_time = self.SCL - self.MC
                if remaining_time > 0:
                    self.preempted_service_time = remaining_time
                    self.nnonRT += 1
                else:
                    self.preempted_service_time = None

                st = self.generate_service_time(self.rt_service)
                self.SCL = self.MC + st
                self.nRT -= 1
                self.s = SERVER_RT
    
    def handle_nrt_arrival(self) -> None:
        """Process a nonRT arrival event."""
        self.MC = self.nonRTCL
        self.nnonRT += 1
        iat = self.generate_inter_arrival_time(self.nrt_inter_arrival)
        self.nonRTCL = self.MC + iat

        if self.nnonRT == 1 and self.s == SERVER_IDLE:
            st = self.generate_service_time(self.nrt_service)
            self.SCL = self.MC + st
            self.nnonRT -= 1
            self.s = SERVER_NONRT
    
    def handle_service_completion(self) -> None:
        """Process the service-completion event and schedule the next service (if any)."""
        self.MC = self.SCL

        if self.nRT > 0:
            st = self.generate_service_time(self.rt_service)
            self.SCL = self.MC + st
            self.s = SERVER_RT
            self.nRT -= 1
        elif self.nnonRT > 0:
            if self.preempted_service_time is not None:
                st = self.preempted_service_time
                self.preempted_service_time = None
            else:
                st = self.generate_service_time(self.nrt_service)
            self.SCL = self.MC + st
            self.s = SERVER_NONRT
            self.nnonRT -= 1
        else:
            self.s = SERVER_IDLE
            self.SCL = float("inf")
    
    def run(self, max_time: float, print_log: bool = True) -> List[Dict[str, Any]]:
        """Run the simulation until the next event would exceed `max_time`."""
        self._print_log = print_log
        if self._print_log:
            print("=" * 100)
            print(
                f"{'MC':>6} | {'RTCL':>8} | {'nonRTCL':>10} | {'nRT':>3} | {'nnonRT':>6} | "
                f"{'SCL':>8} | {'Server status':>15} | {'pre-empted service time':>20}"
            )
            print("=" * 100)

        self.log_state()

        while self.MC < max_time:
            next_event_time = min(self.RTCL, self.nonRTCL)
            if self.s != SERVER_IDLE:
                next_event_time = min(next_event_time, self.SCL)

            if next_event_time > max_time:
                break

            rt_due = abs(self.RTCL - next_event_time) < EPS
            nrt_due = abs(self.nonRTCL - next_event_time) < EPS
            svc_due = self.s != SERVER_IDLE and abs(self.SCL - next_event_time) < EPS

            # If clocks tie (possible with integer clocks), process arrivals before completion.
            if rt_due:
                self.handle_rt_arrival()
                self.log_state()
            if nrt_due:
                self.handle_nrt_arrival()
                self.log_state()
            if svc_due:
                self.handle_service_completion()
                self.log_state()
        
        return self.output_log
