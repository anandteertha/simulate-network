# Task 3: Statistical Estimation of Response Time

## Overview

This task implements statistical analysis of response times for RT and nonRT messages using the batch means method. The simulation tracks response times for each message and calculates mean, 95th percentile, and confidence intervals.

## Design

### File Structure

- **`simulate_task3.py`**: Core simulation class with queue-based message tracking
- **`batch_means.py`**: Statistical analysis functions using batch means method
- **`task3.py`**: Main script that runs simulations and generates results
- **`generate_pdf.py`**: Script to generate the PDF report

### Key Design Decisions

1. **Queue-based tracking**: Each message is stored in a queue with its arrival time. When service completes, response time is calculated as `completion_time - arrival_time`.

2. **Batch means method**: 
   - Divides response times into m batches of size b
   - Calculates batch mean and batch 95th percentile for each batch
   - Ignores first batch (warm-up period)
   - Uses remaining batches to calculate overall statistics and confidence intervals

3. **Preemption handling**: When RT message preempts nonRT service, the remaining service time is stored and used when the nonRT message resumes.

4. **Exponential distributions**: All inter-arrival and service times use exponential distributions (as required for Task 3).

## How to Run

### Prerequisites

Install required packages:
```bash
pip install -r requirements.txt
```

### Running Task 3.1 (Interactive)

Run the main script and enter parameters when prompted:
```bash
python task3.py
```

You will be asked for:
- Mean inter-arrival time of RT messages (MIAT_RT)
- Starting/ending mean inter-arrival time of nonRT messages (MIAT_nonRT)
- Step size for MIAT_nonRT
- Mean service times (MST_RT, MST_nonRT)
- Number of batches (m)
- Batch size (b)

The script will:
1. Run simulations for each MIAT_nonRT value
2. Display results with confidence intervals
3. Generate plots (P1T3-Results.png)
4. Run Task 3.2 with assignment default parameters

### Running Task 3.2 Only (Assignment Parameters)

To generate the PDF with assignment default parameters:
```bash
python generate_pdf.py
```

This will:
- Run simulations with MST_RT=2, MST_nonRT=4, MIAT_RT=7
- Vary MIAT_nonRT from 10 to 40 in increments of 5
- Use m=51 batches, b=1000 observations per batch
- Generate `P1T3-Results-arrao6.pdf`

### Output Files

- **P1T3-Results.png**: Plots from Task 3.1 (if run interactively)
- **P1T3-Results-assignment.png**: Plots from Task 3.2
- **P1T3-Results-arrao6.pdf**: Complete PDF report with all results

## Parameters

### Assignment Default Parameters (Task 3.2)

- MST_RT = 2.0
- MST_nonRT = 4.0
- MIAT_RT = 7.0
- MIAT_nonRT: 10, 15, 20, 25, 30, 35, 40
- m = 51 batches
- b = 1000 observations per batch
- First batch ignored, using batches 1-50 for statistics

## Statistics Calculated

For each message type (RT and nonRT):

1. **Mean response time**: Average of batch means (excluding first batch)
2. **95th percentile**: Average of batch 95th percentiles (excluding first batch)
3. **95% Confidence intervals**: Calculated using t-distribution with (n-1) degrees of freedom, where n is the number of batches used (50)

## Notes

- The simulation uses exponential distributions for all random variates
- Response time is measured from arrival to service completion
- Preempted nonRT messages resume with their remaining service time
- The batch means method helps account for correlation in the data

