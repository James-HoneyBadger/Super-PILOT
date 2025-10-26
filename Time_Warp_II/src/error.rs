use std::fmt;

/// Comprehensive error type for the Time Warp IDE application
#[derive(Debug, Clone)]
pub enum AppError {
    /// Errors from the BASIC interpreter
    Interpreter(crate::languages::basic::ast::InterpreterError),
    /// File I/O errors
    File(FileError),
    /// External dependency errors
    External(ExternalError),
}

#[derive(Debug, Clone)]
pub enum FileError {
    IoError { path: String, message: String },
}

#[derive(Debug, Clone)]
pub enum ExternalError {
    SystemError {
        command: String,
        exit_code: i32,
        stderr: String,
    },
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AppError::Interpreter(err) => write!(f, "Interpreter error: {}", err),
            AppError::File(err) => write!(f, "File error: {}", err),
            AppError::External(err) => write!(f, "External error: {}", err),
        }
    }
}

impl fmt::Display for FileError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            FileError::IoError { path, message } => {
                write!(f, "I/O error for {}: {}", path, message)
            }
        }
    }
}

impl fmt::Display for ExternalError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ExternalError::SystemError {
                command,
                exit_code,
                stderr,
            } => {
                write!(
                    f,
                    "System command '{}' failed (exit code {}): {}",
                    command, exit_code, stderr
                )
            }
        }
    }
}

impl std::error::Error for AppError {}
impl std::error::Error for FileError {}
impl std::error::Error for ExternalError {}

// Conversion implementations
impl From<FileError> for AppError {
    fn from(err: FileError) -> Self {
        AppError::File(err)
    }
}

impl From<ExternalError> for AppError {
    fn from(err: ExternalError) -> Self {
        AppError::External(err)
    }
}

// Convert from std::io::Error
impl From<std::io::Error> for AppError {
    fn from(err: std::io::Error) -> Self {
        AppError::External(ExternalError::SystemError {
            command: "I/O operation".to_string(),
            exit_code: -1,
            stderr: err.to_string(),
        })
    }
}

// Result type alias for convenience
pub type AppResult<T> = Result<T, AppError>;
