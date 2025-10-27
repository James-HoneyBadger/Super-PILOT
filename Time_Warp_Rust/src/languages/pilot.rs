use crate::interpreter::{ExecutionResult, InterpreterError, TurtleState};
use std::collections::HashMap;

pub struct PilotExecutor {
    variables: HashMap<String, String>,
    labels: HashMap<String, usize>,
    current_line: usize,
    program: Vec<String>,
}

impl PilotExecutor {
    pub fn new() -> Self {
        Self {
            variables: HashMap::new(),
            labels: HashMap::new(),
            current_line: 0,
            program: Vec::new(),
        }
    }

    pub fn load_program(&mut self, program: Vec<String>) {
        self.program = program;
        self.labels.clear();
        self.current_line = 0;

        // Parse labels
        for (i, line) in self.program.iter().enumerate() {
            let line = line.trim();
            if line.starts_with('*') {
                if let Some(label_end) = line.find(':') {
                    let label = line[1..label_end].to_string();
                    self.labels.insert(label, i);
                }
            }
        }
    }

    pub fn execute_command(&mut self, command: &str, turtle: &mut TurtleState) -> ExecutionResult {
        let command = command.trim();

        if command.is_empty() {
            return ExecutionResult::Continue;
        }

        // Handle different PILOT commands
        if let Some(colon_pos) = command.find(':') {
            let cmd_type = &command[..colon_pos];
            let content = &command[colon_pos + 1..];

            match cmd_type.to_uppercase().as_str() {
                "T" => self.handle_type(content, turtle),
                "A" => self.handle_accept(content),
                "J" => self.handle_jump(content),
                "Y" => self.handle_yes(content),
                "N" => self.handle_no(content),
                "U" => self.handle_use(content),
                "C" => self.handle_compute(content),
                "R" => self.handle_remark(content),
                "E" => self.handle_end(content),
                _ => ExecutionResult::Error(InterpreterError::InvalidCommand(format!(
                    "Unknown PILOT command: {}",
                    cmd_type
                ))),
            }
        } else {
            // Handle label lines or plain text
            if command.starts_with('*') {
                // Label line, skip
                ExecutionResult::Continue
            } else {
                // Plain text - treat as type command
                self.handle_type(command, turtle)
            }
        }
    }

    fn handle_type(&self, content: &str, turtle: &mut TurtleState) -> ExecutionResult {
        let processed = self.process_variables(content);
        // In a real implementation, this would output to the UI
        println!("{}", processed);
        ExecutionResult::Continue
    }

    fn handle_accept(&mut self, content: &str) -> ExecutionResult {
        // In a real implementation, this would prompt for input
        // For now, we'll simulate with a default value
        let var_name = content.trim();
        if !var_name.is_empty() {
            self.variables
                .insert(var_name.to_string(), "simulated_input".to_string());
        }
        ExecutionResult::Continue
    }

    fn handle_jump(&mut self, content: &str) -> ExecutionResult {
        let label = content.trim();
        if let Some(&line) = self.labels.get(label) {
            self.current_line = line;
            ExecutionResult::Jump(line)
        } else {
            ExecutionResult::Error(InterpreterError::InvalidLabel(format!(
                "Label not found: {}",
                label
            )))
        }
    }

    fn handle_yes(&mut self, content: &str) -> ExecutionResult {
        // Simplified - in real PILOT, this checks a condition
        // For now, assume condition is true
        let label = content.trim();
        if let Some(&line) = self.labels.get(label) {
            self.current_line = line;
            ExecutionResult::Jump(line)
        } else {
            ExecutionResult::Error(InterpreterError::InvalidLabel(format!(
                "Label not found: {}",
                label
            )))
        }
    }

    fn handle_no(&mut self, content: &str) -> ExecutionResult {
        // Simplified - in real PILOT, this checks a condition
        // For now, assume condition is false, so continue
        ExecutionResult::Continue
    }

    fn handle_use(&mut self, content: &str) -> ExecutionResult {
        // USE command - call a procedure
        // Simplified implementation
        ExecutionResult::Continue
    }

    fn handle_compute(&mut self, content: &str) -> ExecutionResult {
        // COMPUTE command - mathematical operations
        // Simplified implementation
        ExecutionResult::Continue
    }

    fn handle_remark(&self, content: &str) -> ExecutionResult {
        // REMARK command - comments, ignore
        ExecutionResult::Continue
    }

    fn handle_end(&self, content: &str) -> ExecutionResult {
        // END command - terminate program
        ExecutionResult::End
    }

    fn process_variables(&self, text: &str) -> String {
        let mut result = text.to_string();
        for (var, value) in &self.variables {
            result = result.replace(&format!("#{}", var), value);
        }
        result
    }

    pub fn get_variable(&self, name: &str) -> Option<&String> {
        self.variables.get(name)
    }

    pub fn set_variable(&mut self, name: String, value: String) {
        self.variables.insert(name, value);
    }
}
