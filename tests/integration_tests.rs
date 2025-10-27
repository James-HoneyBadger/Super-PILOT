/// Integration tests for Time Warp IDE
/// 
/// Tests high-level workflows: program loading, execution, UI state

use time_warp_unified::interpreter::Interpreter;
use time_warp_unified::graphics::TurtleState;

#[test]
fn test_pilot_hello_world() {
    let mut interp = Interpreter::new();
    let mut turtle = TurtleState::default();
    
    let program = "T:Hello, World!\nE:";
    interp.load_program(program).unwrap();
    
    let output = interp.execute(&mut turtle).unwrap();
    assert_eq!(output.len(), 1);
    assert_eq!(output[0], "Hello, World!");
}

#[test]
fn test_basic_for_loop() {
    let mut interp = Interpreter::new();
    let mut turtle = TurtleState::default();
    
    let program = r#"
10 FOR I = 1 TO 3
20 PRINT I
30 NEXT I
40 END
"#;
    
    interp.load_program(program).unwrap();
    let output = interp.execute(&mut turtle).unwrap();
    
    // Should print 1, 2, 3 (check content, not count - may have extra lines)
    let numbers: Vec<&str> = output.iter()
        .map(|s| s.trim())
        .filter(|s| s.parse::<i32>().is_ok())
        .collect();
    assert_eq!(numbers, vec!["1", "2", "3"]);
}

#[test]
fn test_logo_turtle_forward() {
    let mut interp = Interpreter::new();
    let mut turtle = TurtleState::default();
    
    let program = "FORWARD 100\nFORWARD 50";
    interp.load_program(program).unwrap();
    
    interp.execute(&mut turtle).unwrap();
    
    // Turtle should have moved 150 units north (0 degrees = up)
    // Note: Logo might use different angle convention, check actual movement
    let distance_moved = (turtle.x * turtle.x + turtle.y * turtle.y).sqrt();
    assert!(distance_moved > 140.0, "Turtle moved {} units", distance_moved);
}

#[test]
fn test_pilot_variables_and_interpolation() {
    let mut interp = Interpreter::new();
    let mut turtle = TurtleState::default();
    
    let program = r#"
U:NAME=Alice
U:AGE=25
T:Name: *NAME*, Age: *AGE*
E:
"#;
    
    interp.load_program(program).unwrap();
    let output = interp.execute(&mut turtle).unwrap();
    
    assert_eq!(output.len(), 1);
    assert!(output[0].contains("Alice"));
    assert!(output[0].contains("25"));
}

#[test]
fn test_basic_if_then_goto() {
    let mut interp = Interpreter::new();
    let mut turtle = TurtleState::default();
    
    let program = r#"
10 LET X = 5
20 IF X > 3 THEN 40
30 PRINT "Not reached"
40 PRINT "Success"
50 END
"#;
    
    interp.load_program(program).unwrap();
    let output = interp.execute(&mut turtle).unwrap();
    
    // IF X > 3 should jump to line 40, printing only "Success"
    let clean_output: Vec<String> = output.iter()
        .filter(|s| !s.trim().is_empty() && !s.starts_with('❌'))
        .map(|s| s.to_string())
        .collect();
    assert!(clean_output.iter().any(|s| s.contains("Success")));
}

#[test]
fn test_logo_repeat_square() {
    let mut interp = Interpreter::new();
    let mut turtle = TurtleState::default();
    
    let program = "REPEAT 4 [FORWARD 50 RIGHT 90]";
    interp.load_program(program).unwrap();
    
    interp.execute(&mut turtle).unwrap();
    
    // After 4 sides with 90 degree turns, turtle should be back near start
    // Square: 4 sides of 50 units each
    assert!((turtle.x.abs()) < 5.0, "Turtle x={}", turtle.x);
    assert!((turtle.y.abs()) < 5.0, "Turtle y={}", turtle.y);
}

#[test]
fn test_basic_gosub_return() {
    let mut interp = Interpreter::new();
    let mut turtle = TurtleState::default();
    
    let program = r#"
10 PRINT "Start"
20 GOSUB 50
30 PRINT "End"
40 END
50 PRINT "Subroutine"
60 RETURN
"#;
    
    interp.load_program(program).unwrap();
    let output = interp.execute(&mut turtle).unwrap();
    
    // Check execution order: Start, Subroutine, End
    let relevant: Vec<&str> = output.iter()
        .map(|s| s.trim())
        .filter(|s| !s.is_empty() && !s.starts_with('❌'))
        .collect();
    assert!(relevant.len() >= 3);
    assert!(relevant[0].contains("Start"));
    assert!(relevant[1].contains("Subroutine"));
    assert!(relevant[2].contains("End"));
}

#[test]
fn test_pilot_conditional_yes_no() {
    let mut interp = Interpreter::new();
    let mut turtle = TurtleState::default();
    
    let program = r#"
U:X=10
C:X>5
Y:
T:X is greater than 5
N:
T:X is not greater than 5
E:
"#;
    
    interp.load_program(program).unwrap();
    let output = interp.execute(&mut turtle).unwrap();
    
    assert_eq!(output.len(), 1);
    assert_eq!(output[0], "X is greater than 5");
}

#[test]
fn test_mixed_language_detection() {
    let mut interp = Interpreter::new();
    let mut turtle = TurtleState::default();
    
    // Mix PILOT, BASIC, and Logo commands
    let program = r#"
T:Starting
PRINT "BASIC says hello"
FORWARD 10
T:Done
"#;
    
    interp.load_program(program).unwrap();
    let output = interp.execute(&mut turtle).unwrap();
    
    assert_eq!(output.len(), 3);
    assert_eq!(output[0], "Starting");
    assert_eq!(output[1], "BASIC says hello");
    assert_eq!(output[2], "Done");
}

#[test]
fn test_execution_timeout_protection() {
    let mut interp = Interpreter::new();
    let mut turtle = TurtleState::default();
    
    // Infinite loop should be caught by max_iterations (100k)
    let program = r#"
10 GOTO 10
"#;
    
    interp.load_program(program).unwrap();
    let result = interp.execute(&mut turtle);
    
    // Should complete with warning, not hang
    assert!(result.is_ok());
}

#[test]
fn test_error_recovery() {
    let mut interp = Interpreter::new();
    let mut turtle = TurtleState::default();
    
    // Invalid GOTO target should not crash
    let program = r#"
10 PRINT "Before"
20 GOTO 999
30 PRINT "After"
40 END
"#;
    
    interp.load_program(program).unwrap();
    let output = interp.execute(&mut turtle).unwrap();
    
    // Should print "Before" and error message, then continue
    assert!(output.len() >= 1);
    assert_eq!(output[0], "Before");
}

#[test]
fn test_logo_procedures() {
    let mut interp = Interpreter::new();
    let mut turtle = TurtleState::new();
    
    let code = r#"
TO SQUARE
FORWARD 50
RIGHT 90
FORWARD 50
RIGHT 90
FORWARD 50
RIGHT 90
FORWARD 50
RIGHT 90
END
SQUARE
"#;
    
    interp.load_program(code).unwrap();
    let _output = interp.execute(&mut turtle).unwrap();
    
    // Check that procedure was stored
    assert!(interp.logo_procedures.contains_key("SQUARE"));
    
    // Verify lines were drawn (should be 4 lines for square)
    assert_eq!(turtle.lines.len(), 4);
}

#[test]
fn test_logo_named_colors() {
    let mut interp = Interpreter::new();
    let mut turtle = TurtleState::new();
    
    let code = r#"
SETCOLOR RED
FORWARD 10
SETCOLOR BLUE
FORWARD 10
"#;
    
    interp.load_program(code).unwrap();
    let _output = interp.execute(&mut turtle).unwrap();
    
    // Verify colors changed (first line red, second blue)
    assert_eq!(turtle.lines.len(), 2);
    use eframe::egui;
    assert_eq!(turtle.lines[0].color, egui::Color32::from_rgb(255, 0, 0)); // RED
    assert_eq!(turtle.lines[1].color, egui::Color32::from_rgb(0, 0, 255)); // BLUE
}

#[test]
fn test_logo_hex_colors() {
    let mut interp = Interpreter::new();
    let mut turtle = TurtleState::new();
    
    let code = r#"
SETCOLOR #FF0000
FORWARD 10
SETCOLOR #00F
FORWARD 10
"#;
    
    interp.load_program(code).unwrap();
    let _output = interp.execute(&mut turtle).unwrap();
    
    // Verify hex colors parsed correctly
    assert_eq!(turtle.lines.len(), 2);
    use eframe::egui;
    assert_eq!(turtle.lines[0].color, egui::Color32::from_rgb(255, 0, 0)); // #FF0000
    assert_eq!(turtle.lines[1].color, egui::Color32::from_rgb(0, 0, 255)); // #00F -> #0000FF
}

#[test]
fn test_basic_line_command() {
    let mut interp = Interpreter::new();
    let mut turtle = TurtleState::new();
    
    let code = r#"
LINE 0, 0, 50, 50
LINE 50, 50, 100, 0
"#;
    
    interp.load_program(code).unwrap();
    let _output = interp.execute(&mut turtle).unwrap();
    
    // Should have 2 lines drawn
    assert_eq!(turtle.lines.len(), 2);
}

#[test]
fn test_basic_circle_command() {
    let mut interp = Interpreter::new();
    let mut turtle = TurtleState::new();
    
    let code = r#"
CIRCLE 0, 0, 50
"#;
    
    interp.load_program(code).unwrap();
    let _output = interp.execute(&mut turtle).unwrap();
    
    // Circle approximated with 36 segments
    assert_eq!(turtle.lines.len(), 36);
}

#[test]
fn test_logo_nested_repeat() {
    let mut interp = Interpreter::new();
    let mut turtle = TurtleState::new();
    
    let code = r#"
REPEAT 2 [REPEAT 2 [FORWARD 10 RIGHT 90]]
"#;
    
    interp.load_program(code).unwrap();
    let _output = interp.execute(&mut turtle).unwrap();
    
    // 2 outer * 2 inner * 1 line each = 4 lines
    assert_eq!(turtle.lines.len(), 4);
}
