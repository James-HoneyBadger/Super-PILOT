use thiserror::Error;

#[derive(Error, Debug)]
pub enum TimeWarpError {
    #[error("Parse error: {0}")]
    ParseError(String),
    
    #[error("Runtime error: {0}")]
    RuntimeError(String),
    
    #[error("File error: {0}")]
    FileError(#[from] std::io::Error),
    
    #[error("Expression error: {0}")]
    ExpressionError(String),
}
