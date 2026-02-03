"""Task 2.2 runner (exponential inter-arrival and service times; user inputs means)."""

from python.simulate import Simulate


def main():
    print("=" * 100)
    print("Task 2.2: Simulation with Exponential Distributions")
    print("=" * 100)
    print()

    print("Please enter mean inter-arrival and service times:")
    mean_inter_arrival_time_RT = float(
        input("Please enter mean inter arrival time for Real time messages: ")
    )
    mean_inter_arrival_time_NRT = float(
        input("Please enter mean inter arrival time for Non-Real time messages: ")
    )
    mean_service_time_RT = float(
        input("Please enter mean service time for Real time messages: ")
    )
    mean_service_time_NRT = float(
        input("Please enter mean service time for Non-Real time messages: ")
    )

    print()
    print("=" * 100)
    print("Starting simulation with exponential distributions...")
    print("=" * 100)
    print()

    sim = Simulate(
        rt_inter_arrival=mean_inter_arrival_time_RT,
        nrt_inter_arrival=mean_inter_arrival_time_NRT,
        rt_service=mean_service_time_RT,
        nrt_service=mean_service_time_NRT,
        use_exponential=True,
        seed=None,  # Can set seed for reproducibility
    )

    sim.run(max_time=200)

    print()
    print("=" * 100)
    print("Simulation completed!")
    print("=" * 100)


if __name__ == "__main__":
    main()
