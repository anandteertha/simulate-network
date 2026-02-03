#[derive(Debug)]
pub enum ServiceType {
    RealTime,
    NonRealTime,
    Idle,
}

impl std::fmt::Display for ServiceType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let matched_service = match self {
            ServiceType::RealTime => "s=1",
            ServiceType::NonRealTime => "s=2",
            ServiceType::Idle => "s=0",
        };
        write!(f, "{}", matched_service)
    }
}
