use crate::errors::ClientError;


#[derive(Clone, Copy, PartialEq, Eq)]
pub enum ResponseFormat {
    Json,
    Xml,
}

impl ResponseFormat {
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

impl Default for ResponseFormat {
    fn default() -> Self {
        ResponseFormat::Json
    }
}

impl TryFrom<&str> for ResponseFormat {
    type Error = ClientError;

    fn try_from(s: &str) -> Result<Self, Self::Error> {
        match s.to_lowercase().trim() {
            "json" => Ok(ResponseFormat::Json),
            "xml" => Ok(ResponseFormat::Xml),
            _ => Err(ClientError::UnsupportedFormat {
                expected: Self::values(),
                actual: s.to_string()
            }),
        }
    }
}

impl TryFrom<Option<&str>> for ResponseFormat {
    type Error = ClientError;

    fn try_from(opt: Option<&str>) -> Result<Self, Self::Error> {
        match opt {
            Some(s) => Self::try_from(s),
            None => Err(ClientError::UnsupportedFormat {
                expected: Self::values(),
                actual: "None".to_string()
            })
        }
    }
}