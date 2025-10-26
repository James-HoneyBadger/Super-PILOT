pub mod ast;
pub mod interpreter;
pub mod parser;
pub mod tokenizer;

// Re-export main types for convenience
pub use ast::{ExecutionResult, GraphicsCommand};
pub use interpreter::Interpreter;
