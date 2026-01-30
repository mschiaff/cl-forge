mod native;
mod constants;

use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use pyo3::types::{PyString, PyAny, PyDict};

use base::enums::ResponseFormat;

#[pyclass]
struct MarketClient {
    client: native::MarketClient,
}

#[pymethods]
impl MarketClient {
    #[new]
    fn new(ticket: &str) -> PyResult<Self> {
        let client = native::MarketClient::new(ticket)?;
        
        Ok(Self { client })
    }
    
    #[getter]
    fn base_url(&self) -> String {
        self.client.base.base_url.clone()
    }
    
    #[getter]
    fn ticket(&self) -> String {
        self.client.base.api_key.clone()
    }

    //noinspection DuplicatedCode
    #[pyo3(signature = (path, fmt="json", params=None))]
    fn get<'py>(
            &self,
            py: Python<'py>,
            path: &str,
            fmt: Option<&str>,
            params: Option<Bound<'py, PyDict>>
    ) -> PyResult<Bound<'py, PyAny>> {
        let fmt = ResponseFormat::try_from(fmt)?;

        let mut new_params: Vec<(String, String)> = Vec::new();

        if let Some(dict) = params {
            for (k, v) in dict.iter() {
                if k.to_string().to_lowercase().trim() == "ticket" {
                    return Err(
                        PyValueError::new_err(
                            "Ticket cannot be overridden."
                        )
                    )
                }
                new_params.push(
                    (k.to_string(), v.to_string())
                )
            }
        }

        let body: String = self.client
            .get(path, fmt, &new_params)?;

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
            "MarketClient(ticket='{}', base_url='{}')",
            self.ticket(),
            self.base_url(),
        )
    }
}


#[pymodule]
pub fn rs_market(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<MarketClient>()?;
    Ok(())
}