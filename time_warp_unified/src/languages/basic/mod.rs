use anyhow::Result;
use crate::interpreter::{Interpreter, ExecutionResult};
use crate::graphics::TurtleState;

pub fn execute(interp: &mut Interpreter, command: &str, _turtle: &mut TurtleState) -> Result<ExecutionResult> {
    let cmd = command.trim().to_uppercase();
    let parts: Vec<&str> = cmd.splitn(2, char::is_whitespace).collect();
    
    if parts.is_empty() {
        return Ok(ExecutionResult::Continue);
    }
    
    match parts[0] {
        "PRINT" => execute_print(interp, parts.get(1).unwrap_or(&"")),
        "LET" => execute_let(interp, parts.get(1).unwrap_or(&"")),
        "INPUT" => execute_input(interp, parts.get(1).unwrap_or(&"")),
        "GOTO" => execute_goto(interp, parts.get(1).unwrap_or(&"")),
        "IF" => execute_if(interp, parts.get(1).unwrap_or(&"")),
        "FOR" => execute_for(interp, parts.get(1).unwrap_or(&"")),
        "NEXT" => execute_next(interp, parts.get(1).unwrap_or(&"")),
        "GOSUB" => execute_gosub(interp, parts.get(1).unwrap_or(&"")),
        "RETURN" => execute_return(interp),
        "REM" => Ok(ExecutionResult::Continue), // Comment
        "END" => Ok(ExecutionResult::End),
        _ => {
            interp.log_output(format!("Unknown BASIC command: {}", parts[0]));
            Ok(ExecutionResult::Continue)
        }
    }
}

fn execute_print(interp: &mut Interpreter, args: &str) -> Result<ExecutionResult> {
    let output = interp.interpolate_text(args);
    interp.log_output(output);
    Ok(ExecutionResult::Continue)
}

fn execute_let(interp: &mut Interpreter, assignment: &str) -> Result<ExecutionResult> {
    if let Some(pos) = assignment.find('=') {
        let var_name = assignment[..pos].trim().to_string();
        let expr = assignment[pos + 1..].trim();
        
        match interp.evaluate_expression(expr) {
            Ok(value) => {
                interp.variables.insert(var_name, value);
            }
            Err(_) => {
                interp.string_variables.insert(var_name, expr.to_string());
            }
        }
    }
    
    Ok(ExecutionResult::Continue)
}

fn execute_input(interp: &mut Interpreter, var: &str) -> Result<ExecutionResult> {
    // TODO: Implement input handling
    interp.log_output(format!("INPUT {} (not yet implemented)", var));
    Ok(ExecutionResult::Continue)
}

fn execute_goto(interp: &mut Interpreter, line_num: &str) -> Result<ExecutionResult> {
    if let Ok(num) = line_num.trim().parse::<usize>() {
        // Find line with this number
        // TODO: Implement line number lookup
        interp.log_output(format!("GOTO {} (not yet implemented)", num));
    }
    Ok(ExecutionResult::Continue)
}

fn execute_if(interp: &mut Interpreter, condition: &str) -> Result<ExecutionResult> {
    // IF condition THEN command
    // TODO: Implement IF...THEN
    interp.log_output(format!("IF {} (not yet implemented)", condition));
    Ok(ExecutionResult::Continue)
}

fn execute_for(interp: &mut Interpreter, params: &str) -> Result<ExecutionResult> {
    // FOR var = start TO end [STEP step]
    // TODO: Implement FOR loop
    interp.log_output(format!("FOR {} (not yet implemented)", params));
    Ok(ExecutionResult::Continue)
}

fn execute_next(interp: &mut Interpreter, var: &str) -> Result<ExecutionResult> {
    // NEXT var
    // TODO: Implement NEXT
    interp.log_output(format!("NEXT {} (not yet implemented)", var));
    Ok(ExecutionResult::Continue)
}

fn execute_gosub(interp: &mut Interpreter, line_num: &str) -> Result<ExecutionResult> {
    if let Ok(num) = line_num.trim().parse::<usize>() {
        interp.push_gosub(interp.current_line);
        // TODO: Jump to line number
        interp.log_output(format!("GOSUB {} (not yet implemented)", num));
    }
    Ok(ExecutionResult::Continue)
}

fn execute_return(interp: &mut Interpreter) -> Result<ExecutionResult> {
    if let Some(line) = interp.pop_gosub() {
        Ok(ExecutionResult::Jump(line + 1))
    } else {
        interp.log_output("RETURN without GOSUB".to_string());
        Ok(ExecutionResult::Continue)
    }
}
