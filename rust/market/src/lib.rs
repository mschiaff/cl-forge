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
    
    fn get<'py>(&self, py: Python<'py>, path: &str) -> PyResult<Bound<'py, PyAny>> {
        let value = self.client.get(path).map_err(PyErr::from);
        let orjson = py.import("orjson")?;
        let dict = orjson.call_method1("loads", (value?,))?;
        Ok(dict)
    }

    fn __repr__(&self) -> String {
        format!(
            "MarketClient(api_key='{}', base_url='{}')",
            self.ticket(),
            self.base_url(),
        )
    }
}


#[pymodule]
pub fn market(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<MarketClient>()?;
    Ok(())
}