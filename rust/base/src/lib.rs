pub mod settings;
pub mod errors;
pub mod native;
pub mod enums;

use pyo3::prelude::*;
use pyo3::create_exception;
use pyo3::exceptions::{PyException, PyImportError, PyValueError};

use crate::errors::ClientError;


create_exception!(
    rs_base, ClientException, PyException,
    "Base class for all exceptions raised by API clients."
);
create_exception!(
    rs_base, EmptyApiKey, ClientException,
    "Raised when an API key is not provided."
);
create_exception!(
    rs_base, EmptyPath, ClientException,
    "Raised when a path is not provided."
);
create_exception!(
    rs_base, InvalidPath, ClientException,
    "Raised when API path is invalid."
);
create_exception!(
    rs_base, HttpError, ClientException,
    "Raised when an HTTP error occurs."
);
create_exception!(
    rs_base, BadStatus, ClientException,
    "Raised when an HTTP status code is not 200 (success)."
);
create_exception!(
    rs_base, UnsupportedFormat, ClientException,
    "Raised when an unsupported format is requested."
);


impl From<ClientError> for PyErr {
    fn from(err: ClientError) -> PyErr {
        match err {
            ClientError::EmptyApiKey => EmptyApiKey::new_err(err.to_string()),
            ClientError::EmptyPath => EmptyPath::new_err(err.to_string()),
            ClientError::InvalidPath => InvalidPath::new_err(err.to_string()),
            ClientError::HttpError(_) => HttpError::new_err(err.to_string()),
            ClientError::BadStatus { .. } => BadStatus::new_err(err.to_string()),
            ClientError::UnsupportedFormat { .. } => UnsupportedFormat::new_err(err.to_string()),
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
/// use pyo3::Python;
///
/// let json = r#"{"key": "value"}"#;
/// Python::with_gil(|py| {
///     let dict = json_to_dict(py, json).unwrap();
///     assert_eq!(
///         dict.get_item("key").unwrap().extract::<&str>().unwrap(),
///         "value"
///     );
/// });
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


#[pyclass]
pub struct Token {
    pub inner: settings::Token
}

#[pymethods]
impl Token {
    #[new]
    #[pyo3(signature = (dotenv_path = None))]
    pub fn new(dotenv_path: Option<String>) -> Self {
        Self { inner: settings::Token::new(dotenv_path) }
    }
    
    #[getter]
    fn cmf(&self) -> Option<String> {
        self.inner.cmf.clone()
    }
    
    #[getter]
    fn market(&self) -> Option<String> {
        self.inner.market.clone()
    }
}


#[pyclass]
pub struct Config {
    pub inner: settings::Config
}

#[pymethods]
impl Config {
    #[new]
    #[pyo3(signature = (dotenv_path = None))]
    pub fn new(dotenv_path: Option<String>) -> Self {
        Self { inner: settings::Config::new(dotenv_path) }
    }
    
    #[getter]
    fn tokens(&self) -> Token {
        Token { inner: self.inner.tokens.clone() }
    }
}


#[pymodule]
pub fn rs_base(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("ClientException", m.py().get_type::<ClientException>())?;
    m.add("EmptyApiKey", m.py().get_type::<EmptyApiKey>())?;
    m.add("EmptyPath", m.py().get_type::<EmptyPath>())?;
    m.add("InvalidPath", m.py().get_type::<InvalidPath>())?;
    m.add("HttpError", m.py().get_type::<HttpError>())?;
    m.add("BadStatus", m.py().get_type::<BadStatus>())?;
    m.add("UnsupportedFormat", m.py().get_type::<UnsupportedFormat>())?;
    m.add_class::<Config>()?;
    m.add_class::<Token>()?;
    Ok(())
}