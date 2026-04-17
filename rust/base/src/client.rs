use std::time::Duration;

use crate::errors::ClientError;


#[derive(Debug)]
pub struct CoreClient {
    pub api_key: String,
    pub base_url: String,
    pub aclient: reqwest::Client,
    pub client: reqwest::blocking::Client,
}

impl CoreClient {
    pub fn new(
        api_key: &str,
        base_url: &str,
        user_agent: &str,
    ) -> Result<Self, ClientError> {
        let aclient = reqwest::Client::builder()
            .timeout(Duration::from_secs(10))
            .user_agent(user_agent)
            .build()?;

        let client = reqwest::blocking::Client::builder()
            .timeout(Duration::from_secs(10))
            .user_agent(user_agent)
            .build()?;

        let api_key = api_key
            .trim()
            .to_string();

        if api_key.is_empty() {
            return Err(ClientError::EmptyApiKey);
        }

        Ok(Self {
            base_url: base_url.to_string(),
            api_key: api_key.to_string(),
            aclient,
            client
        })
    }

    fn build(
        &self,
        path: String,
    ) -> Result<String, ClientError> {
        let path = path.trim();
        let url = format!("{}{}", self.base_url, path);

        if path.is_empty() {
            return Err(ClientError::EmptyPath);
        }
        if !path.starts_with('/') {
            return Err(ClientError::InvalidPath);
        }

        Ok(url)
    }

    //noinspection DuplicatedCode
    pub fn get(
        &self,
        path: String,
        params: &[(&str, &str)]
    ) -> Result<String, ClientError> {
        let url = self.build(path)?;

        let response = self.client
            .get(url)
            .query(params)
            .send()?;

        if !response.status().is_success() {
            return Err(ClientError::BadStatus {
                status: response.status().as_u16(),
                body: response.text().unwrap_or_default()
            });
        }

        Ok(response.text()?)
    }

    //noinspection DuplicatedCode
    pub async fn aget(
        &self,
        path: String,
        params: &[(&str, &str)]
    ) -> Result<String, ClientError> {
        let url = self.build(path)?;

        let response = self.aclient
            .get(url)
            .query(params)
            .send()
            .await?;

        if !response.status().is_success() {
            return Err(ClientError::BadStatus {
                status: response.status().as_u16(),
                body: response.text().await.unwrap_or_default()
            });
        }

        Ok(response.text().await?)
    }
}