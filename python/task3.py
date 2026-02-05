import matplotlib.pyplot as plt
import numpy as np

from batch_means import calculate_statistics_with_ci
from simulate_task3 import SimulateTask3


def run_single_simulation(
    rt_inter_arrival: float,
    nrt_inter_arrival: float,
    rt_service: float,
    nrt_service: float,
    num_batches: int,
    batch_size: int,
    seed: int = None,
) -> tuple[dict, dict]:
    sim = SimulateTask3(
        rt_inter_arrival=rt_inter_arrival,
        nrt_inter_arrival=nrt_inter_arrival,
        rt_service=rt_service,
        nrt_service=nrt_service,
        use_exponential=True,
        seed=seed,
    )

    total_messages = num_batches * batch_size
    sim.run_until_messages(total_messages, total_messages)

    rt_stats = calculate_statistics_with_ci(
        sim.rt_response_times, num_batches, batch_size
    )
    nrt_stats = calculate_statistics_with_ci(
        sim.nrt_response_times, num_batches, batch_size
    )

    return rt_stats, nrt_stats


def task_3_1():
    print("=" * 100)
    print("Task 3.1: Statistical Estimation of Response Time")
    print("=" * 100)
    print()

    print("Please enter simulation parameters:")
    miat_rt = float(input("Mean inter-arrival time of RT messages (MIAT_RT): "))
    miat_nrt_start = float(
        input("Starting mean inter-arrival time of nonRT messages (MIAT_nonRT): ")
    )
    miat_nrt_end = float(
        input("Ending mean inter-arrival time of nonRT messages (MIAT_nonRT): ")
    )
    miat_nrt_step = float(input("Step size for MIAT_nonRT: "))
    mst_rt = float(input("Mean service time of RT messages (MST_RT): "))
    mst_nrt = float(input("Mean service time of nonRT messages (MST_nonRT): "))
    num_batches = int(input("Number of batches (m): "))
    batch_size = int(input("Batch size (b): "))

    print()
    print("=" * 100)
    print("Running simulations...")
    print("=" * 100)
    print()

    miat_nrt_values = np.arange(
        miat_nrt_start, miat_nrt_end + miat_nrt_step, miat_nrt_step
    )
    miat_nrt_values = [round(x, 1) for x in miat_nrt_values]

    results = []

    for miat_nrt in miat_nrt_values:
        print(f"Running simulation for MIAT_nonRT = {miat_nrt}...")
        rt_stats, nrt_stats = run_single_simulation(
            rt_inter_arrival=miat_rt,
            nrt_inter_arrival=miat_nrt,
            rt_service=mst_rt,
            nrt_service=mst_nrt,
            num_batches=num_batches,
            batch_size=batch_size,
        )

        results.append(
            {
                "miat_nrt": miat_nrt,
                "lambda_nrt_inv": 1.0 / miat_nrt,
                "rt_stats": rt_stats,
                "nrt_stats": nrt_stats,
            }
        )

        print(
            f"  RT Mean: {rt_stats['mean']:.4f} "
            f"[{rt_stats['mean_ci_lower']:.4f}, {rt_stats['mean_ci_upper']:.4f}]"
        )
        print(
            f"  RT 95th percentile: {rt_stats['percentile_95']:.4f} "
            f"[{rt_stats['percentile_95_ci_lower']:.4f}, "
            f"{rt_stats['percentile_95_ci_upper']:.4f}]"
        )
        print(
            f"  NonRT Mean: {nrt_stats['mean']:.4f} "
            f"[{nrt_stats['mean_ci_lower']:.4f}, {nrt_stats['mean_ci_upper']:.4f}]"
        )
        print(
            f"  NonRT 95th percentile: {nrt_stats['percentile_95']:.4f} "
            f"[{nrt_stats['percentile_95_ci_lower']:.4f}, "
            f"{nrt_stats['percentile_95_ci_upper']:.4f}]"
        )
        print()

    return results


def plot_results(results: list, output_file: str = "task3_results.png"):
    lambda_nrt_inv = [r["lambda_nrt_inv"] for r in results]

    rt_means = [r["rt_stats"]["mean"] for r in results]
    rt_mean_ci_lower = [r["rt_stats"]["mean_ci_lower"] for r in results]
    rt_mean_ci_upper = [r["rt_stats"]["mean_ci_upper"] for r in results]

    nrt_means = [r["nrt_stats"]["mean"] for r in results]
    nrt_mean_ci_lower = [r["nrt_stats"]["mean_ci_lower"] for r in results]
    nrt_mean_ci_upper = [r["nrt_stats"]["mean_ci_upper"] for r in results]

    rt_percentiles = [r["rt_stats"]["percentile_95"] for r in results]
    rt_perc_ci_lower = [r["rt_stats"]["percentile_95_ci_lower"] for r in results]
    rt_perc_ci_upper = [r["rt_stats"]["percentile_95_ci_upper"] for r in results]

    nrt_percentiles = [r["nrt_stats"]["percentile_95"] for r in results]
    nrt_perc_ci_lower = [r["nrt_stats"]["percentile_95_ci_lower"] for r in results]
    nrt_perc_ci_upper = [r["nrt_stats"]["percentile_95_ci_upper"] for r in results]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Task 3: Response Time Statistics", fontsize=16, fontweight="bold")

    ax1 = axes[0, 0]
    ax1.errorbar(
        lambda_nrt_inv,
        rt_means,
        yerr=[
            [m - l for m, l in zip(rt_means, rt_mean_ci_lower)],
            [u - m for u, m in zip(rt_mean_ci_upper, rt_means)],
        ],
        fmt="o-",
        capsize=5,
        label="RT Mean",
        color="blue",
    )
    ax1.set_xlabel("1/λ_nonRT")
    ax1.set_ylabel("Mean Response Time")
    ax1.set_title("Mean Response Time - RT Messages")
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    ax2 = axes[0, 1]
    ax2.errorbar(
        lambda_nrt_inv,
        nrt_means,
        yerr=[
            [m - l for m, l in zip(nrt_means, nrt_mean_ci_lower)],
            [u - m for u, m in zip(nrt_mean_ci_upper, nrt_means)],
        ],
        fmt="s-",
        capsize=5,
        label="NonRT Mean",
        color="red",
    )
    ax2.set_xlabel("1/λ_nonRT")
    ax2.set_ylabel("Mean Response Time")
    ax2.set_title("Mean Response Time - NonRT Messages")
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    ax3 = axes[1, 0]
    ax3.errorbar(
        lambda_nrt_inv,
        rt_percentiles,
        yerr=[
            [p - l for p, l in zip(rt_percentiles, rt_perc_ci_lower)],
            [u - p for u, p in zip(rt_perc_ci_upper, rt_percentiles)],
        ],
        fmt="o-",
        capsize=5,
        label="RT 95th Percentile",
        color="blue",
    )
    ax3.set_xlabel("1/λ_nonRT")
    ax3.set_ylabel("95th Percentile Response Time")
    ax3.set_title("95th Percentile Response Time - RT Messages")
    ax3.grid(True, alpha=0.3)
    ax3.legend()

    ax4 = axes[1, 1]
    ax4.errorbar(
        lambda_nrt_inv,
        nrt_percentiles,
        yerr=[
            [p - l for p, l in zip(nrt_percentiles, nrt_perc_ci_lower)],
            [u - p for u, p in zip(nrt_perc_ci_upper, nrt_percentiles)],
        ],
        fmt="s-",
        capsize=5,
        label="NonRT 95th Percentile",
        color="red",
    )
    ax4.set_xlabel("1/λ_nonRT")
    ax4.set_ylabel("95th Percentile Response Time")
    ax4.set_title("95th Percentile Response Time - NonRT Messages")
    ax4.grid(True, alpha=0.3)
    ax4.legend()

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"Results saved to {output_file}")
    plt.close()


def print_results_summary(results: list):
    print("=" * 100)
    print("Results Summary")
    print("=" * 100)
    print()
    print(
        f"{'MIAT_nonRT':<12} {'1/λ_nonRT':<12} "
        f"{'RT Mean':<15} {'RT 95th %':<15} "
        f"{'NonRT Mean':<15} {'NonRT 95th %':<15}"
    )
    print("-" * 100)

    for r in results:
        print(
            f"{r['miat_nrt']:<12.1f} {r['lambda_nrt_inv']:<12.4f} "
            f"{r['rt_stats']['mean']:<15.4f} {r['rt_stats']['percentile_95']:<15.4f} "
            f"{r['nrt_stats']['mean']:<15.4f} {r['nrt_stats']['percentile_95']:<15.4f}"
        )

    print()


def main():
    results = task_3_1()

    print_results_summary(results)

    plot_results(results, "P1T3-Results.png")

    print("=" * 100)
    print("Task 3.2: Running with Assignment Default Parameters")
    print("=" * 100)
    print()
    print("Parameters: MST_RT=2, MST_nonRT=4, MIAT_RT=7")
    print("Varying MIAT_nonRT from 10 to 40 in increments of 5")
    print()

    assignment_results = []
    mst_rt = 2.0
    mst_nrt = 4.0
    miat_rt = 7.0
    num_batches = 51
    batch_size = 1000

    for miat_nrt in range(10, 45, 5):
        print(f"Running simulation for MIAT_nonRT = {miat_nrt}...")
        rt_stats, nrt_stats = run_single_simulation(
            rt_inter_arrival=miat_rt,
            nrt_inter_arrival=float(miat_nrt),
            rt_service=mst_rt,
            nrt_service=mst_nrt,
            num_batches=num_batches,
            batch_size=batch_size,
        )

        assignment_results.append(
            {
                "miat_nrt": float(miat_nrt),
                "lambda_nrt_inv": 1.0 / miat_nrt,
                "rt_stats": rt_stats,
                "nrt_stats": nrt_stats,
            }
        )

        print(
            f"  RT Mean: {rt_stats['mean']:.4f} "
            f"[{rt_stats['mean_ci_lower']:.4f}, {rt_stats['mean_ci_upper']:.4f}]"
        )
        print(
            f"  RT 95th percentile: {rt_stats['percentile_95']:.4f} "
            f"[{rt_stats['percentile_95_ci_lower']:.4f}, "
            f"{rt_stats['percentile_95_ci_upper']:.4f}]"
        )
        print(
            f"  NonRT Mean: {nrt_stats['mean']:.4f} "
            f"[{nrt_stats['mean_ci_lower']:.4f}, {nrt_stats['mean_ci_upper']:.4f}]"
        )
        print(
            f"  NonRT 95th percentile: {nrt_stats['percentile_95']:.4f} "
            f"[{nrt_stats['percentile_95_ci_lower']:.4f}, "
            f"{nrt_stats['percentile_95_ci_upper']:.4f}]"
        )
        print()

    print_results_summary(assignment_results)
    plot_results(assignment_results, "P1T3-Results-assignment.png")

    print("=" * 100)
    print("Analysis and Comments")
    print("=" * 100)
    print()
    print("Task 3.1 Results Analysis:")
    print("-" * 100)
    print(
        "As 1/λ_nonRT increases (i.e., MIAT_nonRT increases), the nonRT arrival rate decreases."
    )
    print("This means fewer nonRT messages compete for server resources, leading to:")
    print("1. Lower mean response time for nonRT messages (less queueing)")
    print("2. Lower 95th percentile for nonRT messages")
    print(
        "3. Potentially lower response times for RT messages as well, since there's less"
    )
    print("   preemption and interference from nonRT messages")
    print()
    print(
        "The confidence intervals show the uncertainty in our estimates. Wider intervals"
    )
    print("indicate higher variance in the response times, which could be due to:")
    print("- High variability in inter-arrival times (exponential distribution)")
    print("- High variability in service times")
    print("- System approaching saturation")
    print()
    print("Task 3.2 Results Analysis:")
    print("-" * 100)
    print("With fixed MST_RT=2, MST_nonRT=4, and MIAT_RT=7, and varying MIAT_nonRT:")
    print()
    print("RT Messages: RT messages have priority and can preempt nonRT messages.")
    print("Their response time is primarily affected by:")
    print("- Their own arrival rate (fixed at MIAT_RT=7)")
    print("- Service time (fixed at MST_RT=2)")
    print("- Interference from nonRT messages (decreases as MIAT_nonRT increases)")
    print()
    print("NonRT Messages: NonRT messages experience:")
    print("- Direct impact from their own arrival rate (MIAT_nonRT)")
    print("- Preemption by RT messages")
    print("- As MIAT_nonRT increases, fewer nonRT messages arrive, reducing both")
    print("  queue length and preemption frequency")
    print()
    print("Expected Trends:")
    print("1. NonRT mean and 95th percentile should decrease as 1/λ_nonRT increases")
    print(
        "2. RT response times may show slight improvement as nonRT interference decreases"
    )
    print(
        "3. Confidence intervals should be relatively stable if batch size is adequate"
    )
    print()
    print("=" * 100)
    print("Task 3 completed!")
    print("=" * 100)


if __name__ == "__main__":
    main()
