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
use std::fs;
use std::path::PathBuf;
use time_warp_unified::compiler::TempleCodeCompiler;

fn main() -> Result<()> {
    // Initialize logging
    tracing_subscriber::fmt::init();

    tracing::info!("Starting Time Warp Unified v{}", env!("CARGO_PKG_VERSION"));

    // Lightweight CLI: --compile <input> [-o <output>]
    let args = std::env::args().skip(1).collect::<Vec<_>>();
    if !args.is_empty() && args[0] == "--compile" {
        if args.len() < 2 { return Err(anyhow::anyhow!("Usage: --compile <input> [-o <output>]")); }
        let input = PathBuf::from(&args[1]);
        let mut output: Option<PathBuf> = None;
        if args.len() >= 4 && args[2] == "-o" { output = Some(PathBuf::from(&args[3])); }
        let src = fs::read_to_string(&input)?;
        let out_path = output.unwrap_or_else(|| {
            let mut p = input.clone();
            p.set_extension("");
            let stem = p.file_name().and_then(|s| s.to_str()).unwrap_or("a.out");
            let mut o = PathBuf::from(".");
            o.push(stem);
            o
        });
    let compiler = TempleCodeCompiler::new();
        compiler.compile_to_executable(&src, &out_path)?;
        println!("✅ Built executable: {}", out_path.display());
        return Ok(());
    }

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
            // Don't configure custom fonts - use egui defaults
            // configure_fonts(&cc.egui_ctx);
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

// Font configuration removed - using egui defaults
// Custom fonts can be added later if needed with embedded font data
