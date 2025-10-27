use anyhow::{anyhow, Result};
use eframe::egui;
use rfd::FileDialog;
use std::fs;

mod interpreter;
mod languages;

use interpreter::{Language, TimeWarpInterpreter};

// Retromodern color themes
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Theme {
    AmberPhosphor,
    GreenPhosphor,
    BluePhosphor,
    ModernDark,
    ModernLight,
}

impl Theme {
    fn background(&self) -> egui::Color32 {
        match self {
            Theme::AmberPhosphor => egui::Color32::from_rgb(25, 20, 12),
            Theme::GreenPhosphor => egui::Color32::from_rgb(12, 20, 12),
            Theme::BluePhosphor => egui::Color32::from_rgb(10, 15, 25),
            Theme::ModernDark => egui::Color32::from_rgb(30, 30, 35),
            Theme::ModernLight => egui::Color32::from_rgb(250, 250, 252),
        }
    }

    fn text(&self) -> egui::Color32 {
        match self {
            Theme::AmberPhosphor => egui::Color32::from_rgb(255, 176, 0),
            Theme::GreenPhosphor => egui::Color32::from_rgb(51, 255, 51),
            Theme::BluePhosphor => egui::Color32::from_rgb(100, 200, 255),
            Theme::ModernDark => egui::Color32::from_rgb(220, 220, 220),
            Theme::ModernLight => egui::Color32::from_rgb(30, 30, 30),
        }
    }

    fn accent(&self) -> egui::Color32 {
        match self {
            Theme::AmberPhosphor => egui::Color32::from_rgb(255, 200, 100),
            Theme::GreenPhosphor => egui::Color32::from_rgb(100, 255, 100),
            Theme::BluePhosphor => egui::Color32::from_rgb(150, 220, 255),
            Theme::ModernDark => egui::Color32::from_rgb(100, 150, 255),
            Theme::ModernLight => egui::Color32::from_rgb(0, 100, 200),
        }
    }

    fn panel(&self) -> egui::Color32 {
        match self {
            Theme::AmberPhosphor => egui::Color32::from_rgb(30, 25, 15),
            Theme::GreenPhosphor => egui::Color32::from_rgb(15, 25, 15),
            Theme::BluePhosphor => egui::Color32::from_rgb(15, 20, 30),
            Theme::ModernDark => egui::Color32::from_rgb(40, 40, 45),
            Theme::ModernLight => egui::Color32::from_rgb(255, 255, 255),
        }
    }

    fn selection(&self) -> egui::Color32 {
        match self {
            Theme::AmberPhosphor => egui::Color32::from_rgba_premultiplied(255, 176, 0, 80),
            Theme::GreenPhosphor => egui::Color32::from_rgba_premultiplied(51, 255, 51, 80),
            Theme::BluePhosphor => egui::Color32::from_rgba_premultiplied(100, 200, 255, 80),
            Theme::ModernDark => egui::Color32::from_rgba_premultiplied(100, 150, 255, 80),
            Theme::ModernLight => egui::Color32::from_rgba_premultiplied(0, 100, 200, 80),
        }
    }

    fn is_retro(&self) -> bool {
        matches!(
            self,
            Theme::AmberPhosphor | Theme::GreenPhosphor | Theme::BluePhosphor
        )
    }
}

pub struct TimeWarpApp {
    code: String, // Deprecated: use file_buffers
    output: Vec<String>,
    active_tab: usize, // 0 = Editor, 1 = Output & Graphics, 2 = Variables, 3 = Help, 4 = Explorer
    last_file_path: Option<String>,
    open_files: Vec<String>,   // List of open files for tabbed editing
    current_file_index: usize, // Index of currently active file
    file_tree: Vec<String>,    // Stub: List of files in project (to be replaced with real tree)
    file_buffers: std::collections::HashMap<String, String>, // filename -> code buffer
    file_modified: std::collections::HashMap<String, bool>,  // Track unsaved changes
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
    current_theme: Theme,
    show_line_numbers: bool,
    font_size: f32,
    show_settings: bool,
    crt_effect_enabled: bool,
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
            file_buffers: std::collections::HashMap::from([(
                "untitled.tw".to_string(),
                String::new(),
            )]),
            file_modified: std::collections::HashMap::new(),
            current_theme: Theme::ModernDark,
            show_line_numbers: true,
            font_size: 14.0,
            show_settings: false,
            crt_effect_enabled: false,
        }
    }
}

impl TimeWarpApp {
    fn apply_theme(&self, ctx: &egui::Context) {
        let mut visuals = if self.current_theme.is_retro() {
            egui::Visuals::dark()
        } else if self.current_theme == Theme::ModernLight {
            egui::Visuals::light()
        } else {
            egui::Visuals::dark()
        };

        visuals.window_fill = self.current_theme.background();
        visuals.panel_fill = self.current_theme.panel();
        visuals.override_text_color = Some(self.current_theme.text());
        visuals.selection.bg_fill = self.current_theme.selection();
        visuals.widgets.inactive.weak_bg_fill = self.current_theme.panel();
        visuals.widgets.inactive.bg_fill = self.current_theme.panel();
        
        // Retro CRT glow effect
        if self.current_theme.is_retro() {
            visuals.window_shadow.extrusion = 0.0;
            visuals.window_rounding = egui::Rounding::ZERO;
            visuals.menu_rounding = egui::Rounding::ZERO;
        }

        ctx.set_visuals(visuals);

        // Set custom font sizes
        let mut style = (*ctx.style()).clone();
        style.text_styles.insert(
            egui::TextStyle::Body,
            egui::FontId::proportional(self.font_size),
        );
        style.text_styles.insert(
            egui::TextStyle::Monospace,
            egui::FontId::monospace(self.font_size),
        );
        style.text_styles.insert(
            egui::TextStyle::Button,
            egui::FontId::proportional(self.font_size),
        );
        ctx.set_style(style);
    }

    fn render_crt_scanlines(&self, ui: &mut egui::Ui) {
        if !self.crt_effect_enabled || !self.current_theme.is_retro() {
            return;
        }

        let rect = ui.available_rect_before_wrap();
        let painter = ui.painter();
        
        // Draw subtle scanlines
        for y in (rect.min.y as i32..rect.max.y as i32).step_by(2) {
            painter.line_segment(
                [
                    egui::pos2(rect.min.x, y as f32),
                    egui::pos2(rect.max.x, y as f32),
                ],
                egui::Stroke::new(0.5, egui::Color32::from_black_alpha(20)),
            );
        }
    }

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
            let filename = path.file_name().unwrap().to_string_lossy().to_string();
            self.file_buffers.insert(filename.clone(), content);
            self.file_modified.insert(filename.clone(), false);
            if !self.open_files.contains(&filename) {
                self.open_files.push(filename.clone());
            }
            self.current_file_index = self.open_files.iter().position(|f| f == &filename).unwrap_or(0);
            self.code = self.file_buffers.get(&filename).cloned().unwrap_or_default();
            self.last_file_path = Some(path.display().to_string());
            self.save_undo_state();
            Ok(())
        } else {
            Ok(())
        }
    }

    fn save_file(&mut self) -> Result<()> {
        let file = &self.open_files[self.current_file_index];
        let code = self.file_buffers.get(file).cloned().unwrap_or_default();
        let path = if let Some(ref path) = self.last_file_path {
            path.clone()
        } else if let Some(path) = FileDialog::new().set_file_name(file).save_file() {
            path.display().to_string()
        } else {
            return Ok(());
        };

        fs::write(&path, &code)?;
        self.last_file_path = Some(path);
        self.file_modified.insert(file.clone(), false);
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

    fn new_file(&mut self) {
        let base = "untitled".to_string();
        let mut idx = 1;
        while self.file_buffers.contains_key(&format!("{}{}.tw", base, idx)) {
            idx += 1;
        }
        let filename = format!("{}{}.tw", base, idx);
        self.file_buffers.insert(filename.clone(), String::new());
        self.open_files.push(filename.clone());
        self.current_file_index = self.open_files.len() - 1;
        self.code = String::new();
        self.last_file_path = None;
        self.save_undo_state();
    }

    fn close_file(&mut self, idx: usize) {
        if idx < self.open_files.len() {
            let file = self.open_files.remove(idx);
            self.file_buffers.remove(&file);
            if self.open_files.is_empty() {
                self.code.clear();
                self.current_file_index = 0;
                self.last_file_path = None;
            } else {
                self.current_file_index = if idx == 0 { 0 } else { idx - 1 };
                let current_file = &self.open_files[self.current_file_index];
                self.code = self.file_buffers.get(current_file).cloned().unwrap_or_default();
            }
        }
    }

    fn rename_file(&mut self, idx: usize, new_name: String) {
        if idx < self.open_files.len() {
            let old_name = self.open_files[idx].clone();
            if !self.file_buffers.contains_key(&new_name) {
                if let Some(code) = self.file_buffers.remove(&old_name) {
                    self.file_buffers.insert(new_name.clone(), code);
                    self.open_files[idx] = new_name.clone();
                    if self.current_file_index == idx {
                        self.code = self.file_buffers.get(&new_name).cloned().unwrap_or_default();
                    }
                }
            }
        }
    }

    fn update_file_tree(&mut self) {
        use std::path::Path;
        self.file_tree.clear();
        let root = Path::new(".");
        if let Ok(entries) = fs::read_dir(root) {
            for entry in entries.flatten() {
                let path = entry.path();
                if path.is_file() {
                    if let Some(name) = path.file_name().and_then(|n| n.to_str()) {
                        self.file_tree.push(name.to_string());
                    }
                }
            }
        }
    }

    fn open_file_from_tree(&mut self, filename: &str) -> Result<()> {
        let path = std::path::Path::new(filename);
        let content = fs::read_to_string(path)?;
        let filename = path.file_name().unwrap().to_string_lossy().to_string();
        self.file_buffers.insert(filename.clone(), content);
        if !self.open_files.contains(&filename) {
            self.open_files.push(filename.clone());
        }
        self.current_file_index = self.open_files.iter().position(|f| f == &filename).unwrap_or(0);
        self.code = self.file_buffers.get(&filename).cloned().unwrap_or_default();
        self.last_file_path = Some(path.display().to_string());
        self.save_undo_state();
        Ok(())
    }
}

impl eframe::App for TimeWarpApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        // Apply theme
        self.apply_theme(ctx);

        // Menu bar with retromodern styling
        egui::TopBottomPanel::top("menu_bar").show(ctx, |ui| {
            ui.visuals_mut().button_frame = true;
            ui.spacing_mut().item_spacing = egui::vec2(8.0, 4.0);
            
            ui.horizontal(|ui| {
                ui.add_space(4.0);
                
                ui.menu_button("📁 File", |ui| {
                    if ui.button("🆕 New").clicked() {
                        self.new_file();
                        ui.close_menu();
                    }
                    if ui.button("📂 Open...").clicked() {
                        if let Err(e) = self.load_file() {
                            self.error_message = Some(format!("Failed to load file: {}", e));
                        }
                        ui.close_menu();
                    }
                    if ui.button("💾 Save").clicked() {
                        if let Err(e) = self.save_file() {
                            self.error_message = Some(format!("Failed to save file: {}", e));
                        }
                        ui.close_menu();
                    }
                    if ui.button("💾 Save As...").clicked() {
                        self.last_file_path = None;
                        if let Err(e) = self.save_file() {
                            self.error_message = Some(format!("Failed to save file: {}", e));
                        }
                        ui.close_menu();
                    }
                });

                ui.menu_button("✏️ Edit", |ui| {
                    if ui.button("↶ Undo").clicked() {
                        self.undo();
                        ui.close_menu();
                    }
                    if ui.button("↷ Redo").clicked() {
                        self.redo();
                        ui.close_menu();
                    }
                    ui.separator();
                    if ui.button("🔍 Find/Replace...").clicked() {
                        self.show_find_replace = true;
                        ui.close_menu();
                    }
                });

                ui.menu_button("▶️ Run", |ui| {
                    if ui.button("▶️ Run Program").clicked() {
                        self.execute_code();
                        ui.close_menu();
                    }
                    if ui.button("⏹️ Stop").clicked() {
                        self.is_executing = false;
                        ui.close_menu();
                    }
                });

                ui.menu_button("👁️ View", |ui| {
                    if ui.selectable_label(self.syntax_highlighting_enabled, "✨ Syntax Highlighting").clicked() {
                        self.syntax_highlighting_enabled = !self.syntax_highlighting_enabled;
                        ui.close_menu();
                    }
                    if ui.selectable_label(self.show_line_numbers, "📊 Line Numbers").clicked() {
                        self.show_line_numbers = !self.show_line_numbers;
                        ui.close_menu();
                    }
                    if ui.selectable_label(self.crt_effect_enabled, "📺 CRT Effect").clicked() {
                        self.crt_effect_enabled = !self.crt_effect_enabled;
                        ui.close_menu();
                    }
                    ui.separator();
                    
                    ui.label("🎨 Theme:");
                    if ui.selectable_label(self.current_theme == Theme::ModernDark, "Modern Dark").clicked() {
                        self.current_theme = Theme::ModernDark;
                        ui.close_menu();
                    }
                    if ui.selectable_label(self.current_theme == Theme::ModernLight, "Modern Light").clicked() {
                        self.current_theme = Theme::ModernLight;
                        ui.close_menu();
                    }
                    if ui.selectable_label(self.current_theme == Theme::AmberPhosphor, "Amber Terminal").clicked() {
                        self.current_theme = Theme::AmberPhosphor;
                        ui.close_menu();
                    }
                    if ui.selectable_label(self.current_theme == Theme::GreenPhosphor, "Green Terminal").clicked() {
                        self.current_theme = Theme::GreenPhosphor;
                        ui.close_menu();
                    }
                    if ui.selectable_label(self.current_theme == Theme::BluePhosphor, "Blue Terminal").clicked() {
                        self.current_theme = Theme::BluePhosphor;
                        ui.close_menu();
                    }
                    
                    ui.separator();
                    if ui.button("⚙️ Settings...").clicked() {
                        self.show_settings = true;
                        ui.close_menu();
                    }
                });

                ui.menu_button("📚 Examples", |ui| {
                    match self.current_language {
                        Language::Pilot => {
                            if ui.button("👋 Hello World").clicked() {
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

                ui.menu_button("❓ Help", |ui| {
                    if ui.button("📖 Language Reference").clicked() {
                        self.active_tab = 3; // Switch to Help tab
                        ui.close_menu();
                    }
                    if ui.button("ℹ️ About").clicked() {
                        // About dialog would go here
                        ui.close_menu();
                    }
                });
            });
        });

        // Elegant toolbar with retromodern design
        egui::TopBottomPanel::top("toolbar").show(ctx, |ui| {
            ui.add_space(4.0);
            ui.horizontal(|ui| {
                ui.add_space(8.0);

                // Language selector with icon
                ui.label("🌐");
                egui::ComboBox::from_label("Language")
                    .selected_text(format!("{:?}", self.current_language))
                    .show_ui(ui, |ui| {
                        ui.selectable_value(&mut self.current_language, Language::Pilot, "🎓 Pilot");
                        ui.selectable_value(&mut self.current_language, Language::Basic, "💾 Basic");
                        ui.selectable_value(&mut self.current_language, Language::Logo, "🐢 Logo");
                        ui.selectable_value(&mut self.current_language, Language::Python, "🐍 Python");
                        ui.selectable_value(
                            &mut self.current_language,
                            Language::JavaScript,
                            "📜 JavaScript",
                        );
                        ui.selectable_value(&mut self.current_language, Language::Perl, "🐪 Perl");
                    });

                ui.separator();

                // Run controls with elegant spacing
                if ui
                    .button("▶️ Run")
                    .on_hover_text("Execute program (F5)")
                    .clicked()
                {
                    self.execute_code();
                }
                if ui.button("⏹️ Stop").on_hover_text("Stop execution").clicked() {
                    self.is_executing = false;
                }
                
                ui.separator();
                
                // File operations
                if ui.button("📄 New").on_hover_text("Create new file").clicked() {
                    self.new_file();
                }
                if ui.button("📂 Open").on_hover_text("Open file").clicked() {
                    let _ = self.load_file();
                }
                if ui.button("💾 Save").on_hover_text("Save current file").clicked() {
                    let _ = self.save_file();
                }
                
                ui.separator();
                
                // Editor tools
                if ui.button("🔍 Find").on_hover_text("Find and replace").clicked() {
                    self.show_find_replace = !self.show_find_replace;
                }
                if ui.button("↶ Undo").on_hover_text("Undo last change").clicked() {
                    self.undo();
                }
                if ui.button("↷ Redo").on_hover_text("Redo change").clicked() {
                    self.redo();
                }
                
                ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                    ui.add_space(8.0);
                    
                    // Status indicator
                    if self.is_executing {
                        ui.label(egui::RichText::new("⚡ Running...").color(self.current_theme.accent()));
                    } else {
                        let current_file = &self.open_files[self.current_file_index];
                        let is_modified = self.file_modified.get(current_file).copied().unwrap_or(false);
                        if is_modified {
                            ui.label(egui::RichText::new("● Modified").color(self.current_theme.accent()));
                        } else {
                            ui.label(egui::RichText::new("✓ Saved").color(egui::Color32::from_rgb(100, 200, 100)));
                        }
                    }
                });
            });
            ui.add_space(4.0);
        });
        // Elegant file explorer (left panel)
        egui::SidePanel::left("file_explorer")
            .default_width(220.0)
            .resizable(true)
            .show(ctx, |ui| {
                ui.add_space(8.0);
                ui.horizontal(|ui| {
                    ui.heading(egui::RichText::new("📁 Project").strong());
                    ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                        if ui.small_button("🔄").on_hover_text("Refresh file tree").clicked() {
                            self.update_file_tree();
                        }
                    });
                });
                ui.separator();
                ui.add_space(4.0);
                
                egui::ScrollArea::vertical().show(ui, |ui| {
                    for file in &self.file_tree.clone() {
                        let is_open = self.open_files.contains(file);
                        let file_icon = if file.ends_with(".tw") || file.ends_with(".pilot") {
                            "🎓"
                        } else if file.ends_with(".bas") {
                            "💾"
                        } else if file.ends_with(".logo") {
                            "🐢"
                        } else {
                            "📄"
                        };
                        
                        let response = ui.selectable_label(is_open, format!("{} {}", file_icon, file));
                        if response.clicked() {
                            let _ = self.open_file_from_tree(file);
                        }
                        response.context_menu(|ui| {
                            if ui.button("📂 Open").clicked() {
                                let _ = self.open_file_from_tree(file);
                                ui.close_menu();
                            }
                            if ui.button("🗑️ Delete").clicked() {
                                // TODO: Implement file deletion
                                ui.close_menu();
                            }
                        });
                    }
                });
            });

        // Elegant tabbed code editor (center panel)
        egui::CentralPanel::default().show(ctx, |ui| {
            if !self.open_files.is_empty() {
                // Elegant tab bar
                egui::TopBottomPanel::top("tabs").show_inside(ui, |ui| {
                    ui.add_space(4.0);
                    ui.horizontal(|ui| {
                        ui.add_space(4.0);
                        for (i, file) in self.open_files.clone().iter().enumerate() {
                            let selected = i == self.current_file_index;
                            let is_modified = self.file_modified.get(file).copied().unwrap_or(false);
                            
                            let mut tab_text = egui::RichText::new(file);
                            if selected {
                                tab_text = tab_text.strong().color(self.current_theme.accent());
                            }
                            
                            ui.group(|ui| {
                                ui.horizontal(|ui| {
                                    if ui.selectable_label(selected, tab_text).clicked() {
                                        self.current_file_index = i;
                                        let current_file = &self.open_files[self.current_file_index];
                                        self.code = self.file_buffers.get(current_file).cloned().unwrap_or_default();
                                    }
                                    if is_modified {
                                        ui.label(egui::RichText::new("●").color(self.current_theme.accent()));
                                    }
                                    if ui.small_button("✕").on_hover_text("Close file").clicked() {
                                        self.close_file(i);
                                    }
                                });
                            });
                        }
                        if ui.button("➕ New").on_hover_text("Create new file").clicked() {
                            self.new_file();
                        }
                    });
                    ui.add_space(4.0);
                });
                
                // Code editor with line numbers
                egui::ScrollArea::vertical().show(ui, |ui| {
                    self.render_crt_scanlines(ui);
                    
                    let current_file = self.open_files[self.current_file_index].clone();
                    let code_content = self.file_buffers.get(&current_file).cloned().unwrap_or_default();
                    let mut code = code_content;
                    
                    if self.show_line_numbers {
                        ui.horizontal_top(|ui| {
                            // Line numbers gutter
                            let line_count = code.lines().count().max(1);
                            let mut line_numbers = String::new();
                            for i in 1..=line_count {
                                line_numbers.push_str(&format!("{:>4}\n", i));
                            }
                            
                            ui.add(
                                egui::TextEdit::multiline(&mut line_numbers.as_str())
                                    .font(egui::TextStyle::Monospace)
                                    .desired_width(50.0)
                                    .interactive(false)
                                    .frame(false),
                            );
                            
                            ui.separator();
                            
                            // Code editor
                            let response = egui::TextEdit::multiline(&mut code)
                                .font(egui::TextStyle::Monospace)
                                .desired_width(f32::INFINITY)
                                .desired_rows(30)
                                .lock_focus(true)
                                .code_editor()
                                .show(ui);
                            
                            if response.response.changed() {
                                self.file_buffers.insert(current_file.clone(), code.clone());
                                self.code = code.clone();
                                self.file_modified.insert(current_file.clone(), true);
                            }
                        });
                    } else {
                        let response = egui::TextEdit::multiline(&mut code)
                            .font(egui::TextStyle::Monospace)
                            .desired_width(f32::INFINITY)
                            .desired_rows(30)
                            .lock_focus(true)
                            .code_editor()
                            .show(ui);
                        
                        if response.response.changed() {
                            self.file_buffers.insert(current_file.clone(), code.clone());
                            self.code = code.clone();
                            self.file_modified.insert(current_file.clone(), true);
                        }
                    }
                });
            } else {
                ui.vertical_centered(|ui| {
                    ui.add_space(100.0);
                    ui.heading(egui::RichText::new("⏳ Time Warp IDE").size(32.0).strong());
                    ui.add_space(20.0);
                    ui.label(egui::RichText::new("Open or create a file to begin coding").size(16.0));
                    ui.add_space(20.0);
                    if ui.button(egui::RichText::new("📄 Create New File").size(18.0)).clicked() {
                        self.new_file();
                    }
                    if ui.button(egui::RichText::new("📂 Open File").size(18.0)).clicked() {
                        let _ = self.load_file();
                    }
                });
            }
        });

        // Settings panel
        if self.show_settings {
            egui::Window::new("⚙️ Settings")
                .collapsible(false)
                .resizable(true)
                .default_width(400.0)
                .show(ctx, |ui| {
                    ui.heading("Editor Settings");
                    ui.separator();
                    
                    ui.horizontal(|ui| {
                        ui.label("Font Size:");
                        ui.add(egui::Slider::new(&mut self.font_size, 8.0..=24.0).suffix(" pt"));
                    });
                    
                    ui.checkbox(&mut self.show_line_numbers, "Show line numbers");
                    ui.checkbox(&mut self.syntax_highlighting_enabled, "Syntax highlighting");
                    ui.checkbox(&mut self.crt_effect_enabled, "CRT scanline effect");
                    
                    ui.add_space(10.0);
                    ui.heading("Theme");
                    ui.separator();
                    
                    ui.radio_value(&mut self.current_theme, Theme::ModernDark, "🌙 Modern Dark");
                    ui.radio_value(&mut self.current_theme, Theme::ModernLight, "☀️ Modern Light");
                    ui.radio_value(&mut self.current_theme, Theme::AmberPhosphor, "🟡 Amber Terminal");
                    ui.radio_value(&mut self.current_theme, Theme::GreenPhosphor, "🟢 Green Terminal");
                    ui.radio_value(&mut self.current_theme, Theme::BluePhosphor, "🔵 Blue Terminal");
                    
                    ui.add_space(10.0);
                    if ui.button("✓ Close").clicked() {
                        self.show_settings = false;
                    }
                });
        }

        // Error notification with elegant design
        if let Some(error) = &self.error_message {
            let error_clone = error.clone();
            egui::Window::new("❌ Error")
                .collapsible(false)
                .resizable(false)
                .anchor(egui::Align2::CENTER_CENTER, egui::vec2(0.0, 0.0))
                .show(ctx, |ui| {
                    ui.add_space(8.0);
                    ui.label(egui::RichText::new(&error_clone).color(egui::Color32::from_rgb(255, 100, 100)));
                    ui.add_space(8.0);
                    if ui.button("✓ OK").clicked() {
                        self.error_message = None;
                    }
                });
        }

        // Keyboard shortcuts
        if ctx.input(|i| i.key_pressed(egui::Key::F5)) {
            self.execute_code();
        }
        if ctx.input(|i| i.modifiers.ctrl && i.key_pressed(egui::Key::S)) {
            let _ = self.save_file();
        }
        if ctx.input(|i| i.modifiers.ctrl && i.key_pressed(egui::Key::O)) {
            let _ = self.load_file();
        }
        if ctx.input(|i| i.modifiers.ctrl && i.key_pressed(egui::Key::N)) {
            self.new_file();
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
