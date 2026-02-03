# Simulation Overview (RT vs nonRT, preemptive priority)

This project simulates a **single server** processing two kinds of messages:

- **RT (real-time)**: higher priority
- **nonRT**: lower priority

The server uses **preemptive priority with preemptive-resume**:

- If an RT message arrives while a nonRT message is in service, the server **interrupts** the nonRT service and starts the RT service immediately.
- The interrupted nonRT message later **resumes** from its remaining service time.

## Events and clocks

The simulation is event-based. It maintains:

- **MC**: master clock (current simulated time)
- **RTCL**: time of next RT arrival
- **nonRTCL**: time of next nonRT arrival
- **SCL**: time of next service completion (or \(+\infty\) if idle)

At each step, the simulation advances **MC** to the smallest scheduled clock value.

## Server state

- `s = 0`: idle
- `s = 1`: serving RT
- `s = 2`: serving nonRT

## Queue state

- `nRT`: number of RT messages waiting in the RT queue
- `nnonRT`: number of nonRT messages waiting in the nonRT queue

## Tie-breaking

If an arrival and service completion occur at the **same time** (possible with integer clocks), the simulator processes **arrivals first**, then the service completion.

## How this maps to the code

- Core logic lives in `simulate.py` (`Simulate` class).
- Task runners:
  - `task2_1.py`: constant inter-arrival/service times (matches the hand-simulation style)
  - `task2_2.py`: exponential inter-arrival/service times (user inputs means)



