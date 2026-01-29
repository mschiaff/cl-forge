use crate::constants;
use crate::enums::CmfResponseFormat;

use base::native::BaseClient;
use base::errors::ClientError;

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
            fmt: Option<&str>
    ) -> Result<String, ClientError> {
        let fmt = CmfResponseFormat::try_from(fmt)
            .map_err(ClientError::from)?;
        
        let query = [
            ("apikey", self.base.api_key.as_str()),
            ("formato", fmt.as_str())
        ];
        let response = self.base.get(path, &query)?;

        Ok(response)
    }
}