mod native;
mod constants;
mod enums;

use pyo3::prelude::*;


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
    
    fn get<'py>(
            &self,
            py: Python<'py>,
            path: &str
    ) -> PyResult<Bound<'py, PyAny>> {
        let body: String = self.client
            .get(path)?;
        let dict = base::json_to_dict(py, &body)?
            .into();

        Ok(dict)
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