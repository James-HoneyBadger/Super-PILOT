use eframe::egui;

#[derive(Debug, Clone)]
pub struct TurtleLine {
    pub start: egui::Pos2,
    pub end: egui::Pos2,
    pub color: egui::Color32,
    pub width: f32,
}

pub struct TurtleState {
    pub x: f32,
    pub y: f32,
    pub heading: f32, // degrees, 0 = up
    pub pen_down: bool,
    pub pen_color: egui::Color32,
    pub pen_width: f32,
    pub canvas_width: f32,
    pub canvas_height: f32,
    pub lines: Vec<TurtleLine>,
    pub visible: bool,
    pub bg_color: egui::Color32,
}

impl TurtleState {
    pub fn new() -> Self {
        Self {
            x: 0.0,
            y: 0.0,
            heading: 0.0,
            pen_down: true,
            pen_color: egui::Color32::WHITE,
            pen_width: 2.0,
            canvas_width: 800.0,
            canvas_height: 600.0,
            lines: Vec::new(),
            visible: true,
            bg_color: egui::Color32::from_rgb(10, 10, 20),
        }
    }
    
    pub fn forward(&mut self, distance: f32) {
        let rad = self.heading.to_radians();
        let old_x = self.x;
        let old_y = self.y;
        
        self.x += distance * rad.sin();
        self.y -= distance * rad.cos(); // Y is inverted in screen coordinates
        
        if self.pen_down {
            self.lines.push(TurtleLine {
                start: egui::pos2(old_x, old_y),
                end: egui::pos2(self.x, self.y),
                color: self.pen_color,
                width: self.pen_width,
            });
        }
    }
    
    pub fn back(&mut self, distance: f32) {
        self.forward(-distance);
    }
    
    pub fn left(&mut self, angle: f32) {
        self.heading -= angle;
        self.heading = self.heading.rem_euclid(360.0);
    }
    
    pub fn right(&mut self, angle: f32) {
        self.heading += angle;
        self.heading = self.heading.rem_euclid(360.0);
    }
    
    pub fn goto(&mut self, x: f32, y: f32) {
        if self.pen_down {
            self.lines.push(TurtleLine {
                start: egui::pos2(self.x, self.y),
                end: egui::pos2(x, y),
                color: self.pen_color,
                width: self.pen_width,
            });
        }
        self.x = x;
        self.y = y;
    }
    
    pub fn home(&mut self) {
        self.goto(0.0, 0.0);
        self.heading = 0.0;
    }
    
    pub fn clear(&mut self) {
        self.lines.clear();
    }
    
    #[allow(dead_code)]
    pub fn reset(&mut self) {
        self.x = 0.0;
        self.y = 0.0;
        self.heading = 0.0;
        self.pen_down = true;
        self.pen_color = egui::Color32::WHITE;
        self.pen_width = 2.0;
        self.lines.clear();
        self.visible = true;
        self.bg_color = egui::Color32::from_rgb(10, 10, 20);
    }
    
    /// Save canvas as PNG image
    pub fn save_png(&self, path: &str) -> anyhow::Result<()> {
        use image::{ImageBuffer, Rgba};
        
        let width = self.canvas_width as u32;
        let height = self.canvas_height as u32;
        
        // Create image buffer
        let mut img = ImageBuffer::new(width, height);
        
        // Fill background
        for pixel in img.pixels_mut() {
            *pixel = Rgba([self.bg_color.r(), self.bg_color.g(), self.bg_color.b(), 255]);
        }
        
        // Draw lines (simple rasterization)
        for line in &self.lines {
            draw_line_on_image(&mut img, line, width as f32, height as f32);
        }
        
        // Save to file
        img.save(path)?;
        Ok(())
    }
}

fn draw_line_on_image(img: &mut image::ImageBuffer<image::Rgba<u8>, Vec<u8>>, line: &TurtleLine, canvas_w: f32, canvas_h: f32) {
    // Transform turtle coordinates (centered origin) to image coordinates (top-left origin)
    let cx = canvas_w / 2.0;
    let cy = canvas_h / 2.0;
    let x0 = (line.start.x + cx) as i32;
    let y0 = (cy - line.start.y) as i32;
    let x1 = (line.end.x + cx) as i32;
    let y1 = (cy - line.end.y) as i32;
    
    // Bresenham's line algorithm
    let dx = (x1 - x0).abs();
    let dy = -(y1 - y0).abs();
    let sx = if x0 < x1 { 1 } else { -1 };
    let sy = if y0 < y1 { 1 } else { -1 };
    let mut err = dx + dy;
    
    let mut x = x0;
    let mut y = y0;
    let color = image::Rgba([line.color.r(), line.color.g(), line.color.b(), 255]);
    
    loop {
        if x >= 0 && x < canvas_w as i32 && y >= 0 && y < canvas_h as i32 {
            img.put_pixel(x as u32, y as u32, color);
        }
        
        if x == x1 && y == y1 {
            break;
        }
        
        let e2 = 2 * err;
        if e2 >= dy {
            if x == x1 { break; }
            err += dy;
            x += sx;
        }
        if e2 <= dx {
            if y == y1 { break; }
            err += dx;
            y += sy;
        }
    }
}

impl Default for TurtleState {
    fn default() -> Self {
        Self::new()
    }
}
