"""
Main entry point for the simulation project.

This file provides a simple interface to run either Task 2.1 or Task 2.2.
"""

import sys


def main():
    print("=" * 100)
    print("IoT Analytics - Project 1 - Simulation")
    print("=" * 100)
    print()
    print("Select which task to run:")
    print("1. Task 2.1 - Constant inter-arrival and service times")
    print("2. Task 2.2 - Exponential distributions")
    print()

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        from python.task2_1 import main as task2_1_main

        task2_1_main()
    elif choice == "2":
        from python.task2_2 import main as task2_2_main

        task2_2_main()
    else:
        print("Invalid choice. Please run the program again and select 1 or 2.")
        sys.exit(1)


if __name__ == "__main__":
    main()
