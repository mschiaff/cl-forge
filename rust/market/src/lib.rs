mod constants;
mod client;

use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use pyo3::types::{PyString, PyAny, PyDict};

use base::enums::ResponseFormat;

fn extract_params(
    params: Option<Bound<'_, PyDict>>
) -> PyResult<Vec<(String, String)>> {
    let mut new_params = Vec::new();

    if let Some(dict) = params {
        for (k, v) in dict.iter() {
            let key = k.to_string();

            if key.trim().eq_ignore_ascii_case("ticket") {
                return Err(
                    PyValueError::new_err(
                        "Ticket cannot be overridden."
                    )
                );
            }

            new_params.push((key, v.to_string()));
        }
    }

    Ok(new_params)
}

fn build_response<'py>(
    py: Python<'py>,
    fmt: ResponseFormat,
    body: &str
) -> PyResult<Bound<'py, PyAny>> {
    match fmt {
        ResponseFormat::Json => base::json_to_dict(py, body),
        ResponseFormat::Xml => Ok(PyString::new(py, body).into_any()),
    }
}

#[pyclass(subclass, module = "cl_forge.core.impl.rs_cl_forge.rs_market")]
struct BaseMarketClient {
    inner: client::BaseMarketClient,
}

#[pymethods]
impl BaseMarketClient {
    #[new]
    fn new(api_key: &str) -> PyResult<Self> {
        let inner = client::BaseMarketClient::new(api_key)?;
        
        Ok(Self { inner })
    }
    
    #[getter]
    fn base_url(&self) -> String {
        self.inner.client.base_url.clone()
    }
    
    #[getter]
    fn api_key(&self) -> String {
        self.inner.client.api_key.clone()
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
        let params = extract_params(params)?;
        let response = self.inner.get(path, fmt, &params)?;

        build_response(py, fmt, &response)
    }

    //noinspection DuplicatedCode
    #[pyo3(signature = (path, fmt="json", params=None))]
    fn aget<'py>(
        &self,
        py: Python<'py>,
        path: &str,
        fmt: Option<&str>,
        params: Option<Bound<'py, PyDict>>
    ) -> PyResult<Bound<'py, PyAny>> {
        let inner = self.inner.clone();
        let path = path.to_string();
        let fmt = ResponseFormat::try_from(fmt)?;
        let params = extract_params(params)?;

        pyo3_async_runtimes::tokio::future_into_py(py, async move {
            let response = inner.aget(path.as_str(), fmt, &params).await?;

            Python::attach(|py| {
                build_response(py, fmt, &response)
                    .map(|object| object.unbind())
            })
        })
    }

    fn __repr__(&self) -> String {
        format!(
            "BaseMarketClient(base_url='{}')",
            self.base_url(),
        )
    }
}


#[pymodule]
pub fn rs_market(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<BaseMarketClient>()?;
    Ok(())
}
