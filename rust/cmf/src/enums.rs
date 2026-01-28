use base::errors::ClientError;


#[derive(Clone, Copy, PartialEq, Eq)]
pub enum CmfResponseFormat {
    Json,
    Xml,
}

impl CmfResponseFormat {
    pub const ALL: &'static [Self] = &[
        Self::Json,
        Self::Xml,
    ];

    pub fn as_str(&self) -> &'static str {
        match self {
            Self::Json => "json",
            Self::Xml => "xml",
        }
    }

    pub fn iter() -> impl Iterator<Item = &'static Self> {
        Self::ALL.iter()
    }

    /// Returns string with enum values separated by comma.
    pub fn values() -> String {
        Self::iter()
            .map(|v| format!("'{}'", v.as_str()))
            .collect::<Vec<_>>()
            .join(", ")
    }
}

impl Default for CmfResponseFormat {
    fn default() -> Self {
        CmfResponseFormat::Json
    }
}

impl TryFrom<&str> for CmfResponseFormat {
    type Error = ClientError;

    fn try_from(s: &str) -> Result<Self, Self::Error> {
        match s.to_lowercase().trim() {
            "json" => Ok(CmfResponseFormat::Json),
            "xml" => Ok(CmfResponseFormat::Xml),
            _ => Err(ClientError::UnsupportedFormat {
                expected: Self::values(),
                actual: s.to_string()
            }),
        }
    }
}

impl TryFrom<Option<&str>> for CmfResponseFormat {
    type Error = ClientError;

    fn try_from(opt: Option<&str>) -> Result<Self, Self::Error> {
        match opt {
            Some(s) => Self::try_from(s),
            None => Ok(CmfResponseFormat::default()),
        }
    }
}