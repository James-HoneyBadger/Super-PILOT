use eframe::egui;
use crate::app::TimeWarpApp;

pub fn render(app: &TimeWarpApp, ui: &mut egui::Ui) {
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
        
        // Turtle graphics panel
        render_turtle(app, ui);
    });
}

fn render_turtle(app: &TimeWarpApp, ui: &mut egui::Ui) {
    ui.vertical(|ui| {
        ui.heading("Turtle Graphics");
        
        ui.horizontal(|ui| {
            ui.label(format!("Zoom: {:.1}x", app.turtle_zoom));
            ui.label(format!("Position: ({:.0}, {:.0})", app.turtle_state.x, app.turtle_state.y));
            ui.label(format!("Heading: {:.0}°", app.turtle_state.heading));
        });
        
        ui.separator();
        
        let (response, painter) = ui.allocate_painter(
            egui::Vec2::new(app.turtle_state.canvas_width, app.turtle_state.canvas_height),
            egui::Sense::click_and_drag(),
        );
        
        let to_screen = egui::emath::RectTransform::from_to(
            egui::Rect::from_center_size(
                egui::pos2(0.0, 0.0),
                egui::vec2(
                    app.turtle_state.canvas_width / app.turtle_zoom,
                    app.turtle_state.canvas_height / app.turtle_zoom,
                ),
            ),
            response.rect,
        );
        
        // Draw background
        painter.rect_filled(
            response.rect,
            0.0,
            app.current_theme.background(),
        );
        
        // Draw grid
        let grid_spacing = 50.0 * app.turtle_zoom;
        for x in (-10..=10).map(|i| i as f32 * grid_spacing) {
            let start = to_screen * egui::pos2(x, -app.turtle_state.canvas_height / 2.0);
            let end = to_screen * egui::pos2(x, app.turtle_state.canvas_height / 2.0);
            painter.line_segment(
                [start, end],
                egui::Stroke::new(0.5, egui::Color32::from_gray(40)),
            );
        }
        for y in (-10..=10).map(|i| i as f32 * grid_spacing) {
            let start = to_screen * egui::pos2(-app.turtle_state.canvas_width / 2.0, y);
            let end = to_screen * egui::pos2(app.turtle_state.canvas_width / 2.0, y);
            painter.line_segment(
                [start, end],
                egui::Stroke::new(0.5, egui::Color32::from_gray(40)),
            );
        }
        
        // Draw turtle lines
        for line in &app.turtle_state.lines {
            let start = to_screen * line.start;
            let end = to_screen * line.end;
            painter.line_segment(
                [start, end],
                egui::Stroke::new(line.width * app.turtle_zoom, line.color),
            );
        }
        
        // Draw turtle
        if app.turtle_state.visible {
            let turtle_pos = to_screen * egui::pos2(app.turtle_state.x, app.turtle_state.y);
            let turtle_size = 10.0 * app.turtle_zoom;
            
            painter.circle_filled(turtle_pos, turtle_size, app.current_theme.accent());
            
            // Draw direction indicator
            let angle = app.turtle_state.heading.to_radians();
            let dir = egui::vec2(angle.sin(), -angle.cos()) * turtle_size * 1.5;
            painter.line_segment(
                [turtle_pos, turtle_pos + dir],
                egui::Stroke::new(2.0, app.current_theme.text()),
            );
        }
    });
}
