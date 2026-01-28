# IoT Analytics - Project 1: Two-Queue Simulation System

This project implements an event-based simulation of a two-queue system with Real-Time (RT) and Non-Real-Time (nonRT) message queues. The RT queue has preemptive priority over the nonRT queue.

For a short conceptual walkthrough of the scheduling policy and event clocks, see `docs/overview.md`.

## Project Structure

```
simulate-network/
├── simulate.py      # Core simulation class
├── task2_1.py      # Task 2.1: Constant inter-arrival and service times
├── task2_2.py      # Task 2.2: Exponential distributions
├── main.py         # Main entry point
└── README.md       # This file
```

## System Description

The simulation models a server that processes messages from two queues:

1. **RT Queue**: Real-time messages that require immediate processing
2. **nonRT Queue**: Non-real-time messages with lower priority

### Key Features

- **Preemptive Priority**: RT messages can interrupt nonRT message processing
- **Preemptive Resume**: When a nonRT message is interrupted, it resumes from where it stopped
- **Event-Based Simulation**: Uses discrete event simulation with event clocks

### Server States

- `s = 0`: Server is idle
- `s = 1`: Server is processing an RT message
- `s = 2`: Server is processing a nonRT message

## Requirements

- Python 3.6 or higher
- Standard library only (no external dependencies)

## Usage

### Option 1: Using the main entry point

```bash
python main.py
```

Then select:
- `1` for Task 2.1 (constant values)
- `2` for Task 2.2 (exponential distributions)

### Option 2: Running tasks directly

#### Task 2.1: Constant Inter-arrival and Service Times

```bash
python task2_1.py
```

This task reproduces the hand simulation with constant values:
- RT inter-arrival time = 10
- nonRT inter-arrival time = 5
- RT service time = 2
- nonRT service time = 4

The simulation runs until MC (Master Clock) exceeds 200.

#### Task 2.2: Exponential Distributions

```bash
python task2_2.py
```

This task uses exponential distributions for inter-arrival and service times. You will be prompted to enter:
- Mean inter-arrival time for RT messages
- Mean inter-arrival time for nonRT messages
- Mean service time for RT messages
- Mean service time for nonRT messages

The simulation runs until MC exceeds 200.

## Output Format

The simulation outputs a table with the following columns:

| Column | Description |
|--------|-------------|
| MC | Master Clock (current simulation time) |
| RTCL | RT arrival clock (next RT message arrival time) |
| nonRTCL | nonRT arrival clock (next nonRT message arrival time) |
| nRT | Number of RT messages in RT queue |
| nnonRT | Number of nonRT messages in nonRT queue |
| SCL | Service completion clock (next service completion time) |
| Server status | Current server state (idle, s=1, or s=2) |
| pre-empted service time | Remaining service time of preempted nonRT message |

## Simulation Logic

### Event Types

1. **RT Arrival**: An RT message arrives and joins the RT queue
2. **nonRT Arrival**: A nonRT message arrives and joins the nonRT queue
3. **Service Completion**: A message finishes processing

### Event Handling

1. **RT Arrival**:
   - Message joins RT queue (`nRT++`)
   - If RT queue was empty and server is idle, start processing immediately
   - If server is processing a nonRT message, preempt it and start processing RT message
   - Generate next RT arrival time

2. **nonRT Arrival**:
   - Message joins nonRT queue (`nnonRT++`)
   - If nonRT queue was empty and server is idle, start processing immediately
   - Generate next nonRT arrival time

3. **Service Completion**:
   - Check RT queue first (preemptive priority)
   - If RT queue has messages, process RT message
   - If RT queue is empty, check nonRT queue
   - If nonRT queue has messages, process nonRT message (use preempted service time if available)
   - If both queues are empty, server becomes idle

### Preemption Logic

When an RT message arrives while a nonRT message is being processed:
1. Calculate remaining service time: `remaining_time = SCL - MC`
2. Store the remaining service time
3. Return the preempted nonRT message to the top of the nonRT queue
4. Start processing the RT message immediately
5. When the preempted nonRT message is processed later, use the stored remaining service time

## Initial Conditions

The simulation starts with:
- `RTCL = 3`
- `nonRTCL = 5`
- `nRT = 0`
- `nnonRT = 0`
- `s = 2` (server processing nonRT message)
- `SCL = 4`

Note: The final results do not depend on the initial conditions.

## Exponential Distribution

For Task 2.2, exponential variates are generated using the inverse transform method:

```
x = -mean * ln(r)
```

where `r` is a uniform random number in (0, 1).

## Testing

The simulation has been tested against the hand simulation results from Task 1.1. The output matches the expected behavior for:
- Event ordering
- Queue management
- Preemption handling
- Service time calculations

## Notes

- When events occur at the same time (possible with integer clocks), arrivals are processed before service completions
- With exponential distributions (real-valued clocks), simultaneous events are extremely unlikely
- The simulation uses floating-point arithmetic for exponential distributions but maintains precision for comparisons

## Author

Implementation for CSC 591/ECE 592 IoT Analytics - Project 1

## License

This code is provided for educational purposes as part of a course project.

