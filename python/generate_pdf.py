import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
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


def generate_pdf(unity_id: str = "arrao6"):
    pdf_filename = f"P1T3-Results-{unity_id}.pdf"
    
    mst_rt = 2.0
    mst_nrt = 4.0
    miat_rt = 7.0
    num_batches = 51
    batch_size = 1000

    print("Running simulations for PDF generation...")
    results = []
    
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

        results.append(
            {
                "miat_nrt": float(miat_nrt),
                "lambda_nrt_inv": 1.0 / miat_nrt,
                "rt_stats": rt_stats,
                "nrt_stats": nrt_stats,
            }
        )

    print("Generating PDF...")
    
    with PdfPages(pdf_filename) as pdf:
        fig = plt.figure(figsize=(11, 8.5))
        fig.text(0.5, 0.95, "Task 3: Statistical Estimation of Response Time", 
                ha='center', va='top', fontsize=16, fontweight='bold')
        fig.text(0.5, 0.92, f"Unity ID: {unity_id}", 
                ha='center', va='top', fontsize=12)
        fig.text(0.5, 0.89, "Parameters: MST_RT=2, MST_nonRT=4, MIAT_RT=7", 
                ha='center', va='top', fontsize=10)
        fig.text(0.5, 0.86, "Varying MIAT_nonRT from 10 to 40 in increments of 5", 
                ha='center', fontsize=10)
        fig.text(0.5, 0.83, f"Batch Means Method: m={num_batches} batches, b={batch_size} observations per batch", 
                ha='center', fontsize=10)
        fig.text(0.5, 0.80, "First batch ignored, using remaining 50 batches for statistics", 
                ha='center', fontsize=10)
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        fig, axes = plt.subplots(2, 2, figsize=(11, 8.5))
        fig.suptitle("Response Time Statistics", fontsize=14, fontweight="bold")

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
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        fig = plt.figure(figsize=(11, 8.5))
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        y_pos = 0.95
        line_height = 0.04
        
        ax.text(0.1, y_pos, "Results Summary Table", fontsize=14, fontweight='bold', transform=ax.transAxes)
        y_pos -= line_height * 2
        
        header = f"{'MIAT_nonRT':<12} {'1/λ_nonRT':<12} {'RT Mean':<18} {'RT 95th %':<18} {'NonRT Mean':<18} {'NonRT 95th %':<18}"
        ax.text(0.1, y_pos, header, fontsize=9, fontweight='bold', family='monospace', transform=ax.transAxes)
        y_pos -= line_height
        
        for r in results:
            line = (f"{r['miat_nrt']:<12.1f} {r['lambda_nrt_inv']:<12.4f} "
                   f"{r['rt_stats']['mean']:<18.4f} {r['rt_stats']['percentile_95']:<18.4f} "
                   f"{r['nrt_stats']['mean']:<18.4f} {r['nrt_stats']['percentile_95']:<18.4f}")
            ax.text(0.1, y_pos, line, fontsize=9, family='monospace', transform=ax.transAxes)
            y_pos -= line_height
        
        y_pos -= line_height * 2
        ax.text(0.1, y_pos, "Confidence Intervals (95%)", fontsize=12, fontweight='bold', transform=ax.transAxes)
        y_pos -= line_height * 2
        
        for r in results:
            rt_ci = f"[{r['rt_stats']['mean_ci_lower']:.4f}, {r['rt_stats']['mean_ci_upper']:.4f}]"
            nrt_ci = f"[{r['nrt_stats']['mean_ci_lower']:.4f}, {r['nrt_stats']['mean_ci_upper']:.4f}]"
            rt_pci = f"[{r['rt_stats']['percentile_95_ci_lower']:.4f}, {r['rt_stats']['percentile_95_ci_upper']:.4f}]"
            nrt_pci = f"[{r['nrt_stats']['percentile_95_ci_lower']:.4f}, {r['nrt_stats']['percentile_95_ci_upper']:.4f}]"
            
            ax.text(0.1, y_pos, f"MIAT_nonRT = {r['miat_nrt']:.1f}:", fontsize=10, fontweight='bold', transform=ax.transAxes)
            y_pos -= line_height
            ax.text(0.15, y_pos, f"RT Mean CI: {rt_ci}", fontsize=9, transform=ax.transAxes)
            y_pos -= line_height
            ax.text(0.15, y_pos, f"RT 95th % CI: {rt_pci}", fontsize=9, transform=ax.transAxes)
            y_pos -= line_height
            ax.text(0.15, y_pos, f"NonRT Mean CI: {nrt_ci}", fontsize=9, transform=ax.transAxes)
            y_pos -= line_height
            ax.text(0.15, y_pos, f"NonRT 95th % CI: {nrt_pci}", fontsize=9, transform=ax.transAxes)
            y_pos -= line_height * 2
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        fig = plt.figure(figsize=(11, 8.5))
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        y_pos = 0.95
        line_height = 0.025
        
        ax.text(0.1, y_pos, "Analysis and Comments", fontsize=14, fontweight='bold', transform=ax.transAxes)
        y_pos -= line_height * 2
        
        analysis_text = [
            "Task 3.1 Results Analysis:",
            "",
            "As 1/λ_nonRT increases (i.e., MIAT_nonRT increases), the nonRT arrival rate decreases.",
            "This means fewer nonRT messages compete for server resources, leading to:",
            "1. Lower mean response time for nonRT messages (less queueing)",
            "2. Lower 95th percentile for nonRT messages",
            "3. Potentially lower response times for RT messages as well, since there's less",
            "   preemption and interference from nonRT messages",
            "",
            "The confidence intervals show the uncertainty in our estimates. Wider intervals",
            "indicate higher variance in the response times, which could be due to:",
            "- High variability in inter-arrival times (exponential distribution)",
            "- High variability in service times",
            "- System approaching saturation",
            "",
            "Task 3.2 Results Analysis:",
            "",
            "With fixed MST_RT=2, MST_nonRT=4, and MIAT_RT=7, and varying MIAT_nonRT:",
            "",
            "RT Messages: RT messages have priority and can preempt nonRT messages.",
            "Their response time is primarily affected by:",
            "- Their own arrival rate (fixed at MIAT_RT=7)",
            "- Service time (fixed at MST_RT=2)",
            "- Interference from nonRT messages (decreases as MIAT_nonRT increases)",
            "",
            "NonRT Messages: NonRT messages experience:",
            "- Direct impact from their own arrival rate (MIAT_nonRT)",
            "- Preemption by RT messages",
            "- As MIAT_nonRT increases, fewer nonRT messages arrive, reducing both",
            "  queue length and preemption frequency",
            "",
            "Expected Trends:",
            "1. NonRT mean and 95th percentile should decrease as 1/λ_nonRT increases",
            "2. RT response times may show slight improvement as nonRT interference decreases",
            "3. Confidence intervals should be relatively stable if batch size is adequate",
        ]
        
        for line in analysis_text:
            ax.text(0.1, y_pos, line, fontsize=9, transform=ax.transAxes, wrap=True)
            y_pos -= line_height
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    print(f"PDF generated successfully: {pdf_filename}")


if __name__ == "__main__":
    generate_pdf("arrao6")

