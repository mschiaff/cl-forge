use crate::constants;

use base::native::BaseClient;
use base::errors::ClientError;
use::base::enums::ResponseFormat;

pub struct CmfClient {
    pub base: BaseClient,
}

impl CmfClient {
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
        let query = [
            ("apikey", self.base.api_key.as_str()),
            ("formato", fmt.as_str())
        ];
        
        let response = self.base.get(path, &query)?;

        Ok(response)
    }
}