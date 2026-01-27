pub mod errors;
pub mod native;

use pyo3::prelude::*;
use pyo3::create_exception;
use pyo3::exceptions::{PyException, PyImportError, PyValueError};


create_exception!(base, ClientException, PyException);
create_exception!(base, EmptyApiKey, ClientException);
create_exception!(base, EmptyPath, ClientException);
create_exception!(base, InvalidPath, ClientException);
create_exception!(base, HttpError, ClientException);
create_exception!(base, BadStatus, ClientException);


impl From<errors::ClientError> for PyErr {
    fn from(err: errors::ClientError) -> PyErr {
        match err {
            errors::ClientError::EmptyApiKey =>
                EmptyApiKey::new_err(err.to_string()),
            errors::ClientError::EmptyPath =>
                EmptyApiKey::new_err(err.to_string()),
            errors::ClientError::InvalidPath =>
                InvalidPath::new_err(err.to_string()),
            errors::ClientError::HttpError(e) =>
                HttpError::new_err(e.to_string()),
            errors::ClientError::BadStatus { status, body } =>
                BadStatus::new_err(format!("{}: {}", status, body))
        }
    }
}


/// Parses a JSON string into a Python dictionary.
///
/// # Arguments
/// * `body` - JSON formatted string.
///
/// # Returns
/// * `Ok(Bound<PyAny>)` - Python dictionary object.
/// * `Err(PyErr)`:
///     - [`PyImportError`] - If 'orjson' isn't installed.
///     - [`PyValueError`] - If fail parsing the JSON string.
///
/// # Examples
/// ```
/// use base::json_to_dict;
///
/// let json = r#"{"key": "value"}"#;
/// let dict = to_dict(json).unwrap();
/// assert_eq!(dict["key"].as_str().unwrap(), "value");
/// ```
#[pyfunction]
pub fn json_to_dict<'py>(
        py: Python<'py>,
        body: &str
) -> PyResult<Bound<'py, PyAny>> {
    let orjson = py.import("orjson")
        .map_err(
            |e| PyImportError::new_err(e)
    )?;
    let dict = orjson.call_method1("loads", (body,))
        .map_err(
            |e| PyValueError::new_err(e)
        )?;

    Ok(dict)
}

#[pymodule]
pub fn base(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("ClientException", m.py().get_type::<ClientException>())?;
    m.add("EmptyApiKey", m.py().get_type::<EmptyApiKey>())?;
    m.add("EmptyPath", m.py().get_type::<EmptyPath>())?;
    m.add("InvalidPath", m.py().get_type::<InvalidPath>())?;
    m.add("HttpError", m.py().get_type::<HttpError>())?;
    m.add("BadStatus", m.py().get_type::<BadStatus>())?;
    Ok(())
}