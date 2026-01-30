use std::env;
use std::path::Path;

use dotenv::from_path;


#[derive(Debug, Clone, Default)]
pub struct Token {
    pub cmf: Option<String>,
    pub market: Option<String>,
}

impl Token {
    /// Creates a new Token instance by loading environment variables.
    ///
    /// Dotenv file takes presedence over terminal-defined variables.
    /// If `dotenv_path` is provided, it loads the .env file from that path.
    /// Otherwise, it looks for a .env file in the current or parent directories.
    pub fn new(dotenv_path: Option<String>) -> Self {
        if let Some(path) = dotenv_path {
            let _ = from_path(Path::new(&path));
        } else {
            let _ = dotenv::dotenv();
        }

        let cmf = env::var("CLFORGE_CMF_TOKEN")
            .ok()
            .filter(|token| !token.is_empty());
        let market = env::var("CLFORGE_MARKET_TOKEN")
            .ok()
            .filter(|token| !token.is_empty());

        Self { cmf, market }
    }
}

#[derive(Debug, Clone, Default)]
pub struct Settings {
    pub tokens: Token
}

impl Settings {
    pub fn new(dotenv_path: Option<String>) -> Self {
        Self { tokens: Token::new(dotenv_path) }
    }
}