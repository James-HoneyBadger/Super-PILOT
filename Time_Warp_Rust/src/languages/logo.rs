use crate::interpreter::{ExecutionResult, InterpreterError, TurtleState};
use std::collections::HashMap;

pub struct LogoExecutor {
    variables: HashMap<String, f64>,
    procedures: HashMap<String, Vec<String>>,
    call_stack: Vec<(String, usize)>, // procedure name and instruction pointer
    current_procedure: Option<String>,
    instruction_pointer: usize,
}

impl LogoExecutor {
    pub fn new() -> Self {
        Self {
            variables: HashMap::new(),
            procedures: HashMap::new(),
            call_stack: Vec::new(),
            current_procedure: None,
            instruction_pointer: 0,
        }
    }

    pub fn load_program(&mut self, program: Vec<String>) {
        self.procedures.clear();
        let mut current_proc = None;
        let mut proc_lines = Vec::new();

        for line in program {
            let line = line.trim().to_uppercase();

            if line.starts_with("TO ") {
                // Start of procedure definition
                if let Some(proc_name) = current_proc.take() {
                    self.procedures.insert(proc_name, proc_lines);
                    proc_lines = Vec::new();
                }
                let proc_part = &line[3..];
                if let Some(end_pos) = proc_part.find(' ') {
                    current_proc = Some(proc_part[..end_pos].to_string());
                    proc_lines = Vec::new();
                }
            } else if line == "END" {
                // End of procedure definition
                if let Some(proc_name) = current_proc.take() {
                    self.procedures.insert(proc_name, proc_lines);
                    proc_lines = Vec::new();
                }
                proc_lines = Vec::new();
            } else if current_proc.is_some() {
                // Inside procedure
                proc_lines.push(line);
            } else {
                // Main program line
                if !line.is_empty() {
                    let main_proc = self
                        .procedures
                        .entry("MAIN".to_string())
                        .or_insert(Vec::new());
                    main_proc.push(line);
                }
            }
        }

        // Handle any remaining procedure
        if let Some(proc_name) = current_proc {
            self.procedures.insert(proc_name, proc_lines);
        }
    }

    pub fn execute_command(&mut self, command: &str, turtle: &mut TurtleState) -> ExecutionResult {
        let command = command.trim().to_uppercase();

        if command.is_empty() {
            return ExecutionResult::Continue;
        }

        let parts: Vec<&str> = command.split_whitespace().collect();
        if parts.is_empty() {
            return ExecutionResult::Continue;
        }

        match parts[0] {
            "FORWARD" | "FD" => self.handle_forward(&parts[1..], turtle),
            "BACK" | "BK" => self.handle_back(&parts[1..], turtle),
            "LEFT" | "LT" => self.handle_left(&parts[1..], turtle),
            "RIGHT" | "RT" => self.handle_right(&parts[1..], turtle),
            "PENUP" | "PU" => self.handle_penup(turtle),
            "PENDOWN" | "PD" => self.handle_pendown(turtle),
            "SETPENCOLOR" | "SETPC" => self.handle_setpencolor(&parts[1..], turtle),
            "SETBG" | "SETBACKGROUND" => self.handle_setbg(&parts[1..], turtle),
            "HOME" => self.handle_home(turtle),
            "CLEARSCREEN" | "CS" => self.handle_clearscreen(turtle),
            "SHOWTURTLE" | "ST" => self.handle_showturtle(turtle),
            "HIDETURTLE" | "HT" => self.handle_hideturtle(turtle),
            "MAKE" => self.handle_make(&parts[1..]),
            "PRINT" | "PR" => self.handle_print(&parts[1..]),
            "IF" => self.handle_if(&parts[1..], turtle),
            "REPEAT" => self.handle_repeat(&parts[1..], turtle),
            "TO" => ExecutionResult::Continue, // Procedure definition, already handled
            "END" => ExecutionResult::Continue, // Procedure end, already handled
            _ => {
                // Check if it's a procedure call
                if let Some(proc_lines) = self.procedures.get(parts[0]) {
                    return self.call_procedure(parts[0], &parts[1..], proc_lines.clone(), turtle);
                } else {
                    ExecutionResult::Error(InterpreterError::InvalidCommand(format!(
                        "Unknown Logo command: {}",
                        parts[0]
                    )))
                }
            }
        }
    }

    fn handle_forward(&self, args: &[&str], turtle: &mut TurtleState) -> ExecutionResult {
        if let Some(distance_str) = args.first() {
            if let Ok(distance) = self.evaluate_expression(distance_str) {
                turtle.move_forward(distance as f32);
            }
        }
        ExecutionResult::Continue
    }

    fn handle_back(&self, args: &[&str], turtle: &mut TurtleState) -> ExecutionResult {
        if let Some(distance_str) = args.first() {
            if let Ok(distance) = self.evaluate_expression(distance_str) {
                turtle.move_forward(-(distance as f32));
            }
        }
        ExecutionResult::Continue
    }

    fn handle_left(&self, args: &[&str], turtle: &mut TurtleState) -> ExecutionResult {
        if let Some(angle_str) = args.first() {
            if let Ok(angle) = self.evaluate_expression(angle_str) {
                turtle.turn_left(angle as f32);
            }
        }
        ExecutionResult::Continue
    }

    fn handle_right(&self, args: &[&str], turtle: &mut TurtleState) -> ExecutionResult {
        if let Some(angle_str) = args.first() {
            if let Ok(angle) = self.evaluate_expression(angle_str) {
                turtle.turn_right(angle as f32);
            }
        }
        ExecutionResult::Continue
    }

    fn handle_penup(&mut self, turtle: &mut TurtleState) -> ExecutionResult {
        turtle.pen_up();
        ExecutionResult::Continue
    }

    fn handle_pendown(&mut self, turtle: &mut TurtleState) -> ExecutionResult {
        turtle.pen_down();
        ExecutionResult::Continue
    }

    fn handle_setpencolor(&mut self, args: &[&str], turtle: &mut TurtleState) -> ExecutionResult {
        if args.len() >= 3 {
            if let (Ok(r), Ok(g), Ok(b)) = (
                self.evaluate_expression(args[0]),
                self.evaluate_expression(args[1]),
                self.evaluate_expression(args[2]),
            ) {
                turtle.set_pen_color(r as u8, g as u8, b as u8);
            }
        }
        ExecutionResult::Continue
    }

    fn handle_setbg(&mut self, args: &[&str], turtle: &mut TurtleState) -> ExecutionResult {
        if args.len() >= 3 {
            if let (Ok(r), Ok(g), Ok(b)) = (
                self.evaluate_expression(args[0]),
                self.evaluate_expression(args[1]),
                self.evaluate_expression(args[2]),
            ) {
                turtle.set_bg_color(r as u8, g as u8, b as u8);
            }
        }
        ExecutionResult::Continue
    }

    fn handle_home(&mut self, turtle: &mut TurtleState) -> ExecutionResult {
        turtle.home();
        ExecutionResult::Continue
    }

    fn handle_clearscreen(&mut self, turtle: &mut TurtleState) -> ExecutionResult {
        turtle.clear_screen();
        ExecutionResult::Continue
    }

    fn handle_showturtle(&mut self, turtle: &mut TurtleState) -> ExecutionResult {
        turtle.show_turtle();
        ExecutionResult::Continue
    }

    fn handle_hideturtle(&mut self, turtle: &mut TurtleState) -> ExecutionResult {
        turtle.hide_turtle();
        ExecutionResult::Continue
    }

    fn handle_make(&mut self, args: &[&str]) -> ExecutionResult {
        if args.len() >= 2 {
            let var_name = args[0].trim_start_matches('"').trim_end_matches('"');
            let value_str = args[1..].join(" ");
            if let Ok(value) = self.evaluate_expression(&value_str) {
                self.variables.insert(var_name.to_string(), value);
            }
        }
        ExecutionResult::Continue
    }

    fn handle_print(&self, args: &[&str]) -> ExecutionResult {
        let text = args.join(" ");
        if let Ok(value) = self.evaluate_expression(&text) {
            println!("{}", value);
        } else {
            println!("{}", text);
        }
        ExecutionResult::Continue
    }

    fn handle_if(&mut self, args: &[&str], turtle: &mut TurtleState) -> ExecutionResult {
        if args.len() >= 2 {
            let condition = args[0];
            let then_commands = &args[1..];

            if self.evaluate_condition(condition) {
                // Execute the THEN commands inline
                for cmd in then_commands {
                    match self.execute_command(cmd, turtle) {
                        ExecutionResult::Continue => continue,
                        ExecutionResult::End => return ExecutionResult::End,
                        ExecutionResult::Jump(line) => return ExecutionResult::Jump(line),
                        ExecutionResult::Error(e) => return ExecutionResult::Error(e),
                    }
                }
            }
        }
        ExecutionResult::Continue
    }

    fn handle_repeat(&mut self, args: &[&str], turtle: &mut TurtleState) -> ExecutionResult {
        if args.len() >= 2 {
            if let Ok(count) = self.evaluate_expression(args[0]) {
                let commands = &args[1..];
                for _ in 0..count as i32 {
                    for cmd in commands {
                        match self.execute_command(cmd, turtle) {
                            ExecutionResult::Continue => continue,
                            ExecutionResult::End => return ExecutionResult::End,
                            ExecutionResult::Jump(line) => return ExecutionResult::Jump(line),
                            ExecutionResult::Error(e) => return ExecutionResult::Error(e),
                        }
                    }
                }
            }
        }
        ExecutionResult::Continue
    }

    fn call_procedure(
        &mut self,
        name: &str,
        args: &[&str],
        proc_lines: Vec<String>,
        turtle: &mut TurtleState,
    ) -> ExecutionResult {
        // Save current state
        let current_proc = self.current_procedure.clone();
        let current_ip = self.instruction_pointer;

        self.call_stack
            .push((current_proc.unwrap_or_default(), current_ip));
        self.current_procedure = Some(name.to_string());
        self.instruction_pointer = 0;

        // Execute procedure lines
        while self.instruction_pointer < proc_lines.len() {
            let line = &proc_lines[self.instruction_pointer];
            self.instruction_pointer += 1;

            match self.execute_command(line, turtle) {
                ExecutionResult::Continue => continue,
                ExecutionResult::End => break,
                ExecutionResult::Jump(line_num) => {
                    self.instruction_pointer = line_num;
                }
                ExecutionResult::Error(e) => return ExecutionResult::Error(e),
            }
        }

        // Restore state
        if let Some((proc, ip)) = self.call_stack.pop() {
            self.current_procedure = if proc.is_empty() { None } else { Some(proc) };
            self.instruction_pointer = ip;
        }

        ExecutionResult::Continue
    }

    fn evaluate_expression(&self, expr: &str) -> Result<f64, InterpreterError> {
        let expr = expr.trim();

        // Handle numbers
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

        if let Some(minus_pos) = expr.rfind('-') {
            // Use rfind to handle negative numbers
            if minus_pos > 0 {
                let left = self.evaluate_expression(&expr[..minus_pos])?;
                let right = self.evaluate_expression(&expr[minus_pos + 1..])?;
                return Ok(left - right);
            }
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

    fn evaluate_condition(&self, condition: &str) -> bool {
        // Very basic condition evaluation
        if let Some(eq_pos) = condition.find('=') {
            let left = &condition[..eq_pos];
            let right = &condition[eq_pos + 1..];

            if let (Ok(left_val), Ok(right_val)) = (
                self.evaluate_expression(left),
                self.evaluate_expression(right),
            ) {
                return (left_val - right_val).abs() < f64::EPSILON;
            }
        }

        if let Some(gt_pos) = condition.find('>') {
            let left = &condition[..gt_pos];
            let right = &condition[gt_pos + 1..];

            if let (Ok(left_val), Ok(right_val)) = (
                self.evaluate_expression(left),
                self.evaluate_expression(right),
            ) {
                return left_val > right_val;
            }
        }

        if let Some(lt_pos) = condition.find('<') {
            let left = &condition[..lt_pos];
            let right = &condition[lt_pos + 1..];

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

    pub fn set_variable(&mut self, name: String, value: f64) {
        self.variables.insert(name, value);
    }
}
