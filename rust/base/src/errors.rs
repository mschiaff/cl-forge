use thiserror::Error;

#[derive(Debug, Error)]
pub enum ClientError {
    #[error("API Key cannot be empty.")]
    EmptyApiKey,
    
    #[error("Invalid path: {0}")]
    InvalidPath(String),

    #[error("HTTP error: {0}")]
    HttpError(#[from] reqwest::Error),
    
    #[error("Unexpected status {status}: {body}")]
    BadStatus {status: u16, body: String}
}