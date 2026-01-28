use crate::constants;

use base::native::BaseClient;
use base::errors::ClientError;


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
        ).map_err(ClientError::from)?;

        Ok(Self { base })
    }

    pub fn get(&self, path: &str) -> Result<String, ClientError> {
        let query = [
            ("ticket", self.base.api_key.as_str())
        ];
        let response = self.base
            .get(path, &query)
            .map_err(ClientError::from)?;

        Ok(response)
    }
}