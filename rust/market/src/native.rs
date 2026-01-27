use crate::constants;

use base::native::BaseClient;
use base::errors::ClientError;


pub struct MarketClient {
    pub base: BaseClient,
}


impl MarketClient {
    pub fn new(api_key: &str) -> Result<Self, ClientError> {
        let base = BaseClient::new(
            api_key,
            constants::BASE_URL,
            constants::USER_AGENT,
        )?;

        Ok(Self { base })
    }

    pub fn get(&self, path: &str) -> Result<String, ClientError> {
        let query = [("ticket", self.base.api_key.as_str())];
        let response = self.base.get(path, &query)?;

        if !response.status().is_success() {
            return Err(ClientError::BadStatus {
                status: response.status().as_u16(),
                body: response.text().unwrap_or_default()
            });
        }

        Ok(response.text()?)
    }
}