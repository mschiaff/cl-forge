mod native;
mod constants;

use pyo3::prelude::*;


#[pyclass]
pub struct MarketClient {
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
    
    fn get(&self, path: &str) -> PyResult<String> {
        self.client.get(path).map_err(PyErr::from)
    }

    fn __repr__(&self) -> String {
        format!(
            "MarketClient(api_key='{}', base_url='{}')",
            self.ticket(),
            self.base_url(),
        )
    }
}