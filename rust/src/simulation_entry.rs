use crate::service_type::ServiceType;

#[derive(Debug)]
pub struct Entry {
    pub rt_inter_interval: f64,
    pub nrt_inter_interval: f64,
    pub rt_service: f64,
    pub nrt_service: f64,
    pub mc: f64,
    pub rtcl: f64,
    pub non_rtcl: f64,
    pub scl: f64,
    pub n_rt: i64,
    pub n_nonrt: i64,
    pub s: ServiceType,
    pub preempted_service_time: f64,
    pub is_exponential: bool,
}
