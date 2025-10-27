use anyhow::Result;
use eframe::egui;

mod app;
mod interpreter;
mod languages;
mod graphics;
mod ui;
mod utils;

#[cfg(feature = "audio")]
mod audio;

#[cfg(feature = "ml")]
mod ml;

#[cfg(feature = "plugins")]
mod plugins;

mod game;
mod iot;

use app::TimeWarpApp;

fn main() -> Result<()> {
    // Initialize logging
    tracing_subscriber::fmt::init();

    tracing::info!("Starting Time Warp Unified v{}", env!("CARGO_PKG_VERSION"));

    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([1400.0, 900.0])
            .with_min_inner_size([800.0, 600.0])
            .with_icon(load_icon()),
        ..Default::default()
    };

    eframe::run_native(
        "Time Warp IDE - Unified",
        options,
        Box::new(|cc| {
            // Set up custom fonts if needed
            configure_fonts(&cc.egui_ctx);
            Ok(Box::new(TimeWarpApp::new(cc)))
        }),
    )
    .map_err(|e| anyhow::anyhow!("Failed to start application: {}", e))
}

fn load_icon() -> egui::IconData {
    // TODO: Load actual icon from assets
    egui::IconData {
        rgba: vec![255; 32 * 32 * 4],
        width: 32,
        height: 32,
    }
}

fn configure_fonts(ctx: &egui::Context) {
    let mut fonts = egui::FontDefinitions::default();
    
    // Add monospace font for code editor
    fonts.families.insert(
        egui::FontFamily::Monospace,
        vec![
            "Hack".to_owned(),
            "Monaco".to_owned(),
            "Consolas".to_owned(),
            "Courier New".to_owned(),
        ],
    );
    
    ctx.set_fonts(fonts);
}
