use eframe::egui;
use crate::app::TimeWarpApp;

pub fn render(_app: &TimeWarpApp, ui: &mut egui::Ui) {
    ui.heading("Time Warp IDE - Help");
    ui.separator();
    
    egui::ScrollArea::vertical().show(ui, |ui| {
        ui.heading("Quick Start");
        ui.label("Time Warp supports three educational programming languages:");
        ui.add_space(10.0);
        
        ui.heading("PILOT Language");
        ui.label("T:text - Display text");
        ui.label("A:var - Accept input");
        ui.label("U:var=value - Set variable");
        ui.label("C:condition - Compute condition");
        ui.label("Y:condition - Execute if true");
        ui.label("N:condition - Execute if false");
        ui.label("J:label - Jump to label");
        ui.label("L:label - Define label");
        ui.label("E: - End program");
        ui.add_space(10.0);
        
        ui.heading("BASIC Language");
        ui.label("PRINT \"text\" - Display text");
        ui.label("INPUT var - Get user input");
        ui.label("LET var = value - Set variable");
        ui.label("GOTO line - Jump to line number");
        ui.label("IF condition THEN command - Conditional");
        ui.label("FOR var = start TO end - Loop");
        ui.label("NEXT var - End loop");
        ui.label("GOSUB line - Call subroutine");
        ui.label("RETURN - Return from subroutine");
        ui.label("END - End program");
        ui.add_space(10.0);
        
        ui.heading("Logo Language");
        ui.label("FORWARD n - Move turtle forward");
        ui.label("BACK n - Move turtle backward");
        ui.label("LEFT n - Turn left n degrees");
        ui.label("RIGHT n - Turn right n degrees");
        ui.label("PENUP - Lift pen");
        ui.label("PENDOWN - Lower pen");
        ui.label("CLEARSCREEN - Clear graphics");
        ui.label("HOME - Return to center");
        ui.label("SETXY x y - Set position");
        ui.label("REPEAT n [commands] - Repeat commands");
        ui.add_space(10.0);
        
        ui.heading("Example Programs");
        ui.label("See the examples/ directory for sample programs in each language.");
    });
}
