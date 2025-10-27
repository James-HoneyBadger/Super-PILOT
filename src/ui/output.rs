use eframe::egui;
use crate::app::TimeWarpApp;

pub fn render(app: &mut TimeWarpApp, ui: &mut egui::Ui) {
    ui.horizontal(|ui| {
        // Output panel
        ui.vertical(|ui| {
            ui.heading("Output");
            ui.separator();
            
            egui::ScrollArea::vertical()
                .max_height(300.0)
                .show(ui, |ui| {
                    for line in &app.interpreter.output {
                        ui.label(line);
                    }
                });
        });
        
        ui.separator();
        
        // Turtle graphics panel (rendered below to allow &mut access)
    });
    
    // Render canvas in separate full-width row
    ui.add_space(8.0);
    crate::ui::canvas::render_canvas(app, ui);

    // If interpreter is waiting for input, show a prompt overlay
    if let Some(req) = app.interpreter.pending_input.clone() {
        egui::Window::new("Input Required")
            .collapsible(false)
            .resizable(false)
            .anchor(egui::Align2::CENTER_CENTER, egui::vec2(0.0, 0.0))
            .show(ui.ctx(), |ui| {
                ui.label(format!("📝 {}", req.prompt));
                let response = ui.add(
                    egui::TextEdit::singleline(&mut app.input_buffer)
                        .hint_text("Type here and press Enter")
                        .desired_width(300.0)
                );
                let submitted = response.lost_focus() && ui.input(|i| i.key_pressed(egui::Key::Enter));
                ui.horizontal(|ui| {
                    if ui.button("Submit").clicked() || submitted {
                        let value = app.input_buffer.clone();
                        app.input_buffer.clear();
                        app.interpreter.provide_input(&value);
                        // Resume execution if we were running
                        if app.is_executing {
                            if let Err(e) = app.interpreter.execute(&mut app.turtle_state) {
                                app.error_message = Some(format!("Execution error: {}", e));
                                app.is_executing = false;
                            } else {
                                // If still waiting, remain executing; else stop
                                if app.interpreter.pending_input.is_none() {
                                    app.is_executing = false;
                                }
                            }
                        }
                    }
                    if ui.button("Cancel").clicked() {
                        // Treat cancel as empty input
                        let value = app.input_buffer.clone();
                        app.input_buffer.clear();
                        app.interpreter.provide_input(&value);
                        if app.is_executing {
                            if let Err(e) = app.interpreter.execute(&mut app.turtle_state) {
                                app.error_message = Some(format!("Execution error: {}", e));
                                app.is_executing = false;
                            } else if app.interpreter.pending_input.is_none() {
                                app.is_executing = false;
                            }
                        }
                    }
                });
                // Keep focus on the text edit for quick typing
                if !response.has_focus() {
                    response.request_focus();
                }
            });
    }
}
 
