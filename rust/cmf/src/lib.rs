mod constants;
mod native;
mod enums;

use pyo3::prelude::*;
use pyo3::types::{PyString, PyAny};

use base::errors::ClientError;
use crate::enums::CmfResponseFormat;


#[pyclass]
struct CmfClient {
    client: native::CmfClient,
}

#[pymethods]
impl CmfClient {
    #[new]
    fn new(api_key: &str) -> PyResult<Self> {
        let client = native::CmfClient::new(api_key)
            .map_err(ClientError::from)?.into();
        
        Ok(Self { client })
    }
    
    #[getter]
    fn base_url(&self) -> String {
        self.client.base.base_url.clone()
    }
    
    #[getter]
    fn api_key(&self) -> String {
        self.client.base.api_key.clone()
    }

    #[pyo3(signature = (path, fmt=None))]
    fn get<'py>(
            &self,
            py: Python<'py>,
            path: &str,
            fmt: Option<&str>
    ) -> PyResult<Bound<'py, PyAny>> {
        let body: String = self.client
            .get(path, fmt)
            .map_err(ClientError::from)?
            .into();
        
        let fmt = CmfResponseFormat::try_from(fmt)
            .map_err(ClientError::from)?;

        match fmt {
            CmfResponseFormat::Json => {
                Ok(base::json_to_dict(py, &body)?.into())
            }
            CmfResponseFormat::Xml => {
                Ok(PyString::new(py, &body).into_any())
            }
        }
    }

    fn __repr__(&self) -> String {
        format!(
            "CmfClient(api_key='{}', base_url='{}')",
            self.api_key(),
            self.base_url(),
        )
    }
}


#[pymodule]
pub fn rs_cmf(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<CmfClient>()?;
    Ok(())
}