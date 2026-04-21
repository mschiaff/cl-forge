use std::sync::Arc;

use crate::constants;

use base::client::CoreClient;
use base::errors::ClientError;
use base::enums::ResponseFormat;

#[derive(Clone)]
pub struct BaseCmfClient {
    pub client: Arc<CoreClient>
}

impl BaseCmfClient {
    pub fn new(api_key: &str) -> Result<Self, ClientError> {
        let inner = CoreClient::new(
            api_key,
            constants::BASE_URL,
            constants::USER_AGENT
        )?;

        Ok(Self { client: Arc::new(inner) })
    }

    fn build_params(
        &self,
        fmt: &ResponseFormat
    ) -> Vec<(&str, &str)> {
        // In "CMF", the API key and response format are query parameters.
        let params = vec![
            ("apikey", self.client.api_key.as_str()),
            ("formato", fmt.as_str())
        ];
        params
    }

    pub fn get(
        &self,
        path: String,
        fmt: ResponseFormat
    ) -> Result<String, ClientError> {
        let params = self.build_params(&fmt);
        let response = self.client.get(path, &params)?;

        Ok(response)
    }

    pub async fn aget(
        &self,
        path: String,
        fmt: ResponseFormat
    ) -> Result<String, ClientError> {
        let params = self.build_params(&fmt);
        let response = self.client.aget(path, &params).await?;

        Ok(response)
    }
}