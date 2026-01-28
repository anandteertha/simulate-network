"""Task 2.1 runner (constant inter-arrival and service times)."""

from simulate import Simulate


def main():
    print("=" * 100)
    print("Task 2.1: Simulation with Constant Inter-arrival and Service Times")
    print("=" * 100)
    print()
    
    rt_inter_arrival = 10
    nrt_inter_arrival = 5
    rt_service = 2
    nrt_service = 4
    
    sim = Simulate(
        rt_inter_arrival=rt_inter_arrival,
        nrt_inter_arrival=nrt_inter_arrival,
        rt_service=rt_service,
        nrt_service=nrt_service,
        use_exponential=False
    )
    
    sim.run(max_time=200)
    
    print()
    print("=" * 100)
    print("Simulation completed!")
    print("=" * 100)


if __name__ == "__main__":
    main()

