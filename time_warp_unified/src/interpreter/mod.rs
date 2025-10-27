use anyhow::Result;
use std::collections::HashMap;

use crate::graphics::TurtleState;
use crate::languages::{Language, pilot, basic, logo};

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ExecutionResult {
    Continue,
    End,
    Jump(usize),
}

pub struct Interpreter {
    // Core state
    pub variables: HashMap<String, f64>,
    pub string_variables: HashMap<String, String>,
    pub output: Vec<String>,
    
    // Program state
    program_lines: Vec<(Option<usize>, String)>,
    current_line: usize,
    labels: HashMap<String, usize>,
    
    // Control flow stacks
    gosub_stack: Vec<usize>,
    for_stack: Vec<ForContext>,
    
    // PILOT-specific
    match_flag: bool,
    last_match_set: bool,
    stored_condition: Option<bool>,
    
    // Language detection
    current_language: Language,
    
    // I/O
    input_callback: Option<Box<dyn FnMut(&str) -> String>>,
}

#[derive(Clone)]
struct ForContext {
    var_name: String,
    end_value: f64,
    step: f64,
    for_line: usize,
}

impl Interpreter {
    pub fn new() -> Self {
        Self {
            variables: HashMap::new(),
            string_variables: HashMap::new(),
            output: Vec::new(),
            
            program_lines: Vec::new(),
            current_line: 0,
            labels: HashMap::new(),
            
            gosub_stack: Vec::new(),
            for_stack: Vec::new(),
            
            match_flag: false,
            last_match_set: false,
            stored_condition: None,
            
            current_language: Language::Pilot,
            
            input_callback: None,
        }
    }
    
    pub fn load_program(&mut self, program_text: &str) -> Result<()> {
        self.reset();
        
        let lines: Vec<&str> = program_text.lines().collect();
        self.program_lines.clear();
        
        for (idx, line) in lines.iter().enumerate() {
            let (line_num, command) = self.parse_line(line);
            self.program_lines.push((line_num, command.to_string()));
            
            // Collect PILOT labels
            if command.starts_with("L:") {
                let label = command[2..].trim();
                self.labels.insert(label.to_string(), idx);
            }
        }
        
        Ok(())
    }
    
    pub fn execute(&mut self, turtle: &mut TurtleState) -> Result<Vec<String>> {
        self.output.clear();
        self.current_line = 0;
        
        let max_iterations = 100000;
        let mut iterations = 0;
        
        while self.current_line < self.program_lines.len() && iterations < max_iterations {
            iterations += 1;
            
            let (_, command) = self.program_lines[self.current_line].clone();
            
            if command.trim().is_empty() {
                self.current_line += 1;
                continue;
            }
            
            let result = self.execute_line(&command, turtle)?;
            
            match result {
                ExecutionResult::Continue => self.current_line += 1,
                ExecutionResult::End => break,
                ExecutionResult::Jump(line) => self.current_line = line,
            }
        }
        
        if iterations >= max_iterations {
            self.log_output("⚠️ Warning: Maximum iterations reached".to_string());
        }
        
        Ok(self.output.clone())
    }
    
    fn execute_line(&mut self, command: &str, turtle: &mut TurtleState) -> Result<ExecutionResult> {
        let cmd_type = self.determine_command_type(command);
        
        match cmd_type {
            Language::Pilot => pilot::execute(self, command, turtle),
            Language::Basic => basic::execute(self, command, turtle),
            Language::Logo => logo::execute(self, command, turtle),
            _ => Ok(ExecutionResult::Continue),
        }
    }
    
    fn determine_command_type(&self, command: &str) -> Language {
        let cmd = command.trim();
        
        // PILOT: commands start with letter followed by colon
        if cmd.len() > 1 && cmd.chars().nth(1) == Some(':') {
            return Language::Pilot;
        }
        
        // Logo keywords
        let logo_keywords = ["FORWARD", "FD", "BACK", "BK", "LEFT", "LT", "RIGHT", "RT",
                            "PENUP", "PU", "PENDOWN", "PD", "CLEARSCREEN", "CS", "HOME",
                            "SETXY", "REPEAT", "TO", "END"];
        let first_word = cmd.split_whitespace().next().unwrap_or("");
        if logo_keywords.contains(&first_word.to_uppercase().as_str()) {
            return Language::Logo;
        }
        
        // BASIC keywords
        let basic_keywords = ["LET", "PRINT", "INPUT", "GOTO", "IF", "THEN", "FOR", "NEXT",
                             "GOSUB", "RETURN", "REM", "DIM", "DATA", "READ"];
        if basic_keywords.contains(&first_word.to_uppercase().as_str()) {
            return Language::Basic;
        }
        
        // Default to PILOT
        Language::Pilot
    }
    
    fn parse_line(&self, line: &str) -> (Option<usize>, &str) {
        let line = line.trim();
        
        // Check for line number at start
        let parts: Vec<&str> = line.splitn(2, char::is_whitespace).collect();
        if let Some(first) = parts.first() {
            if let Ok(num) = first.parse::<usize>() {
                if parts.len() > 1 {
                    return (Some(num), parts[1].trim());
                }
            }
        }
        
        (None, line)
    }
    
    pub fn log_output(&mut self, text: String) {
        self.output.push(text);
    }
    
    pub fn evaluate_expression(&self, expr: &str) -> Result<f64> {
        // Simple expression evaluator for now
        // TODO: Implement full expression parser with variables
        expr.trim()
            .parse::<f64>()
            .or_else(|_| {
                self.variables
                    .get(expr.trim())
                    .copied()
                    .ok_or_else(|| anyhow::anyhow!("Unknown variable: {}", expr))
            })
    }
    
    pub fn interpolate_text(&self, text: &str) -> String {
        let mut result = text.to_string();
        
        // Replace *VAR* with variable values
        let re = regex::Regex::new(r"\*([A-Z_][A-Z0-9_]*)\*").unwrap();
        for cap in re.captures_iter(text) {
            let var_name = &cap[1];
            if let Some(val) = self.variables.get(var_name) {
                result = result.replace(&format!("*{}*", var_name), &val.to_string());
            } else if let Some(val) = self.string_variables.get(var_name) {
                result = result.replace(&format!("*{}*", var_name), val);
            }
        }
        
        result
    }
    
    fn reset(&mut self) {
        self.variables.clear();
        self.string_variables.clear();
        self.output.clear();
        self.program_lines.clear();
        self.current_line = 0;
        self.labels.clear();
        self.gosub_stack.clear();
        self.for_stack.clear();
        self.match_flag = false;
        self.last_match_set = false;
        self.stored_condition = None;
    }
    
    // Stack operations for GOSUB/RETURN
    pub fn push_gosub(&mut self, line: usize) {
        self.gosub_stack.push(line);
    }
    
    pub fn pop_gosub(&mut self) -> Option<usize> {
        self.gosub_stack.pop()
    }
    
    // FOR/NEXT loop management
    pub fn push_for(&mut self, var: String, end_val: f64, step: f64, line: usize) {
        self.for_stack.push(ForContext {
            var_name: var,
            end_value: end_val,
            step,
            for_line: line,
        });
    }
    
    pub fn pop_for(&mut self) -> Option<ForContext> {
        self.for_stack.pop()
    }
    
    pub fn peek_for(&self) -> Option<&ForContext> {
        self.for_stack.last()
    }
    
    // Jump to label
    pub fn jump_to_label(&self, label: &str) -> Option<usize> {
        self.labels.get(label).copied()
    }
}

impl Default for Interpreter {
    fn default() -> Self {
        Self::new()
    }
}
