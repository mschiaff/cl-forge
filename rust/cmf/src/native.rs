use crate::constants;

use base::client::CoreClient;
use base::errors::ClientError;
use base::enums::ResponseFormat;

pub struct CmfClient {
    pub base: CoreClient,
}

impl CmfClient {
    //noinspection DuplicatedCode
    pub fn new(api_key: &str) -> Result<Self, ClientError> {
        let base = CoreClient::new(
            api_key,
            constants::BASE_URL,
            constants::USER_AGENT,
        )?;

        Ok(Self { base })
    }

    pub fn get(
            &self,
            path: String,
            fmt: ResponseFormat
    ) -> Result<String, ClientError> {
        let query = [
            ("apikey", self.base.api_key.as_str()),
            ("formato", fmt.as_str())
        ];
        
        let response = self.base.get(path, &query)?;

        Ok(response)
    }
}