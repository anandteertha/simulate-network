from __future__ import annotations
import math
import random
from collections import deque
from typing import List, Optional


SERVER_IDLE = 0
SERVER_RT = 1
SERVER_NONRT = 2

EPS = 1e-10


class SimulateTask3:
    def __init__(
        self,
        rt_inter_arrival: float,
        nrt_inter_arrival: float,
        rt_service: float,
        nrt_service: float,
        use_exponential: bool = True,
        seed: Optional[int] = None,
    ) -> None:
        self.rt_inter_arrival = rt_inter_arrival
        self.nrt_inter_arrival = nrt_inter_arrival
        self.rt_service = rt_service
        self.nrt_service = nrt_service
        self.use_exponential = use_exponential

        if seed is not None:
            random.seed(seed)

        self.MC: float = 0.0
        self.SCL: float = float("inf")
        self.s: int = SERVER_IDLE

        self.rt_queue: deque[tuple[float, int]] = deque()
        self.nrt_queue: deque[tuple[float, int]] = deque()

        self.rt_response_times: List[float] = []
        self.nrt_response_times: List[float] = []

        self.rt_message_id = 0
        self.nrt_message_id = 0

        self.preempted_service_time: Optional[float] = None

        iat_rt = self.generate_inter_arrival_time(self.rt_inter_arrival)
        iat_nrt = self.generate_inter_arrival_time(self.nrt_inter_arrival)
        self.RTCL = iat_rt
        self.nonRTCL = iat_nrt

    def generate_inter_arrival_time(self, mean_value: float) -> float:
        if self.use_exponential:
            r = random.random()
            return -mean_value * math.log(r)
        return mean_value

    def generate_service_time(self, mean_value: float) -> float:
        if self.use_exponential:
            r = random.random()
            return -mean_value * math.log(r)
        return mean_value

    def handle_rt_arrival(self) -> None:
        self.MC = self.RTCL
        arrival_time = self.MC

        self.rt_queue.append((arrival_time, self.rt_message_id))
        self.rt_message_id += 1

        iat = self.generate_inter_arrival_time(self.rt_inter_arrival)
        self.RTCL = self.MC + iat

        if len(self.rt_queue) == 1:
            if self.s == SERVER_IDLE:
                st = self.generate_service_time(self.rt_service)
                self.SCL = self.MC + st
                self.s = SERVER_RT
            elif self.s == SERVER_NONRT:
                remaining_time = self.SCL - self.MC
                if remaining_time > EPS:
                    self.preempted_service_time = remaining_time
                else:
                    self.preempted_service_time = None

                st = self.generate_service_time(self.rt_service)
                self.SCL = self.MC + st
                self.s = SERVER_RT

    def handle_nrt_arrival(self) -> None:
        self.MC = self.nonRTCL
        arrival_time = self.MC

        self.nrt_queue.append((arrival_time, self.nrt_message_id))
        self.nrt_message_id += 1

        iat = self.generate_inter_arrival_time(self.nrt_inter_arrival)
        self.nonRTCL = self.MC + iat

        if len(self.nrt_queue) == 1 and self.s == SERVER_IDLE:
            st = self.generate_service_time(self.nrt_service)
            self.SCL = self.MC + st
            self.s = SERVER_NONRT

    def handle_service_completion(self) -> None:
        self.MC = self.SCL

        if self.s == SERVER_RT:
            if self.rt_queue:
                arrival_time, _ = self.rt_queue.popleft()
                response_time = self.MC - arrival_time
                self.rt_response_times.append(response_time)

            if self.rt_queue:
                st = self.generate_service_time(self.rt_service)
                self.SCL = self.MC + st
                self.s = SERVER_RT
            elif self.nrt_queue:
                if self.preempted_service_time is not None:
                    st = self.preempted_service_time
                    self.preempted_service_time = None
                else:
                    st = self.generate_service_time(self.nrt_service)
                self.SCL = self.MC + st
                self.s = SERVER_NONRT
            else:
                self.s = SERVER_IDLE
                self.SCL = float("inf")

        elif self.s == SERVER_NONRT:
            if self.nrt_queue:
                arrival_time, _ = self.nrt_queue.popleft()
                response_time = self.MC - arrival_time
                self.nrt_response_times.append(response_time)

            if self.rt_queue:
                st = self.generate_service_time(self.rt_service)
                self.SCL = self.MC + st
                self.s = SERVER_RT
            elif self.nrt_queue:
                if self.preempted_service_time is not None:
                    st = self.preempted_service_time
                    self.preempted_service_time = None
                else:
                    st = self.generate_service_time(self.nrt_service)
                self.SCL = self.MC + st
                self.s = SERVER_NONRT
            else:
                self.s = SERVER_IDLE
                self.SCL = float("inf")

    def run_until_messages(self, num_rt_messages: int, num_nrt_messages: int) -> None:
        self.rt_response_times.clear()
        self.nrt_response_times.clear()

        max_iterations = 10_000_000
        iteration = 0

        while (
            len(self.rt_response_times) < num_rt_messages
            or len(self.nrt_response_times) < num_nrt_messages
        ):
            iteration += 1
            if iteration > max_iterations:
                raise RuntimeError(
                    f"Simulation exceeded {max_iterations} iterations. "
                    f"Collected {len(self.rt_response_times)} RT and "
                    f"{len(self.nrt_response_times)} nonRT messages."
                )

            next_event_time = min(self.RTCL, self.nonRTCL)
            if self.s != SERVER_IDLE and self.SCL != float("inf"):
                next_event_time = min(next_event_time, self.SCL)

            if next_event_time == float("inf"):
                raise RuntimeError("No events scheduled - simulation cannot proceed")

            rt_due = abs(self.RTCL - next_event_time) < EPS
            nrt_due = abs(self.nonRTCL - next_event_time) < EPS
            svc_due = (
                self.s != SERVER_IDLE
                and self.SCL != float("inf")
                and abs(self.SCL - next_event_time) < EPS
            )

            if rt_due:
                self.handle_rt_arrival()
            if nrt_due:
                self.handle_nrt_arrival()
            if svc_due:
                self.handle_service_completion()

            if (
                len(self.rt_response_times) >= num_rt_messages
                and len(self.nrt_response_times) >= num_nrt_messages
            ):
                break

        if len(self.rt_response_times) > num_rt_messages:
            self.rt_response_times = self.rt_response_times[:num_rt_messages]
        if len(self.nrt_response_times) > num_nrt_messages:
            self.nrt_response_times = self.nrt_response_times[:num_nrt_messages]
