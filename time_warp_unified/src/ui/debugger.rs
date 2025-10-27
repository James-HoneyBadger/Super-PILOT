use eframe::egui;
use crate::app::TimeWarpApp;

pub fn render(_app: &TimeWarpApp, ui: &mut egui::Ui) {
    ui.heading("Debugger");
    ui.separator();
    
    ui.label("Debugger features coming soon:");
    ui.label("• Breakpoints");
    ui.label("• Step execution");
    ui.label("• Variable inspector");
    ui.label("• Call stack");
}
