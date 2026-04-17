use std::sync::Arc;

use crate::constants;

use base::client::CoreClient;
use base::errors::ClientError;
use base::enums::ResponseFormat;

#[derive(Clone)]
pub struct BaseMarketClient {
    pub client: Arc<CoreClient>
}

impl BaseMarketClient {
    pub fn new(api_key: &str) -> Result<Self, ClientError> {
        let inner = CoreClient::new(
            api_key,
            constants::BASE_URL,
            constants::USER_AGENT
        )?;
        
        Ok(Self { client: Arc::new(inner) })
    }
    
    fn build_path(&self, path: &str, fmt: ResponseFormat) -> String {
        // In "Mercado Público", the response format
        // is part of the path, not a query parameter.
        // e.g., "<BASE_URL>/licitaciones.json
        let path = path.trim();
        format!("{}.{}", path, fmt.as_str())
    }
    
    fn build_params<'a>(
        &'a self,
        params: &'a [(String, String)]
    ) -> Vec<(&'a str, &'a str)> {
        let mut query = vec![
            ("ticket", self.client.api_key.as_str())
        ];
        for (k, v) in params {
            query.push((k.as_str(), v.as_str()));
        }
        query
    }
    
    pub fn get(
            &self,
            path: &str,
            fmt: ResponseFormat,
            params: &[(String, String)]
    ) -> Result<String, ClientError> {
        let path = self.build_path(path, fmt);
        let params = self.build_params(params);
        let response = self.client.get(path, &params)?;
        
        Ok(response)
    }

    pub async fn aget(
            &self,
            path: &str,
            fmt: ResponseFormat,
            params: &[(String, String)]
    ) -> Result<String, ClientError> {
        let path = self.build_path(path, fmt);
        let params = self.build_params(params);
        let response = self.client.aget(path, &params).await?;

        Ok(response)
    }
}
