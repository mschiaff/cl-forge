pub mod errors;
pub mod native;

use pyo3::prelude::*;
use pyo3::create_exception;
use pyo3::exceptions::PyException;


create_exception!(base, ClientException, PyException);
create_exception!(base, EmptyApiKey, ClientException);
create_exception!(base, InvalidPath, ClientException);
create_exception!(base, HttpError, ClientException);
create_exception!(base, BadStatus, ClientException);


impl From<errors::ClientError> for PyErr {
    fn from(err: errors::ClientError) -> PyErr {
        match err {
            errors::ClientError::EmptyApiKey => 
                EmptyApiKey::new_err(err.to_string()),
            errors::ClientError::InvalidPath(p) =>
                InvalidPath::new_err(p),
            errors::ClientError::HttpError(e) =>
                HttpError::new_err(e.to_string()),
            errors::ClientError::BadStatus { status, body } =>
                BadStatus::new_err(format!("{}: {}", status, body))
        }
    }
}