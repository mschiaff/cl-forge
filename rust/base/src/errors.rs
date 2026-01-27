use thiserror::Error;

#[derive(Debug, Error)]
pub enum ClientError {
    #[error("API Key cannot be empty.")]
    EmptyApiKey,

    #[error("Path cannot be empty.")]
    EmptyPath,
    
    #[error("Path must start with '/'")]
    InvalidPath,

    #[error("HTTP error: {0}")]
    HttpError(#[from] reqwest::Error),
    
    #[error("Unexpected status {status}: {body}")]
    BadStatus {status: u16, body: String}
}