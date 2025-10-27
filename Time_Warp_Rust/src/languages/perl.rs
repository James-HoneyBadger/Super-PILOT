use crate::interpreter::{ExecutionResult, InterpreterError, TurtleState};

pub struct PerlExecutor {
    // For now, this is a stub - full Perl execution would require Perl interpreter integration
}

impl PerlExecutor {
    pub fn new() -> Self {
        Self {}
    }

    pub fn load_program(&mut self, _program: Vec<String>) {
        // Stub implementation
    }

    pub fn execute_command(
        &mut self,
        _command: &str,
        _turtle: &mut TurtleState,
    ) -> ExecutionResult {
        // Stub - would need Perl interpreter integration
        ExecutionResult::Error(InterpreterError::InvalidCommand(
            "Perl execution not yet implemented".to_string(),
        ))
    }
}
