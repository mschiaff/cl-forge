use std::time::Duration;

use reqwest::blocking::Client;

use crate::errors::ClientError;


pub struct BaseClient {
    pub client: Client,
    pub api_key: String,
    pub base_url: String,
}


impl BaseClient {
    pub fn new(
        api_key: &str,
        base_url: &str,
        user_agent: &str
    ) -> Result<Self, ClientError> {
        let api_key = api_key.trim();

        if api_key.is_empty() {
            return Err(ClientError::EmptyApiKey);
        }

        let client = Client::builder()
            .timeout(Duration::from_secs(10))
            .user_agent(user_agent)
            .build()
            .map_err(ClientError::from)?;

        Ok(Self {
            client,
            api_key: api_key.to_string(),
            base_url: base_url.to_string(),
        })
    }

    pub fn get(
        &self,
        path: &str,
        query: &[(&str, &str)]
    ) -> Result<String, ClientError> {
        let path = path.trim();
        let url = format!("{}{}", self.base_url, path);
        
        if path.is_empty() {
            return Err(ClientError::EmptyPath);
        }
        if !path.starts_with('/') {
            return Err(ClientError::InvalidPath);
        }

        let response = self.client
            .get(url)
            .query(query)
            .send()
            .map_err(ClientError::from)?;
        
        if !response.status().is_success() {
            return Err(ClientError::BadStatus {
                status: response.status().as_u16(),
                body: response.text().unwrap_or_default()
            });
        }

        Ok(
            response
                .text()
                .map_err(ClientError::from)?
        )
    }
}