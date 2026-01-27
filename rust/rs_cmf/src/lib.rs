mod errors;
mod constants;
mod native;
mod enums;

use std::time::Duration;

use pyo3::prelude::*;
use pyo3::create_exception;
use pyo3::types::{PyDict, PyString, PyAny};
use pyo3::exceptions::{PyException, PyValueError};
use reqwest::blocking::Client;
use secrecy::{ExposeSecret, SecretString};

use crate::errors::CmfClientError;
use crate::enums::CmfResponseFormat;


create_exception!(_rs_cmf, CmfClientException, PyException);

create_exception!(_rs_cmf, EmptyPath, CmfClientException);
create_exception!(_rs_cmf, BadStatus, CmfClientException);
create_exception!(_rs_cmf, EmptyApiKey, CmfClientException);
create_exception!(_rs_cmf, InvalidPath, CmfClientException);
create_exception!(_rs_cmf, ConnectError, CmfClientException);

impl From<CmfClientError> for PyErr {
    fn from(err: CmfClientError) -> PyErr {
        match err {
            CmfClientError::EmptyPath =>
                EmptyPath::new_err(err.to_string()),
            CmfClientError::BadStatus { .. } =>
                BadStatus::new_err(err.to_string()),
            CmfClientError::EmptyApiKey =>
                EmptyApiKey::new_err(err.to_string()),
            CmfClientError::InvalidPath =>
                InvalidPath::new_err(err.to_string()),
            CmfClientError::ConnectError(_) =>
                ConnectError::new_err(err.to_string()),
            CmfClientError::BaseError(e) => e.into(),
        }
    }
}


#[pyclass]
struct CmfClient {
    client: Client,
    api_key: SecretString,
    #[pyo3(get)]
    base_url: String,
}


#[pymethods]
impl CmfClient {
    #[new]
    fn new(api_key: &str) -> PyResult<Self> {
        let api_key = api_key.trim();

        if api_key.is_empty() {
            return Err(CmfClientError::EmptyApiKey.into());
        }

        let session = Client::builder()
            .timeout(Duration::from_secs(10))
            .user_agent(constants::USER_AGENT)
            .build()
            .map_err(CmfClientError::from)?;

        let base_url = constants::BASE_URL;

        Ok(Self {
            client: session,
            api_key: SecretString::new(Box::from(api_key)),
            base_url: base_url.to_string(),
        })
    }

    #[getter]
    fn api_key(&self) -> String {
        let full_key = self.api_key.expose_secret();
        let key_part = if full_key.len() > 5 {
            &full_key[..5]
        } else {
            full_key
        };
        format!("{}...", key_part)
    }

    fn __repr__(&self) -> String {
        format!(
            "CmfClient(api_key='{}', base_url='{}')",
            self.api_key(),
            &self.base_url,
        )
    }

    #[pyo3(signature = (path, format=None, params=None))]
    fn get<'py>(
            &self,
            py: Python<'py>,
            path: &str,
            format: Option<&str>,
            params: Option<&Bound<'py, PyDict>>,
    ) -> PyResult<Bound<'py, PyAny>> {
        let path = path.trim();

        if path.is_empty() {
            return Err(CmfClientError::EmptyPath.into());
        }
        if !path.starts_with('/') {
            return Err(CmfClientError::InvalidPath.into())
        }

        let format_enum = CmfResponseFormat::try_from(format)
            .map_err(CmfClientError::from)?;

        let url = format!("{}{}", self.base_url, path);
        let mut qparams: Vec<(String, String)> = vec![
            ("apikey".into(), self.api_key.expose_secret().into()),
            ("formato".into(), format_enum.as_str().to_string())
        ];

        if let Some(p) = params {
            for (k, v) in p.iter() {
                let k = k.extract::<String>()?;
                let v = v.str()?.to_str()?.to_string();
                qparams.push((k, v));
            }
        }

        let response = self.client
            .get(url)
            .query(&qparams)
            .send()
            .map_err(CmfClientError::from)?;
        let status = response.status();

        if !status.is_success() {
            let body = response.text().unwrap_or_default();
            return Err(
                CmfClientError::BadStatus {
                    status: status.as_u16(), body
                }.into()
            );
        }

        let body = response.text().map_err(CmfClientError::from)?;
        
        match format_enum {
            CmfResponseFormat::Json => {
                let _json: serde_json::Value = serde_json::from_str(&body)
                    .map_err(
                        |e| PyValueError::new_err(
                            format!("Failed to parse JSON response: {}", e)
                        )
                    )?;
                
                let json_module = py.import("json")?;
                let dict = json_module.call_method1("loads", (body,))?;
                Ok(dict)
            }
            CmfResponseFormat::Xml => {
                Ok(PyString::new(py, &body).into_any())
            }
        }
    }
}


#[pymodule]
pub fn _rs_cmf(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<CmfClient>()?;
    m.add("CmfClientException", m.py().get_type::<CmfClientException>())?;
    m.add("EmptyPath", m.py().get_type::<EmptyPath>())?;
    m.add("BadStatus", m.py().get_type::<BadStatus>())?;
    m.add("EmptyApiKey", m.py().get_type::<EmptyApiKey>())?;
    m.add("InvalidPath", m.py().get_type::<InvalidPath>())?;
    m.add("ConnectError", m.py().get_type::<ConnectError>())?;
    Ok(())
}