use anyhow::{anyhow, Result};
use eframe::egui;
use rfd::FileDialog;
use std::fs;

mod interpreter;
mod languages;

use interpreter::{Language, TimeWarpInterpreter};

pub struct TimeWarpApp {
    code: String,
    output: Vec<String>,
    active_tab: usize, // 0 = Editor, 1 = Output & Graphics, 2 = Variables, 3 = Help, 4 = Explorer
    last_file_path: Option<String>,
    open_files: Vec<String>,   // List of open files for tabbed editing
    current_file_index: usize, // Index of currently active file
    file_tree: Vec<String>,    // Stub: List of files in project (to be replaced with real tree)
    interpreter: TimeWarpInterpreter,
    show_find_replace: bool,
    find_text: String,
    replace_text: String,
    is_executing: bool,
    error_message: Option<String>,
    undo_history: Vec<String>,
    undo_position: usize,
    max_undo_steps: usize,
    syntax_highlighting_enabled: bool,
    current_language: Language,
}

impl Default for TimeWarpApp {
    fn default() -> Self {
        Self {
            code: String::new(),
            output: Vec::new(),
            active_tab: 0,
            last_file_path: None,
            interpreter: TimeWarpInterpreter::new(),
            show_find_replace: false,
            find_text: String::new(),
            replace_text: String::new(),
            is_executing: false,
            error_message: None,
            undo_history: Vec::new(),
            undo_position: 0,
            max_undo_steps: 100,
            syntax_highlighting_enabled: true,
            current_language: Language::Pilot,
            open_files: vec!["untitled.tw".to_string()],
            current_file_index: 0,
            file_tree: vec!["untitled.tw".to_string()],
        }
    }
}

impl TimeWarpApp {
    fn save_undo_state(&mut self) {
        // Remove any redo states after current position
        self.undo_history.truncate(self.undo_position);

        // Add current state to history
        self.undo_history.push(self.code.clone());
        self.undo_position = self.undo_history.len();

        // Limit history size
        if self.undo_history.len() > self.max_undo_steps {
            self.undo_history.remove(0);
            self.undo_position -= 1;
        }
    }

    fn undo(&mut self) -> bool {
        if self.undo_position > 0 {
            self.undo_position -= 1;
            self.code = self.undo_history[self.undo_position].clone();
            true
        } else {
            false
        }
    }

    fn redo(&mut self) -> bool {
        if self.undo_position < self.undo_history.len() - 1 {
            self.undo_position += 1;
            self.code = self.undo_history[self.undo_position].clone();
            true
        } else {
            false
        }
    }

    fn execute_code(&mut self) {
        self.active_tab = 1; // Switch to Output tab when running
        self.is_executing = true;
        self.output.clear();

        // Set the language in the interpreter
        self.interpreter.set_language(self.current_language.clone());

        // Split code into lines and execute
        let program_lines: Vec<String> = self
            .code
            .lines()
            .map(|line| line.trim().to_string())
            .filter(|line| !line.is_empty())
            .collect();

        match self.interpreter.execute_program(program_lines) {
            Ok(result) => {
                self.output = result;
                self.is_executing = false;
            }
            Err(err) => {
                self.output = vec![format!("Error: {}", err)];
                self.is_executing = false;
                self.error_message = Some(err.to_string());
            }
        }
    }

    fn load_file(&mut self) -> Result<()> {
        if let Some(path) = FileDialog::new()
            .add_filter("Time Warp files", &["tw", "pilot", "bas", "logo"])
            .add_filter("All files", &["*"])
            .pick_file()
        {
            let content = fs::read_to_string(&path)?;
            self.code = content;
            self.last_file_path = Some(path.display().to_string());
            self.save_undo_state();
            Ok(())
        } else {
            Ok(())
        }
    }

    fn save_file(&mut self) -> Result<()> {
        let path = if let Some(ref path) = self.last_file_path {
            path.clone()
        } else if let Some(path) = FileDialog::new().set_file_name("untitled.tw").save_file() {
            path.display().to_string()
        } else {
            return Ok(());
        };

        fs::write(&path, &self.code)?;
        self.last_file_path = Some(path);
        Ok(())
    }

    fn render_syntax_highlighted_text(&self, ui: &mut egui::Ui, text: &str) {
        if !self.syntax_highlighting_enabled {
            ui.add(
                egui::TextEdit::multiline(&mut text.to_string())
                    .font(egui::TextStyle::Monospace)
                    .desired_width(f32::INFINITY)
                    .interactive(false),
            );
            return;
        }

        // Basic syntax highlighting for different languages
        let lines: Vec<&str> = text.lines().collect();

        for line in lines {
            // Check for PILOT commands (end with :)
            if line.trim().ends_with(':') && line.len() > 1 {
                let cmd = &line[..line.len() - 1];
                ui.horizontal(|ui| {
                    ui.label(
                        egui::RichText::new(cmd)
                            .color(egui::Color32::from_rgb(86, 156, 214))
                            .monospace(),
                    );
                    ui.label(
                        egui::RichText::new(":")
                            .color(egui::Color32::WHITE)
                            .monospace(),
                    );
                });
            }
            // Check for BASIC keywords
            else if line.to_uppercase().starts_with("PRINT ")
                || line.to_uppercase().starts_with("LET ")
                || line.to_uppercase().starts_with("IF ")
                || line.to_uppercase().starts_with("FOR ")
                || line.to_uppercase().starts_with("GOTO ")
            {
                let parts: Vec<&str> = line.splitn(2, ' ').collect();
                ui.horizontal(|ui| {
                    ui.label(
                        egui::RichText::new(parts[0])
                            .color(egui::Color32::from_rgb(86, 156, 214))
                            .monospace(),
                    );
                    if parts.len() > 1 {
                        ui.label(
                            egui::RichText::new(format!(" {}", parts[1]))
                                .color(egui::Color32::WHITE)
                                .monospace(),
                        );
                    }
                });
            }
            // Check for Logo commands
            else if line.to_uppercase().starts_with("FORWARD ")
                || line.to_uppercase().starts_with("LEFT ")
                || line.to_uppercase().starts_with("RIGHT ")
                || line.to_uppercase().starts_with("PENUP")
                || line.to_uppercase().starts_with("PENDOWN")
            {
                let parts: Vec<&str> = line.splitn(2, ' ').collect();
                ui.horizontal(|ui| {
                    ui.label(
                        egui::RichText::new(parts[0])
                            .color(egui::Color32::from_rgb(86, 156, 214))
                            .monospace(),
                    );
                    if parts.len() > 1 {
                        ui.label(
                            egui::RichText::new(format!(" {}", parts[1]))
                                .color(egui::Color32::WHITE)
                                .monospace(),
                        );
                    }
                });
            } else {
                ui.label(egui::RichText::new(line).monospace());
            }
        }
    }

    fn get_help_text(&self) -> &'static str {
        r#"TIME WARP LANGUAGE REFERENCE

=== PILOT COMMANDS ===
T:text          - Output text (variables in *VAR* format)
A:variable      - Accept input into variable
Y:condition     - Set match flag when condition is TRUE
N:condition     - Set match flag when condition is TRUE (alternate)
J:label         - Jump to label
M:label         - Jump to label if match flag is set
R:label         - Gosub to label (subroutine call)
L:label         - Label definition
U:var=expr      - Update/Set variable
END             - End program

=== BASIC COMMANDS ===
LET var = expr  - Assign expression to variable
PRINT expr      - Output expression or string
INPUT var       - Get input into variable
GOTO line       - Jump to line number
IF condition THEN command  - Conditional execution
FOR var = start TO end [STEP step] - Loop from start to end
NEXT [var]     - End of FOR loop
GOSUB line     - Call subroutine at line number
RETURN         - Return from subroutine
END            - End program
REM comment    - Comment

=== LOGO COMMANDS ===
FORWARD distance - Move turtle forward by distance units
BACK distance    - Move turtle backward by distance units
LEFT degrees     - Turn turtle left by degrees
RIGHT degrees    - Turn turtle right by degrees
PENUP           - Lift the pen (stop drawing lines)
PENDOWN         - Lower the pen (start drawing lines)
CLEARSCREEN     - Clear all drawings and return turtle to home
HOME            - Return turtle to center (0,0), facing up
SETXY x y       - Move turtle to coordinates (x,y) without drawing

=== TURTLE GRAPHICS ===
The turtle starts at (0,0) facing up (90 degrees).
Use FORWARD/BACK to move, LEFT/RIGHT to turn.
PENUP/PENDOWN controls whether lines are drawn.
Graphics are displayed in the Output & Graphics tab."#
    }
}

impl eframe::App for TimeWarpApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        // Set up visual style
        let mut visuals = egui::Visuals::light();
        visuals.window_fill = egui::Color32::from_rgb(250, 250, 252);
        visuals.panel_fill = egui::Color32::from_rgb(255, 255, 255);
        ctx.set_visuals(visuals);

        // Menu bar
        egui::TopBottomPanel::top("menu_bar").show(ctx, |ui| {
            ui.horizontal(|ui| {
                ui.menu_button("File", |ui| {
                    if ui.button("New").clicked() {
                        self.code.clear();
                        self.save_undo_state();
                        ui.close_menu();
                    }
                    if ui.button("Open...").clicked() {
                        if let Err(e) = self.load_file() {
                            self.error_message = Some(format!("Failed to load file: {}", e));
                        }
                        ui.close_menu();
                    }
                    if ui.button("Save").clicked() {
                        if let Err(e) = self.save_file() {
                            self.error_message = Some(format!("Failed to save file: {}", e));
                        }
                        ui.close_menu();
                    }
                    if ui.button("Save As...").clicked() {
                        self.last_file_path = None;
                        if let Err(e) = self.save_file() {
                            self.error_message = Some(format!("Failed to save file: {}", e));
                        }
                        ui.close_menu();
                    }
                });

                ui.menu_button("Edit", |ui| {
                    if ui.button("Undo").clicked() {
                        self.undo();
                        ui.close_menu();
                    }
                    if ui.button("Redo").clicked() {
                        self.redo();
                        ui.close_menu();
                    }
                    ui.separator();
                    if ui.button("Find/Replace...").clicked() {
                        self.show_find_replace = true;
                        ui.close_menu();
                    }
                });

                ui.menu_button("Run", |ui| {
                    if ui.button("Run Program").clicked() {
                        self.execute_code();
                        ui.close_menu();
                    }
                    if ui.button("Stop").clicked() {
                        self.is_executing = false;
                        ui.close_menu();
                    }
                });

                ui.menu_button("Examples", |ui| {
                    match self.current_language {
                        Language::Pilot => {
                            if ui.button("Hello World").clicked() {
                                self.code = "T:Hello World!\nT:Welcome to Time Warp IDE".to_string();
                                self.save_undo_state();
                                ui.close_menu();
                            }
                            if ui.button("Math Demo").clicked() {
                                self.code = "U:x=5\nU:y=3\nT:The sum of *x* and *y* is *x+y*\nT:The product is *x*y*".to_string();
                                self.save_undo_state();
                                ui.close_menu();
                            }
                            if ui.button("Input Demo").clicked() {
                                self.code = "T:What is your name?\nA:name\nT:Hello *name*!".to_string();
                                self.save_undo_state();
                                ui.close_menu();
                            }
                        }
                        Language::Basic => {
                            if ui.button("Hello World").clicked() {
                                self.code = "10 PRINT \"Hello World!\"\n20 PRINT \"Welcome to Time Warp IDE\"\n30 END".to_string();
                                self.save_undo_state();
                                ui.close_menu();
                            }
                            if ui.button("Math Demo").clicked() {
                                self.code = "10 LET X = 5\n20 LET Y = 3\n30 PRINT \"The sum is \"; X + Y\n40 PRINT \"The product is \"; X * Y\n50 END".to_string();
                                self.save_undo_state();
                                ui.close_menu();
                            }
                            if ui.button("Loop Demo").clicked() {
                                self.code = "10 FOR I = 1 TO 5\n20 PRINT \"Count: \"; I\n30 NEXT I\n40 END".to_string();
                                self.save_undo_state();
                                ui.close_menu();
                            }
                        }
                        Language::Logo => {
                            if ui.button("Square").clicked() {
                                self.code = "FORWARD 100\nRIGHT 90\nFORWARD 100\nRIGHT 90\nFORWARD 100\nRIGHT 90\nFORWARD 100".to_string();
                                self.save_undo_state();
                                ui.close_menu();
                            }
                            if ui.button("Triangle").clicked() {
                                self.code = "FORWARD 100\nRIGHT 120\nFORWARD 100\nRIGHT 120\nFORWARD 100".to_string();
                                self.save_undo_state();
                                ui.close_menu();
                            }
                            if ui.button("Spiral").clicked() {
                                self.code = "REPEAT 36 [FORWARD 10 RIGHT 10]".to_string();
                                self.save_undo_state();
                                ui.close_menu();
                            }
                        }
                        _ => {
                            ui.label("(Examples not available for this language)");
                        }
                    }
                });

                ui.menu_button("View", |ui| {
                    if ui.selectable_label(self.syntax_highlighting_enabled, "Syntax Highlighting").clicked() {
                        self.syntax_highlighting_enabled = !self.syntax_highlighting_enabled;
                        ui.close_menu();
                    }
                });

                ui.menu_button("Help", |ui| {
                    if ui.button("Language Reference").clicked() {
                        self.active_tab = 3; // Switch to Help tab
                        ui.close_menu();
                    }
                    if ui.button("About").clicked() {
                        // About dialog would go here
                        ui.close_menu();
                    }
                });
            });
        });

        // Toolbar
        egui::TopBottomPanel::top("toolbar").show(ctx, |ui| {
            ui.horizontal(|ui| {
                ui.add_space(8.0);

                // Language selector
                ui.label("Language:");
                egui::ComboBox::from_label("")
                    .selected_text(format!("{:?}", self.current_language))
                    .show_ui(ui, |ui| {
                        ui.selectable_value(&mut self.current_language, Language::Pilot, "Pilot");
                        ui.selectable_value(&mut self.current_language, Language::Basic, "Basic");
                        ui.selectable_value(&mut self.current_language, Language::Logo, "Logo");
                        ui.selectable_value(&mut self.current_language, Language::Python, "Python");
                        ui.selectable_value(
                            &mut self.current_language,
                            Language::JavaScript,
                            "JavaScript",
                        );
                        ui.selectable_value(&mut self.current_language, Language::Perl, "Perl");
                    });

                ui.separator();

                if ui
                    .button("▶️ Run")
                    .on_hover_text("Run Program (F5)")
                    .clicked()
                {
                    self.execute_code();
                }
                if ui.button("⏹️ Stop").on_hover_text("Stop Program").clicked() {
                    self.is_executing = false;
                }
                ui.separator();
                if ui.button("📄 New").on_hover_text("New File").clicked() {
                    self.code.clear();
                    self.save_undo_state();
                }
                if ui.button("📂 Open").on_hover_text("Open File").clicked() {
                    let _ = self.load_file();
                }
                if ui.button("💾 Save").on_hover_text("Save File").clicked() {
                    let _ = self.save_file();
                }
                ui.separator();
                if ui.button("🔍 Find").on_hover_text("Find/Replace").clicked() {
                    self.show_find_replace = !self.show_find_replace;
                }
                if ui.button("↶ Undo").on_hover_text("Undo").clicked() {
                    self.undo();
                }
                if ui.button("↷ Redo").on_hover_text("Redo").clicked() {
                    self.redo();
                }
            });
        });
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.vertical(|ui| {
                // Tab bar
                ui.horizontal(|ui| {
                    if ui
                        .selectable_label(self.active_tab == 0, "📝 Code Editor")
                        .clicked()
                    {
                        self.active_tab = 0;
                    }
                    if ui
                        .selectable_label(self.active_tab == 1, "🖥️ Output & Graphics")
                        .clicked()
                    {
                        self.active_tab = 1;
                    }
                    if ui
                        .selectable_label(self.active_tab == 2, "📊 Variables")
                        .clicked()
                    {
                        self.active_tab = 2;
                    }
                    if ui
                        .selectable_label(self.active_tab == 3, "❓ Help")
                        .clicked()
                    {
                        self.active_tab = 3;
                    }
                    if ui
                        .selectable_label(self.active_tab == 4, "🗂️ Explorer")
                        .clicked()
                    {
                        self.active_tab = 4;
                    }
                });
                ui.separator();

                match self.active_tab {
                    0 => {
                        // Code Editor Tab with tabbed editing
                        ui.vertical(|ui| {
                            // Tab bar for open files
                            ui.horizontal(|ui| {
                                for (i, file) in self.open_files.iter().enumerate() {
                                    if ui
                                        .selectable_label(self.current_file_index == i, file)
                                        .clicked()
                                    {
                                        self.current_file_index = i;
                                        self.code = fs::read_to_string(file).unwrap_or_default();
                                    }
                                    if ui.button("×").on_hover_text("Close file").clicked() {
                                        self.open_files.remove(i);
                                        if self.open_files.is_empty() {
                                            self.open_files.push("untitled.tw".to_string());
                                            self.current_file_index = 0;
                                            self.code.clear();
                                        } else if self.current_file_index >= self.open_files.len() {
                                            self.current_file_index = self.open_files.len() - 1;
                                            self.code = fs::read_to_string(
                                                &self.open_files[self.current_file_index],
                                            )
                                            .unwrap_or_default();
                                        }
                                        break;
                                    }
                                }
                            });
                            ui.horizontal(|ui| {
                                ui.checkbox(
                                    &mut self.syntax_highlighting_enabled,
                                    "Syntax Highlighting",
                                );
                                ui.separator();
                                if ui.button("🔍 Find/Replace").clicked() {
                                    self.show_find_replace = !self.show_find_replace;
                                }
                            });
                            if self.show_find_replace {
                                ui.horizontal(|ui| {
                                    ui.label("Find:");
                                    ui.text_edit_singleline(&mut self.find_text);
                                    ui.label("Replace:");
                                    ui.text_edit_singleline(&mut self.replace_text);
                                    if ui.button("Replace All").clicked() {
                                        self.code =
                                            self.code.replace(&self.find_text, &self.replace_text);
                                        self.save_undo_state();
                                    }
                                });
                                ui.separator();
                            }
                            egui::ScrollArea::vertical().show(ui, |ui| {
                                let mut code_clone = self.code.clone();
                                let response = ui.add(
                                    egui::TextEdit::multiline(&mut code_clone)
                                        .font(egui::TextStyle::Monospace)
                                        .desired_width(f32::INFINITY)
                                        .desired_rows(20),
                                );
                                if response.changed() && code_clone != self.code {
                                    self.code = code_clone;
                                    self.save_undo_state();
                                }
                            });
                        });
                    }
                    4 => {
                        // Explorer Tab
                        ui.vertical(|ui| {
                            ui.label("Project Explorer:");
                            let file_list: Vec<String> = self.file_tree.clone();
                            egui::ScrollArea::vertical().show(ui, |ui| {
                                for file in file_list {
                                    ui.horizontal(|ui| {
                                        ui.label(&file);
                                        if ui.button("Open").clicked() {
                                            if !self.open_files.contains(&file) {
                                                self.open_files.push(file.clone());
                                            }
                                            self.current_file_index = self
                                                .open_files
                                                .iter()
                                                .position(|f| f == &file)
                                                .unwrap_or(0);
                                            self.code =
                                                fs::read_to_string(&file).unwrap_or_default();
                                            self.active_tab = 0;
                                        }
                                        if ui.button("Delete").clicked() {
                                            // Stub: delete file from tree
                                            // In real implementation, delete from disk
                                            self.file_tree.retain(|f| f != &file);
                                            self.open_files.retain(|f| f != &file);
                                            if self.open_files.is_empty() {
                                                self.open_files.push("untitled.tw".to_string());
                                                self.current_file_index = 0;
                                                self.code.clear();
                                            }
                                        }
                                    });
                                }
                            });
                            ui.horizontal(|ui| {
                                if ui.button("New File").clicked() {
                                    let new_name =
                                        format!("untitled_{}.tw", self.file_tree.len() + 1);
                                    self.file_tree.push(new_name.clone());
                                    self.open_files.push(new_name.clone());
                                    self.current_file_index = self.open_files.len() - 1;
                                    self.code.clear();
                                    self.active_tab = 0;
                                }
                                if ui.button("Rename File").clicked() {
                                    // Stub: rename current file
                                    if let Some(file) = self.open_files.get(self.current_file_index)
                                    {
                                        let renamed = format!("{}_renamed.tw", file);
                                        if let Some(tree_idx) =
                                            self.file_tree.iter().position(|f| f == file)
                                        {
                                            self.file_tree[tree_idx] = renamed.clone();
                                        }
                                        self.open_files[self.current_file_index] = renamed;
                                    }
                                }
                            });
                        });
                    }
                    1 => {
                        // Output & Graphics Tab
                        ui.vertical(|ui| {
                            ui.label("Output:");
                            egui::ScrollArea::vertical()
                                .max_height(200.0)
                                .show(ui, |ui| {
                                    for line in &self.output {
                                        ui.label(line);
                                    }
                                });

                            ui.separator();
                            ui.label("Turtle Graphics:");

                            // Simple graphics canvas
                            let canvas_size = egui::vec2(400.0, 300.0);
                            let (rect, _response) =
                                ui.allocate_exact_size(canvas_size, egui::Sense::hover());

                            let turtle_state = self.interpreter.get_turtle_state();
                            ui.painter().rect_filled(
                                rect,
                                0.0,
                                egui::Color32::from_rgb(
                                    turtle_state.bg_color.0,
                                    turtle_state.bg_color.1,
                                    turtle_state.bg_color.2,
                                ),
                            );
                            ui.painter().rect_stroke(
                                rect,
                                0.0,
                                egui::Stroke::new(1.0, egui::Color32::BLACK),
                            );

                            // Draw turtle if visible
                            if turtle_state.visible {
                                let center = rect.center();
                                let turtle_x = center.x + turtle_state.x;
                                let turtle_y = center.y - turtle_state.y; // Flip Y coordinate

                                // Draw turtle as a small triangle
                                let size = 5.0;
                                let angle_rad = turtle_state.angle.to_radians();
                                let points = [
                                    egui::pos2(
                                        turtle_x + size * angle_rad.cos(),
                                        turtle_y - size * angle_rad.sin(),
                                    ),
                                    egui::pos2(
                                        turtle_x + size * (angle_rad + 2.5).cos(),
                                        turtle_y - size * (angle_rad + 2.5).sin(),
                                    ),
                                    egui::pos2(
                                        turtle_x + size * (angle_rad - 2.5).cos(),
                                        turtle_y - size * (angle_rad - 2.5).sin(),
                                    ),
                                ];

                                ui.painter().add(egui::Shape::convex_polygon(
                                    points.to_vec(),
                                    egui::Color32::RED,
                                    egui::Stroke::NONE,
                                ));
                            }
                        });
                    }
                    2 => {
                        // Variables Tab
                        ui.vertical(|ui| {
                            ui.label("Variables:");

                            match self.current_language {
                                Language::Pilot => {
                                    // Show PILOT variables
                                    ui.label("PILOT Variables:");
                                    egui::ScrollArea::vertical().show(ui, |ui| {
                                        // For now, we'll show a placeholder since we need to add variable access methods
                                        ui.label("(PILOT variable display not yet implemented)");
                                    });
                                }
                                Language::Basic => {
                                    ui.label("BASIC Variables:");
                                    egui::ScrollArea::vertical().show(ui, |ui| {
                                        // Show numeric variables
                                        ui.label("Numeric:");
                                        // Placeholder - need to add variable access
                                        ui.label("(BASIC numeric variables not yet implemented)");

                                        ui.separator();
                                        ui.label("String:");
                                        // Placeholder - need to add variable access
                                        ui.label("(BASIC string variables not yet implemented)");
                                    });
                                }
                                Language::Logo => {
                                    ui.label("Logo Variables:");
                                    egui::ScrollArea::vertical().show(ui, |ui| {
                                        // Placeholder - need to add variable access
                                        ui.label("(Logo variable display not yet implemented)");
                                    });
                                }
                                _ => {
                                    ui.label("Variables not available for this language");
                                }
                            }
                        });
                    }
                    3 => {
                        // Help Tab
                        egui::ScrollArea::vertical().show(ui, |ui| {
                            ui.add(
                                egui::TextEdit::multiline(&mut self.get_help_text().to_string())
                                    .font(egui::TextStyle::Monospace)
                                    .desired_width(f32::INFINITY)
                                    .interactive(false),
                            );
                        });
                    }
                    _ => {}
                }
            });
        });

        // Error notification
        if let Some(error) = &self.error_message {
            let error_clone = error.clone();
            egui::Window::new("Error")
                .collapsible(false)
                .resizable(false)
                .show(ctx, |ui| {
                    ui.label(&error_clone);
                    if ui.button("OK").clicked() {
                        self.error_message = None;
                    }
                });
        }

        // Handle keyboard shortcuts
        if ctx.input(|i| i.key_pressed(egui::Key::F5)) {
            self.execute_code();
        }
    }
}

fn main() -> Result<()> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default().with_inner_size([1000.0, 700.0]),
        ..Default::default()
    };

    eframe::run_native(
        "Time Warp IDE",
        options,
        Box::new(|_cc| Box::new(TimeWarpApp::default())),
    )
    .map_err(|e| anyhow!("Failed to run application: {}", e))
}
