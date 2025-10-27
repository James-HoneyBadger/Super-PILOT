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
}
 
