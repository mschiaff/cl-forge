mod constants;
mod native;

use pyo3::prelude::*;
use pyo3::types::{PyString, PyAny};

use base::enums::ResponseFormat;


#[pyclass]
struct CmfClient {
    client: native::CmfClient,
}

#[pymethods]
impl CmfClient {
    #[new]
    fn new(api_key: &str) -> PyResult<Self> {
        let client = native::CmfClient::new(api_key)?;
        
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

    //noinspection DuplicatedCode
    #[pyo3(signature = (path, fmt="json"))]
    fn get<'py>(
            &self,
            py: Python<'py>,
            path: &str,
            fmt: Option<&str>
    ) -> PyResult<Bound<'py, PyAny>> {
        let fmt = ResponseFormat::try_from(fmt)?;
        let body: String = self.client.get(path, fmt)?;
        
        match fmt {
            ResponseFormat::Json => {
                Ok(base::json_to_dict(py, &body)?)
            }
            ResponseFormat::Xml => {
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