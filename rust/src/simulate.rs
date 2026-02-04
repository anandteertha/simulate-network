use rand::Rng;
use std::f64::{EPSILON, MAX};

use crate::{service_type::ServiceType, simulation_entry::Entry};

fn generate_inter_arrival_time_or_service_time(entry: &mut Entry, mean_time: f64) -> f64 {
    if entry.is_exponential {
        let random_number: f64 = rand::thread_rng().r#gen();
        return -mean_time * random_number.ln();
    }
    mean_time
}

pub fn handle_arrival_rt(entry: &mut Entry) {
    entry.mc = entry.rtcl;
    entry.rtcl =
        entry.mc + generate_inter_arrival_time_or_service_time(entry, entry.rt_inter_interval);
    entry.n_rt += 1;
    if entry.n_rt == 1 {
        match entry.s {
            ServiceType::Idle => {
                rt_completion(entry);
            }
            ServiceType::NonRealTime => {
                entry.preempted_service_time = entry.scl - entry.mc;
                entry.n_nonrt += 1;
                rt_completion(entry);
            }
            ServiceType::RealTime => {}
        }
    }
}

fn rt_completion(entry: &mut Entry) {
    entry.scl = entry.mc + generate_inter_arrival_time_or_service_time(entry, entry.rt_service);
    entry.n_rt -= 1;
    entry.s = ServiceType::RealTime;
}

pub fn handle_arrival_nrt(entry: &mut Entry) {
    entry.mc = entry.non_rtcl;
    entry.n_nonrt += 1;
    entry.non_rtcl =
        entry.mc + generate_inter_arrival_time_or_service_time(entry, entry.nrt_inter_interval);

    if entry.n_nonrt == 1 {
        if matches!(entry.s, ServiceType::Idle) {
            nrt_completion(entry, entry.nrt_service);
        }
    }
}

pub fn nrt_completion(entry: &mut Entry, service_time: f64) {
    entry.scl = entry.mc + generate_inter_arrival_time_or_service_time(entry, service_time);
    entry.n_nonrt -= 1;
    entry.s = ServiceType::NonRealTime;
}

pub fn handle_service_completion(entry: &mut Entry) {
    entry.mc = entry.scl;
    if entry.n_rt > 0 {
        rt_completion(entry);
    } else if entry.n_nonrt > 0 {
        let mut service_time: f64 = entry.nrt_service;
        if entry.preempted_service_time > 0.0 {
            service_time = entry.preempted_service_time;
        }
        nrt_completion(entry, service_time);
    } else {
        entry.s = ServiceType::Idle;
        entry.scl = MAX;
    }
}

fn log(entry: &mut Entry) {
    let preempted_str = if entry.preempted_service_time > 0.0 {
        format!("{:.2}", entry.preempted_service_time)
    } else {
        "-".to_string()
    };
    println!(
        "{:6.2} | {:8.2} | {:10.2} | {:3} | {:6} | {:8.2} | {:1} | {:<22} |",
        entry.mc,
        entry.rtcl,
        entry.non_rtcl,
        entry.n_rt,
        entry.n_nonrt,
        entry.scl,
        entry.s,
        preempted_str
    );
}

pub fn run(entry: &mut Entry, max_time: f64) {
    let table_width = 97;
    println!("{}", "=".repeat(table_width));
    println!(
        "{:>6} | {:>8} | {:>10} | {:>3} | {:>6} | {:>8} | {:<3} | {:<22} |",
        "MC", "RTCL", "nonRTCL", "nRT", "nnonRT", "SCL", "S", "preempted service time"
    );
    log(entry);
    println!("{}", "=".repeat(table_width));

    while entry.mc < max_time {
        let mut next_event_time = entry.rtcl.min(entry.non_rtcl);
        if !matches!(entry.s, ServiceType::Idle) {
            next_event_time = next_event_time.min(entry.scl);
        }
        if next_event_time > max_time {
            break;
        }
        let rt = entry.rtcl - next_event_time;
        let nrt = entry.non_rtcl - next_event_time;
        let sc = entry.scl - next_event_time;
        if rt.abs() < EPSILON {
            handle_arrival_rt(entry);
            log(entry);
        }
        if nrt.abs() < EPSILON {
            handle_arrival_nrt(entry);
            log(entry);
        }
        if sc.abs() < EPSILON && !matches!(entry.s, ServiceType::Idle) {
            handle_service_completion(entry);
            log(entry);
        }
    }
}
