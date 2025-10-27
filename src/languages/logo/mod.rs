use anyhow::Result;
use crate::interpreter::{Interpreter, ExecutionResult};
use crate::graphics::TurtleState;

pub fn execute(interp: &mut Interpreter, command: &str, turtle: &mut TurtleState) -> Result<ExecutionResult> {
    let cmd = command.trim().to_uppercase();
    let parts: Vec<&str> = cmd.splitn(2, char::is_whitespace).collect();
    
    if parts.is_empty() {
        return Ok(ExecutionResult::Continue);
    }
    
    match parts[0] {
        "FORWARD" | "FD" => execute_forward(interp, turtle, parts.get(1).unwrap_or(&"0")),
        "BACK" | "BK" | "BACKWARD" => execute_back(interp, turtle, parts.get(1).unwrap_or(&"0")),
        "LEFT" | "LT" => execute_left(turtle, parts.get(1).unwrap_or(&"0")),
        "RIGHT" | "RT" => execute_right(turtle, parts.get(1).unwrap_or(&"0")),
        "PENUP" | "PU" => execute_penup(turtle),
        "PENDOWN" | "PD" => execute_pendown(turtle),
        "CLEARSCREEN" | "CS" => execute_clearscreen(turtle),
        "HOME" => execute_home(turtle),
        "SETXY" => execute_setxy(interp, turtle, parts.get(1).unwrap_or(&"")),
        "SETHEADING" | "SETH" => execute_setheading(interp, turtle, parts.get(1).unwrap_or(&"0")),
        "HIDETURTLE" | "HT" => execute_hideturtle(turtle),
        "SHOWTURTLE" | "ST" => execute_showturtle(turtle),
        "REPEAT" => execute_repeat(interp, parts.get(1).unwrap_or(&"")),
        _ => {
            interp.log_output(format!("Unknown Logo command: {}", parts[0]));
            Ok(ExecutionResult::Continue)
        }
    }
}

fn execute_forward(interp: &mut Interpreter, turtle: &mut TurtleState, distance_str: &str) -> Result<ExecutionResult> {
    let distance = interp.evaluate_expression(distance_str.trim())?;
    turtle.forward(distance as f32);
    Ok(ExecutionResult::Continue)
}

fn execute_back(interp: &mut Interpreter, turtle: &mut TurtleState, distance_str: &str) -> Result<ExecutionResult> {
    let distance = interp.evaluate_expression(distance_str.trim())?;
    turtle.back(distance as f32);
    Ok(ExecutionResult::Continue)
}

fn execute_left(turtle: &mut TurtleState, angle_str: &str) -> Result<ExecutionResult> {
    let angle = angle_str.trim().parse::<f32>()?;
    turtle.left(angle);
    Ok(ExecutionResult::Continue)
}

fn execute_right(turtle: &mut TurtleState, angle_str: &str) -> Result<ExecutionResult> {
    let angle = angle_str.trim().parse::<f32>()?;
    turtle.right(angle);
    Ok(ExecutionResult::Continue)
}

fn execute_penup(turtle: &mut TurtleState) -> Result<ExecutionResult> {
    turtle.pen_down = false;
    Ok(ExecutionResult::Continue)
}

fn execute_pendown(turtle: &mut TurtleState) -> Result<ExecutionResult> {
    turtle.pen_down = true;
    Ok(ExecutionResult::Continue)
}

fn execute_clearscreen(turtle: &mut TurtleState) -> Result<ExecutionResult> {
    turtle.clear();
    Ok(ExecutionResult::Continue)
}

fn execute_home(turtle: &mut TurtleState) -> Result<ExecutionResult> {
    turtle.home();
    Ok(ExecutionResult::Continue)
}

fn execute_setxy(interp: &mut Interpreter, turtle: &mut TurtleState, coords: &str) -> Result<ExecutionResult> {
    let parts: Vec<&str> = coords.split_whitespace().collect();
    if parts.len() >= 2 {
        let x = interp.evaluate_expression(parts[0])? as f32;
        let y = interp.evaluate_expression(parts[1])? as f32;
        turtle.goto(x, y);
    }
    Ok(ExecutionResult::Continue)
}

fn execute_setheading(interp: &mut Interpreter, turtle: &mut TurtleState, angle_str: &str) -> Result<ExecutionResult> {
    let angle = interp.evaluate_expression(angle_str.trim())? as f32;
    turtle.heading = angle;
    Ok(ExecutionResult::Continue)
}

fn execute_hideturtle(turtle: &mut TurtleState) -> Result<ExecutionResult> {
    turtle.visible = false;
    Ok(ExecutionResult::Continue)
}

fn execute_showturtle(turtle: &mut TurtleState) -> Result<ExecutionResult> {
    turtle.visible = true;
    Ok(ExecutionResult::Continue)
}

fn execute_repeat(interp: &mut Interpreter, params: &str) -> Result<ExecutionResult> {
    // REPEAT n [commands]
    // Parse: REPEAT 4 [FORWARD 50 RIGHT 90]
    let params = params.trim();
    
    // Find count and bracket section
    let bracket_start = params.find('[').ok_or_else(|| anyhow::anyhow!("REPEAT missing '['"))?;
    let bracket_end = params.rfind(']').ok_or_else(|| anyhow::anyhow!("REPEAT missing ']'"))?;
    
    let count_str = params[..bracket_start].trim();
    let commands = params[bracket_start + 1..bracket_end].trim();
    
    let count = interp.evaluate_expression(count_str)? as usize;
    
    // Store commands in output for visibility (educational IDE feature)
    interp.log_output(format!("REPEAT {} [{}]", count, commands));
    
    // For now, REPEAT expands commands inline (simple implementation)
    // Future: Add RepeatContext stack for nested repeats and multi-line support
    for _ in 0..count {
        // Execute each command in sequence
        for cmd in commands.split_whitespace().collect::<Vec<_>>().chunks(2) {
            if cmd.len() >= 2 {
                let full_cmd = format!("{} {}", cmd[0], cmd[1]);
                // Recursively execute through logo module
                let mut turtle = crate::graphics::TurtleState::default();
                execute(interp, &full_cmd, &mut turtle)?;
            } else if cmd.len() == 1 {
                let mut turtle = crate::graphics::TurtleState::default();
                execute(interp, cmd[0], &mut turtle)?;
            }
        }
    }
    
    Ok(ExecutionResult::Continue)
}
