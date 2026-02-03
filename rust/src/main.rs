use crate::{simulate::run, simulation_entry::Entry};

pub mod service_type;
pub mod simulate;
pub mod simulation_entry;
fn main() {
    task_2_1();
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
    };
    run(&mut entry, 200.0);
    println!();
    println!("{}", "=".repeat(100));
    println!("Simulation completed!");
    println!("{}", "=".repeat(100));
}
