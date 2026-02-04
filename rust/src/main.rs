use crate::{simulate::run, simulation_entry::Entry};
use std::io::stdin;
pub mod service_type;
pub mod simulate;
pub mod simulation_entry;
fn main() {
    task_2_1();
    task_2_2();
}

fn task_2_1() {
    println!("{}", "=".repeat(100));
    println!("Task 2.1: Simulation with Constant Inter-arrival and Service Times");
    println!("{}", "=".repeat(100));
    let mut entry: Entry = Entry {
        rt_inter_interval: 10.0,
        nrt_inter_interval: 5.0,
        rt_service: 2.0,
        nrt_service: 4.0,
        mc: 0.0,
        rtcl: 0.0,
        non_rtcl: 0.0,
        scl: 0.0,
        n_rt: 0,
        n_nonrt: 0,
        s: service_type::ServiceType::Idle,
        preempted_service_time: 0.0,
        is_exponential: false,
    };
    run(&mut entry, 200.0);
    println!();
    println!("{}", "=".repeat(100));
    println!("Simulation completed!");
    println!("{}", "=".repeat(100));
}

fn get_input(s: &str) -> String {
    println!("{}", s);
    let mut mean_inter_arrival_time_rt = String::new();
    stdin()
        .read_line(&mut mean_inter_arrival_time_rt)
        .expect("Failed to read line");
    mean_inter_arrival_time_rt
}

fn task_2_2() {
    println!("{}", "=".repeat(100));
    println!("Task 2.2: Simulation with Exponential Distributions");
    println!("{}", "=".repeat(100));
    println!("Please enter mean inter-arrival and service times:");
    let mean_inter_arrival_time_rt: f64 = loop {
        let value = get_input("Please enter mean inter-arrival RT time:");
        match value.trim().parse() {
            Ok(num) => break num,
            Err(_) => {
                println!("Invalid input. Please enter a valid floating-point number:");
                continue;
            }
        }
    };

    let mean_inter_arrival_time_nrt: f64 = loop {
        let value = get_input("Please enter mean inter-arrival NRT time:");
        match value.trim().parse() {
            Ok(num) => break num,
            Err(_) => {
                println!("Invalid input. Please enter a valid floating-point number:");
                continue;
            }
        }
    };

    let mean_service_time_rt: f64 = loop {
        let value = get_input("Please enter mean service RT time:");
        match value.trim().parse() {
            Ok(num) => break num,
            Err(_) => {
                println!("Invalid input. Please enter a valid floating-point number:");
                continue;
            }
        }
    };

    let mean_service_time_nrt: f64 = loop {
        let value = get_input("Please enter mean service NRT time:");
        match value.trim().parse() {
            Ok(num) => break num,
            Err(_) => {
                println!("Invalid input. Please enter a valid floating-point number:");
                continue;
            }
        }
    };

    println!();
    println!("{}", "=".repeat(100));
    println!("Starting simulation with exponential distributions...");
    println!("{}", "=".repeat(100));
    println!();

    let mut entry: Entry = Entry {
        rt_inter_interval: mean_inter_arrival_time_rt,
        nrt_inter_interval: mean_inter_arrival_time_nrt,
        rt_service: mean_service_time_rt,
        nrt_service: mean_service_time_nrt,
        mc: 0.0,
        rtcl: 0.0,
        non_rtcl: 0.0,
        scl: 0.0,
        n_rt: 0,
        n_nonrt: 0,
        s: service_type::ServiceType::Idle,
        preempted_service_time: 0.0,
        is_exponential: true,
    };
    run(&mut entry, 200.0);
    println!();
    println!("{}", "=".repeat(100));
    println!("Simulation completed!");
    println!("{}", "=".repeat(100));
}
