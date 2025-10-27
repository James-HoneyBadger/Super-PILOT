use crate::interpreter::{ExecutionResult, InterpreterError, TurtleState};
use std::collections::HashMap;

pub struct BasicExecutor {
    variables: HashMap<String, f64>,
    string_vars: HashMap<String, String>,
    program_lines: HashMap<i32, String>,
    current_line: i32,
    data_values: Vec<String>,
    data_index: usize,
}

impl BasicExecutor {
    pub fn new() -> Self {
        Self {
            variables: HashMap::new(),
            string_vars: HashMap::new(),
            program_lines: HashMap::new(),
            current_line: 0,
            data_values: Vec::new(),
            data_index: 0,
        }
    }

    pub fn load_program(&mut self, program: Vec<String>) {
        self.program_lines.clear();
        self.data_values.clear();
        self.data_index = 0;

        for line in program {
            let line = line.trim();
            if line.is_empty() {
                continue;
            }

            // Parse line number and command
            if let Some(space_pos) = line.find(' ') {
                if let Ok(line_num) = line[..space_pos].parse::<i32>() {
                    let command = line[space_pos + 1..].trim().to_string();
                    self.program_lines.insert(line_num, command.clone());

                    // Check for DATA statements
                    if command.to_uppercase().starts_with("DATA ") {
                        let data_part = &command[5..];
                        for value in data_part.split(',') {
                            self.data_values.push(value.trim().to_string());
                        }
                    }
                }
            }
        }

        // Find the lowest line number to start execution
        if let Some(&start_line) = self.program_lines.keys().min() {
            self.current_line = start_line;
        }
    }

    pub fn execute_command(&mut self, command: &str, turtle: &mut TurtleState) -> ExecutionResult {
        let command = command.trim().to_uppercase();

        if command.is_empty() {
            return ExecutionResult::Continue;
        }

        // Parse the command
        let parts: Vec<&str> = command.split_whitespace().collect();
        if parts.is_empty() {
            return ExecutionResult::Continue;
        }

        match parts[0] {
            "PRINT" | "PR" | "?" => self.handle_print(&command[parts[0].len()..]),
            "INPUT" => self.handle_input(&command[parts[0].len()..]),
            "LET" => self.handle_let(&command[parts[0].len()..]),
            "GOTO" => self.handle_goto(&command[parts[0].len()..]),
            "IF" => self.handle_if(&command[parts[0].len()..]),
            "FOR" => self.handle_for(&command[parts[0].len()..]),
            "NEXT" => self.handle_next(&command[parts[0].len()..]),
            "GOSUB" => self.handle_gosub(&command[parts[0].len()..]),
            "RETURN" => self.handle_return(),
            "READ" => self.handle_read(&command[parts[0].len()..]),
            "DATA" => ExecutionResult::Continue, // Already handled in load_program
            "REM" => ExecutionResult::Continue,  // Comment, ignore
            "END" => ExecutionResult::End,
            "STOP" => ExecutionResult::End,
            "CLS" => self.handle_cls(),
            "LOCATE" => self.handle_locate(&command[parts[0].len()..]),
            _ => {
                // Check if it's an assignment without LET
                if command.contains('=') {
                    self.handle_let(&command)
                } else {
                    ExecutionResult::Error(InterpreterError::InvalidCommand(format!(
                        "Unknown BASIC command: {}",
                        parts[0]
                    )))
                }
            }
        }
    }

    fn handle_print(&self, args: &str) -> ExecutionResult {
        let args = args.trim();
        if args.starts_with('"') && args.ends_with('"') {
            // String literal
            let text = &args[1..args.len() - 1];
            println!("{}", text);
        } else {
            // Expression or variable
            if let Ok(value) = self.evaluate_expression(args) {
                println!("{}", value);
            } else {
                println!("{}", args);
            }
        }
        ExecutionResult::Continue
    }

    fn handle_input(&mut self, args: &str) -> ExecutionResult {
        // In a real implementation, this would prompt for input
        // For now, simulate with default values
        let var_list: Vec<&str> = args.split(',').map(|s| s.trim()).collect();
        for var in var_list {
            if var.ends_with('$') {
                // String variable
                let var_name = &var[..var.len() - 1];
                self.string_vars
                    .insert(var_name.to_string(), "simulated_input".to_string());
            } else {
                // Numeric variable
                self.variables.insert(var.to_string(), 42.0); // Default value
            }
        }
        ExecutionResult::Continue
    }

    fn handle_let(&mut self, args: &str) -> ExecutionResult {
        if let Some(eq_pos) = args.find('=') {
            let var_part = args[..eq_pos].trim();
            let expr_part = args[eq_pos + 1..].trim();

            if var_part.ends_with('$') {
                // String assignment
                let var_name = &var_part[..var_part.len() - 1];
                let value = self.evaluate_string_expression(expr_part);
                self.string_vars.insert(var_name.to_string(), value);
            } else {
                // Numeric assignment
                if let Ok(value) = self.evaluate_expression(expr_part) {
                    self.variables.insert(var_part.to_string(), value);
                }
            }
        }
        ExecutionResult::Continue
    }

    fn handle_goto(&mut self, args: &str) -> ExecutionResult {
        if let Ok(line_num) = args.trim().parse::<i32>() {
            if self.program_lines.contains_key(&line_num) {
                self.current_line = line_num;
                ExecutionResult::Jump(line_num as usize)
            } else {
                ExecutionResult::Error(InterpreterError::InvalidLineNumber(line_num))
            }
        } else {
            ExecutionResult::Error(InterpreterError::InvalidCommand(
                "Invalid GOTO syntax".to_string(),
            ))
        }
    }

    fn handle_if(&mut self, args: &str) -> ExecutionResult {
        if let Some(then_pos) = args.to_uppercase().find(" THEN ") {
            let condition = args[..then_pos].trim();
            let then_part = args[then_pos + 6..].trim();

            if self.evaluate_condition(condition) {
                // Execute the THEN part
                if let Ok(line_num) = then_part.parse::<i32>() {
                    return self.handle_goto(&line_num.to_string());
                } else {
                    // Execute inline command
                    return self.execute_command(then_part, &mut TurtleState::new());
                }
            }
        }
        ExecutionResult::Continue
    }

    fn handle_for(&mut self, args: &str) -> ExecutionResult {
        // Simplified FOR loop implementation
        // In a real implementation, this would need a call stack
        ExecutionResult::Continue
    }

    fn handle_next(&mut self, args: &str) -> ExecutionResult {
        // Simplified NEXT implementation
        ExecutionResult::Continue
    }

    fn handle_gosub(&mut self, args: &str) -> ExecutionResult {
        // Simplified GOSUB implementation
        // Would need a return stack
        self.handle_goto(args)
    }

    fn handle_return(&mut self) -> ExecutionResult {
        // Simplified RETURN implementation
        ExecutionResult::Continue
    }

    fn handle_read(&mut self, args: &str) -> ExecutionResult {
        let var_list: Vec<&str> = args.split(',').map(|s| s.trim()).collect();
        for var in var_list {
            if self.data_index < self.data_values.len() {
                let value = &self.data_values[self.data_index];
                self.data_index += 1;

                if var.ends_with('$') {
                    let var_name = &var[..var.len() - 1];
                    self.string_vars.insert(var_name.to_string(), value.clone());
                } else {
                    if let Ok(num_value) = value.parse::<f64>() {
                        self.variables.insert(var.to_string(), num_value);
                    }
                }
            }
        }
        ExecutionResult::Continue
    }

    fn handle_cls(&self) -> ExecutionResult {
        // Clear screen - in real implementation would clear the output area
        println!("\x1B[2J\x1B[1;1H"); // ANSI clear screen
        ExecutionResult::Continue
    }

    fn handle_locate(&self, args: &str) -> ExecutionResult {
        // LOCATE row, col - position cursor
        // Simplified - just parse and acknowledge
        let coords: Vec<&str> = args.split(',').map(|s| s.trim()).collect();
        if coords.len() == 2 {
            if let (Ok(_row), Ok(_col)) = (coords[0].parse::<i32>(), coords[1].parse::<i32>()) {
                // In real implementation, would position cursor in output area
            }
        }
        ExecutionResult::Continue
    }

    fn evaluate_expression(&self, expr: &str) -> Result<f64, InterpreterError> {
        // Very basic expression evaluator
        let expr = expr.trim();

        // Handle simple cases
        if let Ok(value) = expr.parse::<f64>() {
            return Ok(value);
        }

        // Handle variables
        if let Some(&value) = self.variables.get(expr) {
            return Ok(value);
        }

        // Handle basic arithmetic
        if let Some(plus_pos) = expr.find('+') {
            let left = self.evaluate_expression(&expr[..plus_pos])?;
            let right = self.evaluate_expression(&expr[plus_pos + 1..])?;
            return Ok(left + right);
        }

        if let Some(minus_pos) = expr.find('-') {
            let left = self.evaluate_expression(&expr[..minus_pos])?;
            let right = self.evaluate_expression(&expr[minus_pos + 1..])?;
            return Ok(left - right);
        }

        if let Some(mult_pos) = expr.find('*') {
            let left = self.evaluate_expression(&expr[..mult_pos])?;
            let right = self.evaluate_expression(&expr[mult_pos + 1..])?;
            return Ok(left * right);
        }

        if let Some(div_pos) = expr.find('/') {
            let left = self.evaluate_expression(&expr[..div_pos])?;
            let right = self.evaluate_expression(&expr[div_pos + 1..])?;
            if right != 0.0 {
                return Ok(left / right);
            }
        }

        Err(InterpreterError::InvalidExpression(expr.to_string()))
    }

    fn evaluate_string_expression(&self, expr: &str) -> String {
        let expr = expr.trim();
        if expr.starts_with('"') && expr.ends_with('"') {
            expr[1..expr.len() - 1].to_string()
        } else if let Some(value) = self.string_vars.get(expr) {
            value.clone()
        } else {
            expr.to_string()
        }
    }

    fn evaluate_condition(&self, condition: &str) -> bool {
        // Very basic condition evaluator
        if let Some(eq_pos) = condition.find('=') {
            let left = condition[..eq_pos].trim();
            let right = condition[eq_pos + 1..].trim();

            if let (Ok(left_val), Ok(right_val)) = (
                self.evaluate_expression(left),
                self.evaluate_expression(right),
            ) {
                return (left_val - right_val).abs() < f64::EPSILON;
            }
        }

        if let Some(gt_pos) = condition.find('>') {
            let left = condition[..gt_pos].trim();
            let right = condition[gt_pos + 1..].trim();

            if let (Ok(left_val), Ok(right_val)) = (
                self.evaluate_expression(left),
                self.evaluate_expression(right),
            ) {
                return left_val > right_val;
            }
        }

        if let Some(lt_pos) = condition.find('<') {
            let left = condition[..lt_pos].trim();
            let right = condition[lt_pos + 1..].trim();

            if let (Ok(left_val), Ok(right_val)) = (
                self.evaluate_expression(left),
                self.evaluate_expression(right),
            ) {
                return left_val < right_val;
            }
        }

        false
    }

    pub fn get_variable(&self, name: &str) -> Option<f64> {
        self.variables.get(name).copied()
    }

    pub fn get_string_variable(&self, name: &str) -> Option<&String> {
        self.string_vars.get(name)
    }

    pub fn set_variable(&mut self, name: String, value: f64) {
        self.variables.insert(name, value);
    }

    pub fn set_string_variable(&mut self, name: String, value: String) {
        self.string_vars.insert(name, value);
    }
}
