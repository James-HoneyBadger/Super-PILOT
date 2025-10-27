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
    "LEFT" | "LT" => execute_left(interp, turtle, parts.get(1).unwrap_or(&"0")),
    "RIGHT" | "RT" => execute_right(interp, turtle, parts.get(1).unwrap_or(&"0")),
        "PENUP" | "PU" => execute_penup(turtle),
        "PENDOWN" | "PD" => execute_pendown(turtle),
    "CLEARSCREEN" | "CS" => execute_clearscreen(turtle),
        "HOME" => execute_home(turtle),
        "SETXY" => execute_setxy(interp, turtle, parts.get(1).unwrap_or(&"")),
        "SETHEADING" | "SETH" => execute_setheading(interp, turtle, parts.get(1).unwrap_or(&"0")),
    "SETCOLOR" | "SETPENCOLOR" => execute_setcolor(interp, turtle, parts.get(1).unwrap_or(&"")),
    "PENWIDTH" | "SETPENSIZE" => execute_penwidth(interp, turtle, parts.get(1).unwrap_or(&"")),
    "SETBGCOLOR" => execute_setbgcolor(interp, turtle, parts.get(1).unwrap_or(&"")),
        "HIDETURTLE" | "HT" => execute_hideturtle(turtle),
        "SHOWTURTLE" | "ST" => execute_showturtle(turtle),
    "REPEAT" => execute_repeat(interp, parts.get(1).unwrap_or(&""), turtle),
        "TO" => execute_to(interp, parts.get(1).unwrap_or(&"")),
        "END" => Ok(ExecutionResult::Continue), // END handled in execute_to
        _ => {
            // Check if command is a stored procedure name
            let proc_upper = parts[0].to_uppercase();
            if interp.logo_procedures.contains_key(&proc_upper) {
                execute_procedure(interp, &proc_upper, turtle)
            } else {
                interp.log_output(format!("Unknown Logo command: {}", parts[0]));
                Ok(ExecutionResult::Continue)
            }
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

fn execute_left(interp: &mut Interpreter, turtle: &mut TurtleState, angle_str: &str) -> Result<ExecutionResult> {
    let angle = interp.evaluate_expression(angle_str.trim())? as f32;
    turtle.left(angle);
    Ok(ExecutionResult::Continue)
}

fn execute_right(interp: &mut Interpreter, turtle: &mut TurtleState, angle_str: &str) -> Result<ExecutionResult> {
    let angle = interp.evaluate_expression(angle_str.trim())? as f32;
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
    turtle.home();
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

fn execute_setcolor(interp: &mut Interpreter, turtle: &mut TurtleState, args: &str) -> Result<ExecutionResult> {
    // SETCOLOR accepts: r g b (0-255), named color (RED, BLUE), or hex (#RRGGBB, #RGB)
    let trimmed = args.trim();
    let parts: Vec<&str> = trimmed.split_whitespace().collect();
    
    if parts.len() == 1 {
        let arg = parts[0].to_uppercase();
        // Check named color
        if let Some(color) = parse_named_color(&arg) {
            turtle.pen_color = color;
            return Ok(ExecutionResult::Continue);
        }
        // Check hex color
        if trimmed.starts_with('#') {
            if let Some(color) = parse_hex_color(trimmed) {
                turtle.pen_color = color;
                return Ok(ExecutionResult::Continue);
            }
        }
    } else if parts.len() >= 3 {
        // RGB values
        let r = interp.evaluate_expression(parts[0])?.clamp(0.0, 255.0) as u8;
        let g = interp.evaluate_expression(parts[1])?.clamp(0.0, 255.0) as u8;
        let b = interp.evaluate_expression(parts[2])?.clamp(0.0, 255.0) as u8;
        turtle.pen_color = egui::Color32::from_rgb(r, g, b);
    }
    Ok(ExecutionResult::Continue)
}

fn execute_penwidth(interp: &mut Interpreter, turtle: &mut TurtleState, arg: &str) -> Result<ExecutionResult> {
    let w = interp.evaluate_expression(arg.trim())?.max(0.1) as f32;
    turtle.pen_width = w;
    Ok(ExecutionResult::Continue)
}

fn execute_setbgcolor(interp: &mut Interpreter, turtle: &mut TurtleState, args: &str) -> Result<ExecutionResult> {
    let trimmed = args.trim();
    let parts: Vec<&str> = trimmed.split_whitespace().collect();
    
    if parts.len() == 1 {
        let arg = parts[0].to_uppercase();
        if let Some(color) = parse_named_color(&arg) {
            turtle.bg_color = color;
            return Ok(ExecutionResult::Continue);
        }
        if trimmed.starts_with('#') {
            if let Some(color) = parse_hex_color(trimmed) {
                turtle.bg_color = color;
                return Ok(ExecutionResult::Continue);
            }
        }
    } else if parts.len() >= 3 {
        let r = interp.evaluate_expression(parts[0])?.clamp(0.0, 255.0) as u8;
        let g = interp.evaluate_expression(parts[1])?.clamp(0.0, 255.0) as u8;
        let b = interp.evaluate_expression(parts[2])?.clamp(0.0, 255.0) as u8;
        turtle.bg_color = egui::Color32::from_rgb(r, g, b);
    }
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

fn execute_repeat(interp: &mut Interpreter, params: &str, turtle: &mut TurtleState) -> Result<ExecutionResult> {
    // REPEAT n [commands]
    // Parse: REPEAT 4 [FORWARD 50 RIGHT 90]
    let params = params.trim();
    
    // Find count and bracket section
    let bracket_start = params.find('[').ok_or_else(|| anyhow::anyhow!("REPEAT missing '['"))?;
    let bracket_end = params.rfind(']').ok_or_else(|| anyhow::anyhow!("REPEAT missing ']'"))?;
    
    let count_str = params[..bracket_start].trim();
    let commands = params[bracket_start + 1..bracket_end].trim();
    
    let count = interp.evaluate_expression(count_str)? as usize;
    
    // Execute commands count times using same turtle
    for _ in 0..count {
        // Execute each command in sequence
        for cmd in commands.split_whitespace().collect::<Vec<_>>().chunks(2) {
            if cmd.len() >= 2 {
                let full_cmd = format!("{} {}", cmd[0], cmd[1]);
                execute(interp, &full_cmd, turtle)?;
            } else if cmd.len() == 1 {
                execute(interp, cmd[0], turtle)?;
            }
        }
    }
    
    Ok(ExecutionResult::Continue)
}

fn execute_to(interp: &mut Interpreter, name: &str) -> Result<ExecutionResult> {
    // TO <name>: collect subsequent lines until END into procedure
    let proc_name = name.trim().to_uppercase();
    if proc_name.is_empty() {
        return Err(anyhow::anyhow!("TO missing procedure name"));
    }
    
    let mut body: Vec<String> = Vec::new();
    let start_line = interp.current_line + 1;
    
    // Collect lines until END (skip TO line itself)
    for idx in start_line..interp.program_lines.len() {
        let (_, line) = &interp.program_lines[idx];
        let upper = line.trim().to_uppercase();
        if upper == "END" {
            // Store procedure and jump past END
            interp.logo_procedures.insert(proc_name.clone(), body);
            interp.current_line = idx;
            return Ok(ExecutionResult::Continue);
        }
        body.push(line.clone());
    }
    
    Err(anyhow::anyhow!("TO {} missing END", proc_name))
}

fn execute_procedure(interp: &mut Interpreter, name: &str, turtle: &mut TurtleState) -> Result<ExecutionResult> {
    // Execute stored procedure body
    if let Some(body) = interp.logo_procedures.get(name).cloned() {
        for line in body {
            execute(interp, &line, turtle)?;
        }
        Ok(ExecutionResult::Continue)
    } else {
        Err(anyhow::anyhow!("Procedure {} not found", name))
    }
}

fn parse_named_color(name: &str) -> Option<egui::Color32> {
    match name {
        "BLACK" => Some(egui::Color32::BLACK),
        "WHITE" => Some(egui::Color32::WHITE),
        "RED" => Some(egui::Color32::from_rgb(255, 0, 0)),
        "GREEN" => Some(egui::Color32::from_rgb(0, 255, 0)),
        "BLUE" => Some(egui::Color32::from_rgb(0, 0, 255)),
        "YELLOW" => Some(egui::Color32::from_rgb(255, 255, 0)),
        "CYAN" => Some(egui::Color32::from_rgb(0, 255, 255)),
        "MAGENTA" => Some(egui::Color32::from_rgb(255, 0, 255)),
        "ORANGE" => Some(egui::Color32::from_rgb(255, 165, 0)),
        "PURPLE" => Some(egui::Color32::from_rgb(128, 0, 128)),
        "PINK" => Some(egui::Color32::from_rgb(255, 192, 203)),
        "BROWN" => Some(egui::Color32::from_rgb(165, 42, 42)),
        "GRAY" | "GREY" => Some(egui::Color32::GRAY),
        _ => None,
    }
}

fn parse_hex_color(hex: &str) -> Option<egui::Color32> {
    let hex = hex.trim_start_matches('#');
    
    if hex.len() == 6 {
        // #RRGGBB
        let r = u8::from_str_radix(&hex[0..2], 16).ok()?;
        let g = u8::from_str_radix(&hex[2..4], 16).ok()?;
        let b = u8::from_str_radix(&hex[4..6], 16).ok()?;
        Some(egui::Color32::from_rgb(r, g, b))
    } else if hex.len() == 3 {
        // #RGB -> #RRGGBB
        let r = u8::from_str_radix(&hex[0..1].repeat(2), 16).ok()?;
        let g = u8::from_str_radix(&hex[1..2].repeat(2), 16).ok()?;
        let b = u8::from_str_radix(&hex[2..3].repeat(2), 16).ok()?;
        Some(egui::Color32::from_rgb(r, g, b))
    } else {
        None
    }
}

