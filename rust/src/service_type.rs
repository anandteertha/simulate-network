#[derive(Debug)]
pub enum ServiceType {
    RealTime,
    NonRealTime,
    Idle,
}

impl std::fmt::Display for ServiceType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let matched_service = match self {
            ServiceType::RealTime => "1",
            ServiceType::NonRealTime => "2",
            ServiceType::Idle => "Idle",
        };
        write!(f, "{}", matched_service)
    }
}
