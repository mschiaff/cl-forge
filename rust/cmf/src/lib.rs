mod constants;
mod client;

use pyo3::prelude::*;
use pyo3::types::{PyString, PyAny};

use base::enums::ResponseFormat;


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


#[pyclass(subclass, module = "cl_forge.core.impl.rs_cl_forge.rs_cmf")]
struct BaseCmfClient {
    inner: client::BaseCmfClient,
}

#[pymethods]
impl BaseCmfClient {
    #[new]
    fn new(api_key: &str) -> PyResult<Self> {
        let inner = client::BaseCmfClient::new(api_key)?;
        
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

    #[pyo3(signature = (path, fmt="json"))]
    fn get<'py>(
        &self,
        py: Python<'py>,
        path: &str,
        fmt: Option<&str>
    ) -> PyResult<Bound<'py, PyAny>> {
        let path = path.to_string();
        let fmt = ResponseFormat::try_from(fmt)?;
        let response = self.inner.get(path, fmt)?;

        build_response(py, fmt, &response)
    }

    #[pyo3(signature = (path, fmt="json"))]
    fn aget<'py>(
        &self,
        py: Python<'py>,
        path: &str,
        fmt: Option<&str>
    ) -> PyResult<Bound<'py, PyAny>> {
        let inner = self.inner.clone();
        let path = path.to_string();
        let fmt = ResponseFormat::try_from(fmt)?;

        pyo3_async_runtimes::tokio::future_into_py(py, async move {
            let response = inner.aget(path, fmt).await?;
            
            Python::attach(|py|{
                build_response(py, fmt, &response)
                    .map(|object| object.unbind())
            })
        })
    }

    fn __repr__(slf: Bound<'_, Self>) -> PyResult<String> {
        let class_name = slf.get_type().name()?;
        let base_url = slf.borrow().base_url();
        Ok(format!(
            "{}(base_url='{}')",
            class_name,
            base_url,
        ))
    }
}


#[pymodule]
pub fn rs_cmf(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<BaseCmfClient>()?;
    Ok(())
}