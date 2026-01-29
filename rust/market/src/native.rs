use crate::constants;

use base::native::BaseClient;
use base::errors::ClientError;
use base::enums::ResponseFormat;


pub struct MarketClient {
    pub base: BaseClient,
}

impl MarketClient {
    //noinspection DuplicatedCode
    pub fn new(api_key: &str) -> Result<Self, ClientError> {
        let base = BaseClient::new(
            api_key,
            constants::BASE_URL,
            constants::USER_AGENT,
        )?;

        Ok(Self { base })
    }

    pub fn get(
            &self,
            path: &str,
            fmt: ResponseFormat
    ) -> Result<String, ClientError> {
        // In "Mercado Público", the response format
        // is part of the path, not a query parameter.
        // e.g., "<BASE_URL>/licitaciones.json
        let path = format!("{}.{}", path, fmt.as_str());
        
        let query = [
            ("ticket", self.base.api_key.as_str())
        ];
        
        let response = self.base.get(path.as_str(), &query)?;

        Ok(response)
    }
}