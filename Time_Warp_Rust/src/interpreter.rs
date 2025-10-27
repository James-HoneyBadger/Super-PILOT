use crate::languages::{
    basic::BasicExecutor, javascript::JavaScriptExecutor, logo::LogoExecutor, perl::PerlExecutor,
    pilot::PilotExecutor, python::PythonExecutor,
};
use anyhow::{anyhow, Result};

#[derive(Clone, Debug)]
pub struct TurtleState {
    pub x: f32,
    pub y: f32,
    pub angle: f32, // in degrees
    pub pen_down: bool,
    pub pen_color: (u8, u8, u8),
    pub bg_color: (u8, u8, u8),
    pub visible: bool,
    pub pen_width: f32,
}

impl TurtleState {
    pub fn new() -> Self {
        Self {
            x: 0.0,
            y: 0.0,
            angle: 90.0, // Start facing up
            pen_down: true,
            pen_color: (0, 0, 0),      // Black
            bg_color: (255, 255, 255), // White
            visible: true,
            pen_width: 2.0,
        }
    }

    pub fn move_forward(&mut self, distance: f32) {
        let angle_rad = self.angle.to_radians();
        self.x += distance * angle_rad.cos();
        self.y += distance * angle_rad.sin();
    }

    pub fn turn_left(&mut self, angle: f32) {
        self.angle += angle;
    }

    pub fn turn_right(&mut self, angle: f32) {
        self.angle -= angle;
    }

    pub fn pen_up(&mut self) {
        self.pen_down = false;
    }

    pub fn pen_down(&mut self) {
        self.pen_down = true;
    }

    pub fn set_pen_color(&mut self, r: u8, g: u8, b: u8) {
        self.pen_color = (r, g, b);
    }

    pub fn set_bg_color(&mut self, r: u8, g: u8, b: u8) {
        self.bg_color = (r, g, b);
    }

    pub fn home(&mut self) {
        self.x = 0.0;
        self.y = 0.0;
        self.angle = 90.0;
    }

    pub fn clear_screen(&mut self) {
        self.home();
        self.pen_down = true;
        self.pen_color = (0, 0, 0);
        self.bg_color = (255, 255, 255);
    }

    pub fn show_turtle(&mut self) {
        self.visible = true;
    }

    pub fn hide_turtle(&mut self) {
        self.visible = false;
    }
}

impl Default for TurtleState {
    fn default() -> Self {
        Self::new()
    }
}

#[derive(Debug)]
pub enum ExecutionResult {
    Continue,
    Jump(usize),
    End,
    Error(InterpreterError),
}

#[derive(Debug)]
pub enum InterpreterError {
    InvalidCommand(String),
    InvalidLabel(String),
    InvalidLineNumber(i32),
    InvalidExpression(String),
    DivisionByZero,
}

#[derive(Debug, Clone, PartialEq)]
pub enum Language {
    Pilot,
    Basic,
    Logo,
    Python,
    JavaScript,
    Perl,
}

pub struct TimeWarpInterpreter {
    current_language: Language,
    pilot_executor: PilotExecutor,
    basic_executor: BasicExecutor,
    logo_executor: LogoExecutor,
    python_executor: PythonExecutor,
    javascript_executor: JavaScriptExecutor,
    perl_executor: PerlExecutor,
    turtle_state: TurtleState,
    output: Vec<String>,
}

impl TimeWarpInterpreter {
    pub fn new() -> Self {
        Self {
            current_language: Language::Pilot,
            pilot_executor: PilotExecutor::new(),
            basic_executor: BasicExecutor::new(),
            logo_executor: LogoExecutor::new(),
            python_executor: PythonExecutor::new(),
            javascript_executor: JavaScriptExecutor::new(),
            perl_executor: PerlExecutor::new(),
            turtle_state: TurtleState::new(),
            output: Vec::new(),
        }
    }

    pub fn set_language(&mut self, language: Language) {
        self.current_language = language;
    }

    pub fn load_program(&mut self, program: &Vec<String>) {
        match self.current_language {
            Language::Pilot => self.pilot_executor.load_program(program.clone()),
            Language::Basic => self.basic_executor.load_program(program.clone()),
            Language::Logo => self.logo_executor.load_program(program.clone()),
            Language::Python => self.python_executor.load_program(program.clone()),
            Language::JavaScript => self.javascript_executor.load_program(program.clone()),
            Language::Perl => self.perl_executor.load_program(program.clone()),
        }
    }

    pub fn execute_command(&mut self, command: &str) -> ExecutionResult {
        match self.current_language {
            Language::Pilot => self
                .pilot_executor
                .execute_command(command, &mut self.turtle_state),
            Language::Basic => self
                .basic_executor
                .execute_command(command, &mut self.turtle_state),
            Language::Logo => self
                .logo_executor
                .execute_command(command, &mut self.turtle_state),
            Language::Python => self
                .python_executor
                .execute_command(command, &mut self.turtle_state),
            Language::JavaScript => self
                .javascript_executor
                .execute_command(command, &mut self.turtle_state),
            Language::Perl => self
                .perl_executor
                .execute_command(command, &mut self.turtle_state),
        }
    }

    pub fn execute_program(&mut self, program: Vec<String>) -> Result<Vec<String>> {
        self.load_program(&program);
        self.output.clear();

        let mut line_index = 0;
        while line_index < program.len() {
            let command = &program[line_index];
            match self.execute_command(command) {
                ExecutionResult::Continue => {
                    line_index += 1;
                }
                ExecutionResult::Jump(target) => {
                    line_index = target;
                }
                ExecutionResult::End => {
                    break;
                }
                ExecutionResult::Error(e) => {
                    return Err(anyhow!("Execution error: {:?}", e));
                }
            }
        }

        Ok(self.output.clone())
    }

    pub fn get_turtle_state(&self) -> &TurtleState {
        &self.turtle_state
    }

    pub fn get_output(&self) -> &[String] {
        &self.output
    }

    pub fn add_output(&mut self, text: String) {
        self.output.push(text);
    }

    // Variable access methods for different languages
    pub fn get_pilot_variable(&self, name: &str) -> Option<&String> {
        self.pilot_executor.get_variable(name)
    }

    pub fn get_basic_variable(&self, name: &str) -> Option<f64> {
        self.basic_executor.get_variable(name)
    }

    pub fn get_basic_string_variable(&self, name: &str) -> Option<&String> {
        self.basic_executor.get_string_variable(name)
    }

    pub fn get_logo_variable(&self, name: &str) -> Option<f64> {
        self.logo_executor.get_variable(name)
    }

    pub fn set_pilot_variable(&mut self, name: String, value: String) {
        self.pilot_executor.set_variable(name, value);
    }

    pub fn set_basic_variable(&mut self, name: String, value: f64) {
        self.basic_executor.set_variable(name, value);
    }

    pub fn set_basic_string_variable(&mut self, name: String, value: String) {
        self.basic_executor.set_string_variable(name, value);
    }

    pub fn set_logo_variable(&mut self, name: String, value: f64) {
        self.logo_executor.set_variable(name, value);
    }
}
