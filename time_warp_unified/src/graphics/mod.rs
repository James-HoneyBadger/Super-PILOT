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
    }
}

impl Default for TurtleState {
    fn default() -> Self {
        Self::new()
    }
}
