mod native;
mod constants;

use pyo3::prelude::*;

use base::errors::ClientError;

#[pyclass]
pub struct MarketClient {
    client: native::MarketClient,
}

#[pymethods]
impl MarketClient {
    #[new]
    fn new(ticket: &str) -> PyResult<Self> {
        let client = native::MarketClient::new(ticket)
            .map_err(ClientError::from)?;
        
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
    
    fn get<'py>(
        &self,
        py: Python<'py>,
        path: &str
    ) -> PyResult<Bound<'py, PyAny>> {
        let body = self.client.get(path).map_err(ClientError::from)?;

        let orjson = py.import("orjson")?;
        let dict = orjson.call_method1("loads",(body,))?;
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