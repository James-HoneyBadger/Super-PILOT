#!/usr/bin/env python3
# Time Warp Interpreter - Complete Implementation
# For integration with Time Warp IDE

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import random
import math
import re
import time
from datetime import datetime


class ArduinoController:
    """Arduino hardware controller with simulation support"""

    def __init__(self, simulation_mode=True):
        self.simulation_mode = simulation_mode


class RPiController:
    """Raspberry Pi hardware controller with simulation support"""

    def __init__(self, simulation_mode=True):
        self.simulation_mode = simulation_mode


class AudioMixer:
    """Audio mixer for playing sounds with play/aplay support"""

    def __init__(self):
        self.registry = {}  # name -> path
        self.has_play = self._has_exe("play")
        self.has_aplay = self._has_exe("aplay")

    def _has_exe(self, name: str) -> bool:
        import os

        for p in os.environ.get("PATH", "").split(os.pathsep):
            f = os.path.join(p, name)
            if os.path.isfile(f) and os.access(f, os.X_OK):
                return True
        return False

    def register_sound(self, name, path):
        """Register a sound file with a name"""
        self.registry[name] = path

    def play_sound(self, name):
        """Play a registered sound"""
        path = self.registry.get(name)
        if not path:
            return
        if self.has_play:
            os.system(f"play -q {path}")
        elif self.has_aplay and path.lower().endswith(".wav"):
            os.system(f"aplay -q {path}")
        else:
            # Fallback: system bell
            print("\a", end="", flush=True)


# Easing functions for animations
EASE_FUNCTIONS = {
    "linear": lambda t: t,
    "quadOut": lambda t: 1 - (1 - t) * (1 - t),
    "quadIn": lambda t: t * t,
    "smooth": lambda t: t * t * (3 - 2 * t),
}


class Tween:
    """Animation tween for smoothly changing values over time"""

    def __init__(
        self,
        store: dict,
        key: str,
        start_val: float,
        end_val: float,
        duration_ms: int,
        ease: str = "linear",
    ):
        self.store = store
        self.key = key
        self.start_val = float(start_val)
        self.end_val = float(end_val)
        self.duration = max(1, int(duration_ms))
        self.ease = EASE_FUNCTIONS.get(ease, EASE_FUNCTIONS["linear"])
        self.elapsed = 0
        self.done = False

    def step(self, dt_ms):
        if self.done:
            return
        self.elapsed += dt_ms
        t = min(1.0, self.elapsed / self.duration)
        k = self.ease(t)
        self.store[self.key] = self.start_val + (self.end_val - self.start_val) * k
        if self.elapsed >= self.duration:
            self.store[self.key] = self.end_val
            self.done = True


class Timer:
    """Delayed action timer"""

    def __init__(self, delay_ms: int, label: str):
        self.delay = max(0, int(delay_ms))
        self.label = label


class Particle:
    """Particle for visual effects"""

    def __init__(self, x, y, vx, vy, life_ms, color="#ffaa33", size=3):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life_ms
        self.color = color
        self.size = size

    def step(self, dt_ms):
        self.x += self.vx * (dt_ms / 1000.0)
        self.y += self.vy * (dt_ms / 1000.0)
        self.vy -= 30 * (dt_ms / 1000.0)  # gravity
        self.life -= dt_ms


class ToolTip:
    """Lightweight tooltip helper usable across the UI."""

    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tipwindow = None
        self.id = None
        widget.bind("<Enter>", self.schedule)
        widget.bind("<Leave>", self.hide)

    def schedule(self, event=None):
        try:
            self.id = self.widget.after(self.delay, self.show)
        except Exception:
            self.id = None

    def show(self):
        if self.tipwindow or not self.text:
            return
        try:
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
            self.tipwindow = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            label = tk.Label(
                tw,
                text=self.text,
                justify=tk.LEFT,
                background="#ffffe0",
                relief=tk.SOLID,
                borderwidth=1,
                font=("Segoe UI", 9),
            )
            label.pack(ipadx=4, ipady=2)
        except Exception:
            self.tipwindow = None

    def hide(self, event=None):
        if self.id:
            try:
                self.widget.after_cancel(self.id)
            except Exception:
                pass
            self.id = None
        if self.tipwindow:
            try:
                self.tipwindow.destroy()
            except Exception:
                pass
            self.tipwindow = None


class TimeWarpInterpreter:
    def __init__(self, output_widget=None):
        self.output_widget = output_widget
        self.variables = {}
        self.labels = {}
        self.procedures = {}
        self.program_lines = []
        self.current_line = 0
        self.stack = []
        # For-loop stack: list of dicts with keys: var, end, step, for_line
        self.for_stack = []
        self.match_flag = False
        # Internal flag: set when a Y: or N: was the last command to allow
        # the immediately following T: to be treated as conditional.
        self._last_match_set = False
        self.running = False
        self.debug_mode = False
        self.breakpoints = set()
        self.max_iterations = 10000  # Prevent infinite loops

        # DATA/READ/RESTORE support
        self.data_list = []  # List of data values
        self.data_pointer = 0  # Current position in data list

        # Turtle graphics state
        self.turtle_x = 200  # canvas x
        self.turtle_y = 200  # canvas y
        self.turtle_heading = 90  # degrees, 90 = up
        self.pen_down = True
        self.pen_color = "black"
        self.pen_width = 1
        self.graphics_widget = None
        self.canvas_width = 400
        self.canvas_height = 400
        self.origin_x = 200
        self.origin_y = 200

        # Color palette for SETCOLOR numbers
        self.colors = [
            "black",
            "blue",
            "red",
            "green",
            "yellow",
            "magenta",
            "cyan",
            "white",
            "gray",
            "orange",
            "purple",
            "brown",
            "pink",
            "lightblue",
            "lightgreen",
        ]

        # Hardware controllers (simulation mode by default)
        self.arduino_controller = ArduinoController(simulation_mode=True)
        self.rpi_controller = RPiController(simulation_mode=True)

        # Audio mixer (for sound playback)
        self.audio_mixer = AudioMixer()

        # Animation and particle systems
        self.tweens = []  # List of active tweens
        self.timers = []  # List of active timers
        self.particles = []  # List of active particles
        self.sprites = (
            {}
        )  # Sprite registry: name -> {'path': str, 'x': float, 'y': float}
        self.hud_enabled = False  # HUD display toggle
        self.last_update_time = time.time() * 1000  # For delta time calculations

        self.reset_turtle()

    def reset(self):
        """Reset interpreter state"""
        self.variables = {}
        self.labels = {}
        self.procedures = {}
        self.program_lines = []
        self.current_line = 0
        self.stack = []
        self.for_stack = []
        self.match_flag = False
        self._last_match_set = False
        self.running = False
        self.reset_turtle()

    def reset_turtle(self):
        self.turtle_x = 200
        self.turtle_y = 200
        self.turtle_heading = 90
        self.pen_down = True
        self.pen_color = "black"
        self.pen_width = 1
        self.sprites = {}  # Reset sprite system
        if self.graphics_widget:
            self.graphics_widget.delete("all")

    def move_turtle(self, distance):
        """Move turtle forward/backward by distance, drawing if pen is down"""
        if not self.graphics_widget:
            return
        # Calculate new position
        angle_rad = math.radians(self.turtle_heading)
        new_x = self.turtle_x + distance * math.cos(angle_rad)
        new_y = self.turtle_y + distance * math.sin(angle_rad)

        if self.pen_down:
            # Draw line from current to new position
            x1 = self.origin_x + self.turtle_x
            y1 = self.origin_y - self.turtle_y
            x2 = self.origin_x + new_x
            y2 = self.origin_y - new_y
            self.graphics_widget.create_line(
                x1, y1, x2, y2, fill=self.pen_color, width=self.pen_width, tags="turtle"
            )
            self.graphics_widget.update()

        # Update turtle position
        self.turtle_x = new_x
        self.turtle_y = new_y

        # Update HUD if enabled
        if self.hud_enabled:
            self.update_hud()

    def draw_circle_at(
        self, x, y, radius, color, start_angle=0, end_angle=360, aspect=1.0
    ):
        """Draw a circle or arc at specified coordinates"""
        if not self.graphics_widget:
            return

        # Convert to canvas coordinates
        canvas_x = self.origin_x + x
        canvas_y = self.origin_y - y

        # Calculate bounding box
        width = radius * 2
        height = radius * 2 * aspect

        # Draw the circle/arc
        if start_angle == 0 and end_angle == 360:
            # Full circle
            self.graphics_widget.create_oval(
                canvas_x - radius,
                canvas_y - radius * aspect,
                canvas_x + radius,
                canvas_y + radius * aspect,
                outline=color,
                fill="",
                width=self.pen_width,
                tags="graphics",
            )
        else:
            # Arc
            start = start_angle
            extent = end_angle - start_angle
            self.graphics_widget.create_arc(
                canvas_x - radius,
                canvas_y - radius * aspect,
                canvas_x + radius,
                canvas_y + radius * aspect,
                start=start,
                extent=extent,
                outline=color,
                fill="",
                width=self.pen_width,
                tags="graphics",
            )

        self.graphics_widget.update()

    def execute_draw_commands(self, draw_string):
        """Execute DRAW command string with turtle graphics commands"""
        if not self.graphics_widget:
            return

        # DRAW commands: UnDnRlLeFgHhEeNn... etc.
        # U - pen up, D - pen down, NnEeSsWw - directions, F - forward, B - back, etc.
        i = 0
        original_pen_state = self.pen_down
        original_heading = self.turtle_heading

        try:
            while i < len(draw_string):
                cmd = draw_string[i].upper()
                i += 1

                if cmd in "UD":  # Pen Up/Down
                    self.pen_down = cmd == "D"
                elif cmd in "NESW":  # Directions
                    if cmd == "N":
                        self.turtle_heading = 90
                    elif cmd == "E":
                        self.turtle_heading = 0
                    elif cmd == "S":
                        self.turtle_heading = 270
                    elif cmd == "W":
                        self.turtle_heading = 180
                elif cmd in "FB":  # Forward/Back
                    # Parse number
                    num_str = ""
                    while i < len(draw_string) and draw_string[i].isdigit():
                        num_str += draw_string[i]
                        i += 1
                    if num_str:
                        distance = int(num_str)
                        if cmd == "B":
                            distance = -distance
                        self.move_turtle(distance)
                    else:
                        i -= 1  # No number found, back up
                elif cmd == "R":  # Right turn
                    num_str = ""
                    while i < len(draw_string) and draw_string[i].isdigit():
                        num_str += draw_string[i]
                        i += 1
                    if num_str:
                        angle = int(num_str)
                        self.turtle_heading = (self.turtle_heading - angle) % 360
                    else:
                        i -= 1
                elif cmd == "L":  # Left turn
                    num_str = ""
                    while i < len(draw_string) and draw_string[i].isdigit():
                        num_str += draw_string[i]
                        i += 1
                    if num_str:
                        angle = int(num_str)
                        self.turtle_heading = (self.turtle_heading + angle) % 360
                    else:
                        i -= 1
                elif cmd == "M":  # Move to coordinates
                    # Parse x,y coordinates
                    x_str = ""
                    y_str = ""
                    while i < len(draw_string) and draw_string[i] != ",":
                        x_str += draw_string[i]
                        i += 1
                    if i < len(draw_string) and draw_string[i] == ",":
                        i += 1  # skip comma
                        while i < len(draw_string) and draw_string[i] != ";":
                            y_str += draw_string[i]
                            i += 1
                        if i < len(draw_string) and draw_string[i] == ";":
                            i += 1  # skip semicolon

                    if x_str and y_str:
                        try:
                            x = int(x_str)
                            y = int(y_str)
                            self.turtle_x = x
                            self.turtle_y = y
                        except ValueError:
                            pass
                elif cmd == "C":  # Set color
                    num_str = ""
                    while i < len(draw_string) and draw_string[i].isdigit():
                        num_str += draw_string[i]
                        i += 1
                    if num_str:
                        color_idx = int(num_str) % len(self.colors)
                        self.pen_color = self.colors[color_idx]
                # Skip unrecognized commands
                else:
                    continue

        finally:
            # Restore original state if needed
            pass

    def play_music_string(self, music_string):
        """Play music using GW-BASIC PLAY command syntax"""
        # GW-BASIC PLAY syntax: A-G for notes, # + for sharp/flat, octave numbers, etc.
        # For now, we'll implement a basic version that logs the music string
        self.log_output(f"Playing music: {music_string}")

        # In a full implementation, this would parse the music string and play notes
        # For now, we'll just play a beep for each note-like character
        note_count = sum(1 for c in music_string.upper() if c in "ABCDEFG")
        for _ in range(min(note_count, 10)):  # Limit to avoid too many beeps
            try:
                self.audio_mixer.play_sound("beep")
                time.sleep(0.1)  # Short delay between notes
            except:
                self.log_output("\a", end="")
                time.sleep(0.1)

    def play_sound(self, frequency, duration, volume=255, voice=0):
        """Play a sound with specified frequency, duration, volume, and voice"""
        # Convert GW-BASIC parameters to something playable
        # frequency: Hz, duration: clock ticks (18.2 ticks/second), volume: 0-255, voice: 0-3

        if frequency <= 0 or duration <= 0:
            return

        # For now, we'll use the audio mixer or system beep
        # In a full implementation, this would generate actual tones
        try:
            # Try to play a registered sound, or fall back to beep
            sound_name = f"tone_{frequency}_{duration}"
            self.audio_mixer.play_sound(sound_name)
        except:
            # Fallback: multiple beeps for different "voices"
            beep_count = max(
                1, min(int(duration / 5), 10)
            )  # Scale duration to beep count
            for _ in range(beep_count):
                self.log_output("\a", end="")
                time.sleep(min(0.1, duration / 182))  # Approximate timing

        self.log_output(
            f"Played sound: freq={frequency}Hz, duration={duration}ticks, volume={volume}, voice={voice}"
        )

    def draw_rectangle(self, width, height):
        """Draw a rectangle with the given width and height"""
        if not self.graphics_widget:
            return
        x1 = self.origin_x + self.turtle_x - width / 2
        y1 = self.origin_y - self.turtle_y - height / 2
        x2 = self.origin_x + self.turtle_x + width / 2
        y2 = self.origin_y - self.turtle_y + height / 2
        self.graphics_widget.create_rectangle(
            x1, y1, x2, y2, outline=self.pen_color, width=self.pen_width, tags="turtle"
        )
        self.graphics_widget.update()

    def draw_dot(self, size):
        """Draw a dot at the current turtle position"""
        if not self.graphics_widget:
            return
        radius = size / 2
        x1 = self.origin_x + self.turtle_x - radius
        y1 = self.origin_y - self.turtle_y - radius
        x2 = self.origin_x + self.turtle_x + radius
        y2 = self.origin_y - self.turtle_y + radius
        self.graphics_widget.create_oval(
            x1, y1, x2, y2, fill=self.pen_color, outline="", tags="turtle"
        )
        self.graphics_widget.update()

    def draw_image(self, path, width=None, height=None):
        """Draw an image at the current turtle position"""
        if not self.graphics_widget:
            return
        try:
            from PIL import Image, ImageTk

            img = Image.open(path)
            if width and height:
                img = img.resize((int(width), int(height)), Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            x = self.origin_x + self.turtle_x
            y = self.origin_y - self.turtle_y
            self.graphics_widget.create_image(
                x, y, image=tk_img, anchor="center", tags="turtle"
            )
            # Keep reference to prevent garbage collection
            if not hasattr(self.graphics_widget, "_images"):
                self.graphics_widget._images = []
            self.graphics_widget._images.append(tk_img)
            self.graphics_widget.update()
        except Exception as e:
            self.log_output(f"Error loading image {path}: {e}")

    def toggle_hud(self):
        """Toggle the HUD display"""
        self.hud_enabled = not self.hud_enabled
        if self.graphics_widget:
            self.update_hud()

    def update_hud(self):
        """Update the HUD display"""
        if not self.graphics_widget:
            return
        self.graphics_widget.delete("hud")
        if self.hud_enabled:
            hud_text = f"Pos: ({int(self.turtle_x)}, {int(self.turtle_y)}) Heading: {int(self.turtle_heading)}°"
            self.graphics_widget.create_rectangle(
                10, 10, 300, 35, fill="white", outline="black", tags="hud"
            )
            self.graphics_widget.create_text(
                15, 22, text=hud_text, anchor="w", fill="black", tags="hud"
            )
        self.graphics_widget.update()

    def take_snapshot(self, filename):
        """Take a snapshot of the graphics canvas"""
        if not self.graphics_widget:
            return
        try:
            self.graphics_widget.postscript(file=filename, colormode="color")
            self.log_output(f"Snapshot saved to {filename}")
        except Exception as e:
            self.log_output(f"Error saving snapshot: {e}")

    def create_sprite(self, name, path):
        """Create a new sprite"""
        self.sprites[name] = {"path": path, "x": 0, "y": 0}

    def set_sprite_position(self, name, x, y):
        """Set sprite position"""
        if name in self.sprites:
            self.sprites[name]["x"] = x
            self.sprites[name]["y"] = y

    def draw_sprite(self, name):
        """Draw a sprite at its current position"""
        if name not in self.sprites or not self.graphics_widget:
            return
        sprite = self.sprites[name]
        self.draw_image(sprite["path"], None, None)
        # Note: This moves the turtle to the sprite position for drawing
        # In a full implementation, sprites would be drawn independently

    def log_output(self, text):
        """Log output to widget or console"""
        if self.output_widget:
            try:
                self.output_widget.insert(tk.END, str(text) + "\n")
                self.output_widget.see(tk.END)
            except tk.TclError:
                # Widget has been destroyed, fall back to console
                print(text)
        else:
            print(text)

    def parse_line(self, line):
        """Parse a program line for line number and command"""
        line = line.strip()
        match = re.match(r"^(\d+)\s+(.*)", line)
        if match:
            line_number, command = match.groups()
            return int(line_number), command.strip()
        return None, line.strip()

    def evaluate_expression(self, expr):
        """Safely evaluate mathematical expressions with variables"""
        if not isinstance(expr, str):
            return expr

        expr = expr.strip()

        # Reject obviously dangerous expressions
        if any(
            char in expr
            for char in [
                "{",
                "}",
                "[",
                "]",
                "__",
                "import",
                "exec",
                "eval",
                "open",
                "file",
            ]
        ):
            self.log_output("Expression contains forbidden characters")
            return 0

        # Replace variables.
        # First substitute explicit *VAR* interpolation (used in many programs).
        for var_name, var_value in self.variables.items():
            if isinstance(var_value, str):
                val_repr = f'"{var_value}"'
            else:
                val_repr = str(var_value)
            # Replace *VAR* occurrences first
            expr = expr.replace(f"*{var_name}*", val_repr)

        # Then replace bare variable names using word boundaries to avoid
        # accidental substring replacements (e.g. A vs AB).
        for var_name, var_value in self.variables.items():
            if isinstance(var_value, str):
                val_repr = f'"{var_value}"'
            else:
                val_repr = str(var_value)
            try:
                expr = re.sub(rf"\b{re.escape(var_name)}\b", val_repr, expr)
            except re.error:
                # fallback to plain replace if regex fails for unusual names
                expr = expr.replace(var_name, val_repr)

        try:
            # Allow basic math operations and functions
            allowed_names = {
                "abs": abs,
                "round": round,
                "int": int,
                "float": float,
                "max": max,
                "min": min,
                "len": len,
                "str": str,
                # RND accepts 0 or 1 args in many example programs
                "RND": (lambda *a: random.random()),
                "INT": int,
                "VAL": lambda x: float(x) if "." in str(x) else int(x),
                "UPPER": lambda x: str(x).upper(),
                "LOWER": lambda x: str(x).lower(),
                "MID": (
                    lambda s, start, length: (
                        str(s)[int(start) - 1 : int(start) - 1 + int(length)]
                        if isinstance(s, (str, int, float))
                        else ""
                    )
                ),
                # GW-BASIC Math Functions
                "SIN": math.sin,
                "COS": math.cos,
                "TAN": math.tan,
                "LOG": math.log,
                "SQR": math.sqrt,
                "EXP": math.exp,
                "ATN": math.atan,
                "SGN": lambda x: 1 if x > 0 else (-1 if x < 0 else 0),
                "ABS": abs,
                # GW-BASIC String Functions
                "LEFT_DOLLAR": lambda s, n: str(s)[: int(n)],
                "RIGHT_DOLLAR": lambda s, n: str(s)[-int(n) :],
                "MID_DOLLAR": lambda s, start, length=None: (
                    str(s)[int(start) - 1 : int(start) - 1 + int(length)]
                    if length is not None
                    else str(s)[int(start) - 1 :]
                ),
                "INSTR": lambda s, sub: (
                    str(s).find(str(sub)) + 1 if str(sub) in str(s) else 0
                ),
                "LEN": len,
                "CHR_DOLLAR": lambda n: chr(int(n)),
                "ASC": lambda s: ord(str(s)[0]) if str(s) else 0,
                "STR_DOLLAR": lambda n: str(n),
                "SPACE_DOLLAR": lambda n: " " * int(n),
                "STRING_DOLLAR": lambda n, c: str(c) * int(n),
                # TIMER function - returns seconds since midnight
                "TIMER": lambda: time.time() % 86400,
            }

            # Create safe environment
            safe_dict = {
                "str": str,
                "int": int,
                "float": float,
                "len": len,
                "abs": abs,
                "round": round,
                "max": max,
                "min": min,
            }
            safe_dict.update(allowed_names)

            # Replace undefined variables with defaults
            def replace_undefined_var(match):
                var = match.group(0)
                # Check if it's a GW-BASIC function (with $ replaced)
                if var.replace("$", "_DOLLAR") in allowed_names:
                    return var.replace("$", "_DOLLAR")
                if var in self.variables:
                    value = self.variables[var]
                    if isinstance(value, str):
                        return '"' + value + '"'
                    else:
                        return str(value)
                if var.endswith("$"):
                    return '""'
                else:
                    return var

            expr = re.sub(r"\b[A-Za-z_]\w*\$?\b", replace_undefined_var, expr)
            # Replace $ with _DOLLAR for function names
            expr = expr.replace("$", "_DOLLAR")
            # Replace custom functions
            expr = expr.replace("RND(1)", str(random.random()))
            expr = expr.replace("RND()", str(random.random()))

            result = eval(expr, safe_dict)
            return result
        except SyntaxError as e:
            self.log_output(f"Syntax error in expression '{expr}': {e}")
            return 0
        except Exception as e:
            self.log_output(f"Expression error: {e}")
            return 0

    def interpolate_text(self, text: str) -> str:
        """Interpolate *VAR* tokens and evaluate *expr* tokens inside a text string.

        This central helper is used by T: and MT: to keep interpolation logic
        consistent and reduce duplication.
        """
        # First replace explicit variable occurrences like *VAR*
        for var_name, var_value in self.variables.items():
            text = text.replace(f"*{var_name}*", str(var_value))

        # Then evaluate expression-like tokens remaining between *...*
        try:
            tokens = re.findall(r"\*(.+?)\*", text)
            for tok in tokens:
                # If we've already replaced this as a variable, skip
                if tok in self.variables:
                    continue
                tok_stripped = tok.strip()
                # If token looks like a numeric literal, just use it
                if re.fullmatch(r"[-+]?\d+(?:\.\d+)?", tok_stripped):
                    text = text.replace(f"*{tok}*", tok_stripped)
                    continue
                # Heuristic: if token contains expression characters, try to eval
                if re.search(r"[\(\)\+\-\*/%<>=]", tok):
                    try:
                        val = self.evaluate_expression(tok)
                        text = text.replace(f"*{tok}*", str(val))
                    except Exception:
                        # leave token as-is on error
                        pass
        except Exception:
            pass

        return text

    def get_user_input(self, prompt=""):
        """Get input from user"""
        if self.output_widget:
            # Use dialog for GUI environment
            result = simpledialog.askstring("Input", prompt)
            return result if result is not None else ""
        else:
            # Use console input for command line
            return input(prompt)

    def execute_pilot_command(self, command):
        """Execute PILOT commands"""
        try:
            # Determine the command prefix up to the first colon (e.g., T:, A:, MT:)
            colon_idx = command.find(":")
            if colon_idx != -1:
                cmd_type = command[: colon_idx + 1]
            else:
                cmd_type = command[:2] if len(command) > 1 else command

            if cmd_type == "T:":
                # Text output
                text = command[2:].strip()
                # If the previous command set a match (Y: or N:), then this T: is
                # treated as conditional and only prints when match_flag is True.
                if self._last_match_set:
                    # consume the sentinel
                    self._last_match_set = False
                    if not self.match_flag:
                        # do not print when match is false
                        return "continue"

                text = self.interpolate_text(text)
                self.log_output(text)
                return "continue"

            elif cmd_type == "A:":
                # Accept input
                var_name = command[2:].strip()
                prompt = f"Enter value for {var_name}: "
                value = self.get_user_input(prompt).strip()
                try:
                    val = self.evaluate_expression(value)
                    self.variables[var_name] = val
                except Exception:
                    self.variables[var_name] = value
                return "continue"

            elif cmd_type == "Y:":
                # Match if condition is true
                condition = command[2:].strip()
                try:
                    result = self.evaluate_expression(condition)
                    self.match_flag = bool(result)
                except Exception as e:
                    self.match_flag = False
                    self.log_output(f"Error in Y: condition '{condition}': {e}")
                # mark that the last command set the match flag so a following T: can be conditional
                self._last_match_set = True
                return "continue"

            elif cmd_type == "N:":
                # Match if condition is false
                condition = command[2:].strip()
                try:
                    result = self.evaluate_expression(condition)
                    # N: treat like a plain conditional (match when the condition is TRUE).
                    # Many existing examples and tests use N: as an alternate test
                    # rather than the logical negation of Y:, so keep it as a standard
                    # conditional that sets the match flag to the evaluated result.
                    self.match_flag = bool(result)
                except Exception as e:
                    # On error, default to no match
                    self.match_flag = False
                    self.log_output(f"Error in N: condition '{condition}': {e}")
                # mark that the last command set the match flag so a following T: can be conditional
                self._last_match_set = True
                return "continue"

            elif cmd_type == "J:":
                # Jump to label
                label = command[2:].strip()
                # If the previous command set a match (Y: or N:), treat this J:
                # as conditional: consume the sentinel and only jump when
                # match_flag is True. This matches examples that write
                # "Y:cond" followed by "J:label" as a conditional jump.
                if self._last_match_set:
                    # consume sentinel
                    self._last_match_set = False
                    if not self.match_flag:
                        return "continue"
                if label in self.labels:
                    return f"jump:{self.labels[label]}"
                return "continue"

            elif cmd_type == "M:":
                # Jump if match flag is set
                label = command[2:].strip()
                if self.match_flag and label in self.labels:
                    return f"jump:{self.labels[label]}"
                return "continue"
            elif cmd_type == "MT:":
                # Match-conditional text output: only output when match_flag is True
                text = command[3:].strip()
                if self.match_flag:
                    text = self.interpolate_text(text)
                    self.log_output(text)
                return "continue"

            elif cmd_type == "R:":
                # Extended runtime commands (from templecode.py)
                arg_upper = command[2:].strip().upper()
                if arg_upper.startswith("SND "):
                    # R: SND name=file.wav
                    m = re.search(
                        r'name\s*=\s*"([^"]+)"\s*,\s*file\s*=\s*"([^"]+)"',
                        command[2:],
                        re.IGNORECASE,
                    )
                    if m:
                        name, path = m.groups()
                        self.audio_mixer.register_sound(name, path)
                        self.log_output(f"Sound '{name}' registered")
                    else:
                        self.log_output(
                            'Invalid SND syntax: R: SND name="soundname", file="path.wav"'
                        )
                elif arg_upper.startswith("PLAY "):
                    # R: PLAY "soundname"
                    m = re.search(r"\"([^\"]+)\"", command[2:])
                    if m:
                        name = m.group(1)
                        self.audio_mixer.play_sound(name)
                        self.log_output(f"Playing sound '{name}'")
                    else:
                        self.log_output('Invalid PLAY syntax: R: PLAY "soundname"')
                elif arg_upper.startswith("SAVE "):
                    # R: SAVE "slotname"
                    m = re.search(r"\"([^\"]+)\"", command[2:])
                    if m:
                        slot = m.group(1)
                        # Save current state
                        import os

                        save_dir = os.path.expanduser("~/.time_warp_saves")
                        os.makedirs(save_dir, exist_ok=True)
                        save_path = os.path.join(save_dir, f"{slot}.json")
                        import json

                        state = {
                            "variables": self.variables,
                            "turtle_x": self.turtle_x,
                            "turtle_y": self.turtle_y,
                            "turtle_heading": self.turtle_heading,
                            "pen_down": self.pen_down,
                            "pen_color": self.pen_color,
                            "pen_width": self.pen_width,
                        }
                        with open(save_path, "w") as f:
                            json.dump(state, f)
                        self.log_output(f"Game saved to slot '{slot}'")
                    else:
                        self.log_output('Invalid SAVE syntax: R: SAVE "slotname"')
                elif arg_upper.startswith("LOAD "):
                    # R: LOAD "slotname"
                    m = re.search(r"\"([^\"]+)\"", command[2:])
                    if m:
                        slot = m.group(1)
                        import os

                        save_path = os.path.expanduser(
                            f"~/.time_warp_saves/{slot}.json"
                        )
                        if os.path.exists(save_path):
                            import json

                            with open(save_path, "r") as f:
                                state = json.load(f)
                            self.variables.update(state.get("variables", {}))
                            self.turtle_x = state.get("turtle_x", 200)
                            self.turtle_y = state.get("turtle_y", 200)
                            self.turtle_heading = state.get("turtle_heading", 90)
                            self.pen_down = state.get("pen_down", True)
                            self.pen_color = state.get("pen_color", "black")
                            self.pen_width = state.get("pen_width", 1)
                            self.log_output(f"Game loaded from slot '{slot}'")
                        else:
                            self.log_output(f"Save slot '{slot}' not found")
                    else:
                        self.log_output('Invalid LOAD syntax: R: LOAD "slotname"')
                else:
                    # Default: treat as gosub (subroutine call)
                    label = command[2:].strip()
                    self.stack.append(self.current_line + 1)
                    if label in self.labels:
                        return f"jump:{self.labels[label]}"
                    return "continue"

            elif cmd_type == "C:":
                # Return from subroutine
                if self.stack:
                    return f"jump:{self.stack.pop()}"
                return "continue"

            elif cmd_type == "L:":
                # Label - do nothing
                return "continue"

            elif cmd_type == "U:":
                # Update variable
                assignment = command[2:].strip()
                if "=" in assignment:
                    var_name, expr = assignment.split("=", 1)
                    var_name = var_name.strip()
                    expr = expr.strip()
                    try:
                        value = self.evaluate_expression(expr)
                        self.variables[var_name] = value
                    except Exception as e:
                        self.log_output(f"Error in assignment {assignment}: {e}")
                return "continue"

            elif command.strip().upper() == "END":
                # End program
                return "end"

        except Exception as e:
            self.log_output(f"PILOT command error: {e}")
            return "continue"

        return "continue"

    def execute_basic_command(self, command):
        """Execute BASIC-like commands"""
        try:
            parts = command.split()
            if not parts:
                return "continue"

            cmd = parts[0].upper()

            if cmd == "LET":
                # Variable assignment
                if "=" in command:
                    _, assignment = command.split(" ", 1)
                    if "=" in assignment:
                        var_name, expr = assignment.split("=", 1)
                        var_name = var_name.strip()
                        expr = expr.strip()
                        try:
                            value = self.evaluate_expression(expr)
                            self.variables[var_name] = value
                        except Exception as e:
                            self.log_output(f"Error in LET {assignment}: {e}")
                return "continue"
            elif cmd == "IF":
                # IF condition THEN command  - evaluate condition, execute then-part if true
                try:
                    m = re.match(r"IF\s+(.+?)\s+THEN\s+(.+)", command, re.IGNORECASE)
                    if m:
                        cond_expr = m.group(1).strip()
                        then_cmd = m.group(2).strip()
                        try:
                            cond_val = self.evaluate_expression(cond_expr)
                        except Exception:
                            cond_val = False
                        if cond_val:
                            # Execute the THEN command using the general line executor so
                            # it can be a BASIC, PILOT or LOGO command fragment.
                            return self.execute_line(then_cmd)
                except Exception as e:
                    self.log_output(f"IF statement error: {e}")
                return "continue"
            elif cmd == "FOR":
                # FOR var = start TO end [STEP step]
                try:
                    m = re.match(
                        r"FOR\s+([A-Za-z_]\w*)\s*=\s*(.+?)\s+TO\s+(.+?)(?:\s+STEP\s+(.+))?$",
                        command,
                        re.IGNORECASE,
                    )
                    if m:
                        var_name = m.group(1)
                        start_expr = m.group(2).strip()
                        end_expr = m.group(3).strip()
                        step_expr = m.group(4).strip() if m.group(4) else None

                        start_val = self.evaluate_expression(start_expr)
                        end_val = self.evaluate_expression(end_expr)
                        step_val = (
                            self.evaluate_expression(step_expr)
                            if step_expr is not None
                            else 1
                        )

                        # Integer-only loops: coerce start/end/step to int
                        try:
                            start_val = int(start_val)
                        except Exception:
                            start_val = 0
                        try:
                            end_val = int(end_val)
                        except Exception:
                            end_val = 0
                        try:
                            step_val = int(step_val)
                        except Exception:
                            step_val = 1

                        # Store the loop variable and position
                        self.variables[var_name] = start_val
                        self.for_stack.append(
                            {
                                "var": var_name,
                                "end": end_val,
                                "step": step_val,
                                "for_line": self.current_line,
                            }
                        )
                except Exception as e:
                    self.log_output(f"FOR statement error: {e}")
                return "continue"

            elif cmd == "PRINT":
                # Print output
                text = command[5:].strip()
                parts = text.split(";")
                results = []
                for part in parts:
                    part = part.strip()
                    if part.startswith('"') and part.endswith('"'):
                        results.append(part[1:-1])
                    else:
                        try:
                            val = self.evaluate_expression(part)
                            results.append(str(val))
                        except Exception as e:
                            results.append(part)
                result = "".join(results)
                self.log_output(result)
                return "continue"
            elif cmd == "REM":
                # Comment - ignore rest of the line
                return "continue"
            elif cmd == "END":
                return "end"

            elif cmd == "INPUT":
                # Get user input
                # Parse INPUT [prompt;] var
                input_part = command[5:].strip()  # remove 'INPUT'
                if ";" in input_part:
                    prompt_part, var_part = input_part.split(";", 1)
                    prompt = prompt_part.strip().strip('"').strip("'")
                    var_name = var_part.strip()
                else:
                    var_name = input_part.strip()
                    prompt = f"Enter value for {var_name}: "
                value = self.get_user_input(prompt).strip()
                try:
                    val = self.evaluate_expression(value)
                    self.variables[var_name] = val
                except Exception:
                    self.variables[var_name] = value
                return "continue"

            elif cmd == "GOTO":
                # Jump to line number
                if len(parts) > 1:
                    line_num = int(parts[1])
                    for i, (num, _) in enumerate(self.program_lines):
                        if num == line_num:
                            return f"jump:{i}"
                return "continue"

            elif cmd == "GOSUB":
                # Push return address and jump to line number
                if len(parts) > 1:
                    line_num = int(parts[1])
                    # push next-line index
                    self.stack.append(self.current_line + 1)
                    for i, (num, _) in enumerate(self.program_lines):
                        if num == line_num:
                            return f"jump:{i}"
                return "continue"

            elif cmd == "RETURN":
                # Return from GOSUB
                if self.stack:
                    return f"jump:{self.stack.pop()}"
                return "continue"

            elif cmd == "NEXT":
                # NEXT [var]
                try:
                    parts = command.split()
                    var_spec = parts[1] if len(parts) > 1 else None

                    # Find matching FOR on the stack
                    if not self.for_stack:
                        self.log_output("NEXT without FOR")
                        return "continue"

                    # If var specified, search from top for match, else take top
                    if var_spec:
                        # strip possible commas
                        var_spec = var_spec.strip()
                        found_idx = None
                        for i in range(len(self.for_stack) - 1, -1, -1):
                            if self.for_stack[i]["var"].upper() == var_spec.upper():
                                found_idx = i
                                break
                        if found_idx is None:
                            self.log_output(f"NEXT for unknown variable {var_spec}")
                            return "continue"
                        ctx = self.for_stack[found_idx]
                        # remove any inner loops above this one? keep nested intact
                        # Only pop if loop finishes
                    else:
                        ctx = self.for_stack[-1]
                        found_idx = len(self.for_stack) - 1

                    var_name = ctx["var"]
                    step = int(ctx["step"])
                    end_val = int(ctx["end"])

                    # Ensure variable exists (treat as integer)
                    current_val = self.variables.get(var_name, 0)
                    try:
                        current_val = int(current_val)
                    except Exception:
                        current_val = 0

                    next_val = current_val + step
                    self.variables[var_name] = int(next_val)

                    # Decide whether to loop
                    loop_again = False
                    try:
                        if step >= 0:
                            loop_again = next_val <= int(end_val)
                        else:
                            loop_again = next_val >= int(end_val)
                    except Exception:
                        loop_again = False

                    if loop_again:
                        # jump to line after FOR statement
                        for_line = ctx["for_line"]
                        return f"jump:{for_line+1}"
                    else:
                        # pop this FOR from stack
                        try:
                            self.for_stack.pop(found_idx)
                        except Exception:
                            pass
                except Exception as e:
                    self.log_output(f"NEXT statement error: {e}")
                return "continue"

            # GW-BASIC Graphics Commands
            elif cmd == "SCREEN":
                # SCREEN [mode] [, [burst] [, [active_page] [, visible_page]]]
                try:
                    args = command[6:].strip()  # Remove 'SCREEN'
                    if args:
                        # Parse arguments separated by commas
                        screen_args = [arg.strip() for arg in args.split(",")]
                        mode = (
                            int(self.evaluate_expression(screen_args[0]))
                            if screen_args[0]
                            else 0
                        )

                        # For now, we support basic screen modes
                        # Mode 0: Text mode (default)
                        # Mode 1-7: Graphics modes (we'll treat them as graphics enabled)
                        if mode == 0:
                            # Text mode - could disable graphics if needed
                            pass
                        else:
                            # Graphics mode - ensure graphics are enabled
                            if not self.graphics_widget:
                                self.log_output(
                                    "Graphics not available in this environment"
                                )
                    else:
                        # Default screen mode
                        pass
                except Exception as e:
                    self.log_output(f"SCREEN statement error: {e}")
                return "continue"

            elif cmd == "COLOR":
                # COLOR [foreground] [, background]
                try:
                    args = command[5:].strip()  # Remove 'COLOR'
                    if args:
                        color_args = [arg.strip() for arg in args.split(",")]
                        if len(color_args) >= 1 and color_args[0]:
                            fg_color = int(self.evaluate_expression(color_args[0]))
                            self.pen_color = self.colors[fg_color % len(self.colors)]
                        if len(color_args) >= 2 and color_args[1]:
                            bg_color = int(self.evaluate_expression(color_args[1]))
                            # Set background color if canvas available
                            if self.graphics_widget:
                                bg_hex = self.colors[bg_color % len(self.colors)]
                                self.graphics_widget.config(bg=bg_hex)
                except Exception as e:
                    self.log_output(f"COLOR statement error: {e}")
                return "continue"

            elif cmd == "PALETTE":
                # PALETTE [attribute, color]
                # For simplicity, we'll just log this for now
                try:
                    args = command[7:].strip()  # Remove 'PALETTE'
                    if args:
                        palette_args = [arg.strip() for arg in args.split(",")]
                        if len(palette_args) >= 2:
                            attr = int(self.evaluate_expression(palette_args[0]))
                            color = int(self.evaluate_expression(palette_args[1]))
                            self.log_output(
                                f"Palette attribute {attr} set to color {color}"
                            )
                except Exception as e:
                    self.log_output(f"PALETTE statement error: {e}")
                return "continue"

            elif cmd == "PSET":
                # PSET [STEP] (x, y) [, color]
                try:
                    args = command[4:].strip()  # Remove 'PSET'
                    if args:
                        # Parse STEP option and coordinates
                        step_mode = args.upper().startswith("STEP")
                        if step_mode:
                            args = args[4:].strip()  # Remove 'STEP'

                        # Extract coordinates and optional color
                        coord_match = re.search(r"\(\s*([^,]+)\s*,\s*([^)]+)\)", args)
                        if coord_match:
                            x_expr = coord_match.group(1).strip()
                            y_expr = coord_match.group(2).strip()
                            x = self.evaluate_expression(x_expr)
                            y = self.evaluate_expression(y_expr)

                            # Check for optional color
                            remaining = args[coord_match.end() :].strip()
                            color = None
                            if remaining.startswith(","):
                                color_expr = remaining[1:].strip()
                                color = int(self.evaluate_expression(color_expr))
                                color_name = self.colors[color % len(self.colors)]
                            else:
                                color_name = self.pen_color

                            if step_mode:
                                x += self.turtle_x
                                y += self.turtle_y

                            # Draw point
                            if self.graphics_widget:
                                canvas_x = self.origin_x + x
                                canvas_y = self.origin_y - y
                                self.graphics_widget.create_oval(
                                    canvas_x - 1,
                                    canvas_y - 1,
                                    canvas_x + 1,
                                    canvas_y + 1,
                                    fill=color_name,
                                    outline=color_name,
                                    tags="graphics",
                                )
                                self.graphics_widget.update()
                except Exception as e:
                    self.log_output(f"PSET statement error: {e}")
                return "continue"

            elif cmd == "PRESET":
                # PRESET [STEP] (x, y) [, color]
                try:
                    args = command[6:].strip()  # Remove 'PRESET'
                    if args:
                        # Parse STEP option and coordinates
                        step_mode = args.upper().startswith("STEP")
                        if step_mode:
                            args = args[4:].strip()  # Remove 'STEP'

                        # Extract coordinates and optional color
                        coord_match = re.search(r"\(\s*([^,]+)\s*,\s*([^)]+)\)", args)
                        if coord_match:
                            x_expr = coord_match.group(1).strip()
                            y_expr = coord_match.group(2).strip()
                            x = self.evaluate_expression(x_expr)
                            y = self.evaluate_expression(y_expr)

                            if step_mode:
                                x += self.turtle_x
                                y += self.turtle_y

                            # Erase point (draw background color)
                            if self.graphics_widget:
                                canvas_x = self.origin_x + x
                                canvas_y = self.origin_y - y
                                bg_color = self.graphics_widget.cget("bg")
                                self.graphics_widget.create_oval(
                                    canvas_x - 1,
                                    canvas_y - 1,
                                    canvas_x + 1,
                                    canvas_y + 1,
                                    fill=bg_color,
                                    outline=bg_color,
                                    tags="graphics",
                                )
                                self.graphics_widget.update()
                except Exception as e:
                    self.log_output(f"PRESET statement error: {e}")
                return "continue"

            elif cmd == "CIRCLE":
                # CIRCLE [STEP] (x, y), radius [, [color] [, [start] [, [end] [, aspect]]]]
                try:
                    args = command[6:].strip()  # Remove 'CIRCLE'
                    if args:
                        # Parse STEP option
                        step_mode = args.upper().startswith("STEP")
                        if step_mode:
                            args = args[4:].strip()  # Remove 'STEP'

                        # Parse the complex CIRCLE syntax
                        # Format: (x, y), radius [, color [, start [, end [, aspect]]]]
                        parts = args.split(",")
                        if len(parts) >= 3:
                            coord_part = parts[0].strip()
                            radius_part = parts[1].strip()

                            # Extract coordinates
                            coord_match = re.search(
                                r"\(\s*([^,]+)\s*,\s*([^)]+)\)", coord_part
                            )
                            if coord_match:
                                x_expr = coord_match.group(1).strip()
                                y_expr = coord_match.group(2).strip()
                                x = self.evaluate_expression(x_expr)
                                y = self.evaluate_expression(y_expr)

                                if step_mode:
                                    x += self.turtle_x
                                    y += self.turtle_y

                                radius = self.evaluate_expression(radius_part)

                                # Optional parameters
                                color = self.pen_color
                                start_angle = 0
                                end_angle = 360
                                aspect = 1.0

                                if len(parts) >= 3:
                                    color_val = self.evaluate_expression(
                                        parts[2].strip()
                                    )
                                    color = self.colors[
                                        int(color_val) % len(self.colors)
                                    ]

                                # Draw circle
                                self.draw_circle_at(
                                    x, y, radius, color, start_angle, end_angle, aspect
                                )
                except Exception as e:
                    self.log_output(f"CIRCLE statement error: {e}")
                return "continue"

            elif cmd == "DRAW":
                # DRAW string_expression
                try:
                    args = command[4:].strip()  # Remove 'DRAW'
                    if args.startswith('"') and args.endswith('"'):
                        draw_string = args[1:-1]
                        self.execute_draw_commands(draw_string)
                except Exception as e:
                    self.log_output(f"DRAW statement error: {e}")
                return "continue"

            elif cmd == "PAINT":
                # PAINT [STEP] (x, y) [, [paint_color] [, [border_color] [, background]]]
                try:
                    args = command[5:].strip()  # Remove 'PAINT'
                    if args:
                        # Parse STEP option
                        step_mode = args.upper().startswith("STEP")
                        if step_mode:
                            args = args[4:].strip()  # Remove 'STEP'

                        # Parse coordinates
                        coord_match = re.search(r"\(\s*([^,]+)\s*,\s*([^)]+)\)", args)
                        if coord_match:
                            x_expr = coord_match.group(1).strip()
                            y_expr = coord_match.group(2).strip()
                            x = self.evaluate_expression(x_expr)
                            y = self.evaluate_expression(y_expr)

                            if step_mode:
                                x += self.turtle_x
                                y += self.turtle_y

                            # Optional paint color
                            paint_color = self.pen_color
                            remaining = args[coord_match.end() :].strip()
                            if remaining.startswith(","):
                                color_part = remaining[1:].strip().split(",")[0].strip()
                                if color_part:
                                    color_val = int(
                                        self.evaluate_expression(color_part)
                                    )
                                    paint_color = self.colors[
                                        color_val % len(self.colors)
                                    ]

                            # Fill area (simplified implementation)
                            if self.graphics_widget:
                                canvas_x = self.origin_x + x
                                canvas_y = self.origin_y - y
                                # For simplicity, we'll just draw a filled circle at the point
                                # A full implementation would do flood fill
                                self.graphics_widget.create_oval(
                                    canvas_x - 10,
                                    canvas_y - 10,
                                    canvas_x + 10,
                                    canvas_y + 10,
                                    fill=paint_color,
                                    outline=paint_color,
                                    tags="graphics",
                                )
                                self.graphics_widget.update()
                except Exception as e:
                    self.log_output(f"PAINT statement error: {e}")
                return "continue"

            # GW-BASIC Sound and Music Commands
            elif cmd == "PLAY":
                # PLAY string_expression
                try:
                    args = command[4:].strip()  # Remove 'PLAY'
                    if args.startswith('"') and args.endswith('"'):
                        music_string = args[1:-1]
                        self.play_music_string(music_string)
                except Exception as e:
                    self.log_output(f"PLAY statement error: {e}")
                return "continue"

            elif cmd == "SOUND":
                # SOUND frequency, duration [, volume [, voice]]
                try:
                    args = command[5:].strip()  # Remove 'SOUND'
                    if args:
                        sound_args = [arg.strip() for arg in args.split(",")]
                        if len(sound_args) >= 2:
                            frequency = self.evaluate_expression(sound_args[0])
                            duration = self.evaluate_expression(sound_args[1])
                            volume = 255  # Default maximum volume
                            voice = 0  # Default voice

                            if len(sound_args) >= 3:
                                volume = int(self.evaluate_expression(sound_args[2]))
                            if len(sound_args) >= 4:
                                voice = int(self.evaluate_expression(sound_args[3]))

                            self.play_sound(frequency, duration, volume, voice)
                except Exception as e:
                    self.log_output(f"SOUND statement error: {e}")
                return "continue"

            elif cmd == "BEEP":
                # BEEP - Simple beep sound
                try:
                    self.audio_mixer.play_sound("beep")
                except Exception as e:
                    # Fallback to system beep
                    self.log_output("\a", end="")
                return "continue"

            # Placeholder implementations for missing GW-BASIC features
            elif cmd == "OBJECT":
                # Placeholder for OBJECT command
                self.log_output("OBJECT command not implemented yet")
                return "continue"
            elif cmd == "DEF":
                # Placeholder for DEF OBJECT
                self.log_output("DEF OBJECT command not implemented yet")
                return "continue"
            elif cmd == "ACTIVATE":
                # Placeholder for ACTIVATE command
                self.log_output("ACTIVATE command not implemented yet")
                return "continue"
            elif cmd == "ON":
                # Placeholder for ON event GOSUB
                self.log_output("ON event trapping not implemented yet")
                return "continue"
            elif cmd == "OPEN":
                # Placeholder for OPEN file
                self.log_output("File I/O not implemented yet")
                return "continue"
            elif cmd == "CLOSE":
                # Placeholder for CLOSE file
                self.log_output("File I/O not implemented yet")
                return "continue"
            elif cmd == "GET":
                # Placeholder for GET file
                self.log_output("File I/O not implemented yet")
                return "continue"
            elif cmd == "PUT":
                # Placeholder for PUT file
                self.log_output("File I/O not implemented yet")
                return "continue"
            elif cmd == "BLOAD":
                # Placeholder for BLOAD
                self.log_output("BLOAD not implemented yet")
                return "continue"
            elif cmd == "BSAVE":
                # Placeholder for BSAVE
                self.log_output("BSAVE not implemented yet")
                return "continue"
            elif cmd == "CHAIN":
                # Placeholder for CHAIN
                self.log_output("CHAIN not implemented yet")
                return "continue"
            elif cmd == "COMMON":
                # Placeholder for COMMON
                self.log_output("COMMON not implemented yet")
                return "continue"
            elif cmd == "ERASE":
                # Placeholder for ERASE
                self.log_output("ERASE not implemented yet")
                return "continue"
            elif cmd == "RANDOMIZE":
                # RANDOMIZE [seed] - Seed the random number generator
                try:
                    args = command[9:].strip()  # Remove 'RANDOMIZE'
                    if args:
                        seed = self.evaluate_expression(args)
                        random.seed(seed)
                        self.log_output(f"Random seed set to {seed}")
                    else:
                        # Use current time as seed
                        import time

                        random.seed(time.time())
                        self.log_output("Random seed set to current time")
                except Exception as e:
                    self.log_output(f"RANDOMIZE statement error: {e}")
                return "continue"
            elif cmd == "SWAP":
                # SWAP var1, var2 - Exchange values of two variables
                try:
                    args = command[4:].strip()  # Remove 'SWAP'
                    if "," in args:
                        var1, var2 = [v.strip() for v in args.split(",", 1)]
                        if var1 in self.variables and var2 in self.variables:
                            # Swap the values
                            temp = self.variables[var1]
                            self.variables[var1] = self.variables[var2]
                            self.variables[var2] = temp
                            self.log_output(f"Swapped {var1} and {var2}")
                        else:
                            self.log_output(f"Variables {var1} and/or {var2} not found")
                    else:
                        self.log_output(
                            "SWAP requires two variables separated by comma"
                        )
                except Exception as e:
                    self.log_output(f"SWAP statement error: {e}")
                return "continue"
            elif cmd == "CALL":
                # Placeholder for CALL assembly
                self.log_output("Assembly integration not implemented yet")
                return "continue"
            elif cmd == "USR":
                # Placeholder for USR function
                self.log_output("Assembly integration not implemented yet")
                return "continue"
            elif cmd == "PEEK":
                # Placeholder for PEEK
                self.log_output("System functions not implemented yet")
                return "continue"
            elif cmd == "POKE":
                # Placeholder for POKE
                self.log_output("System functions not implemented yet")
                return "continue"
            elif cmd == "WAIT":
                # WAIT seconds - Pause execution for specified seconds
                try:
                    args = command[4:].strip()  # Remove 'WAIT'
                    if args:
                        seconds = self.evaluate_expression(args)
                        import time

                        time.sleep(float(seconds))
                        self.log_output(f"Waited {seconds} seconds")
                    else:
                        self.log_output("WAIT requires seconds value")
                except Exception as e:
                    self.log_output(f"WAIT statement error: {e}")
                return "continue"
            elif cmd == "INKEY$":
                # INKEY$ - Return pressed key or empty string
                try:
                    # Simulate by prompting for input
                    key = input("Press a key: ").strip()
                    if key:
                        self.variables["INKEY$"] = key[0]  # First char only
                    else:
                        self.variables["INKEY$"] = ""
                    self.log_output(f"INKEY$ returned: '{self.variables['INKEY$']}'")
                except Exception as e:
                    self.log_output(f"INKEY$ error: {e}")
                    self.variables["INKEY$"] = ""
                return "continue"
            elif cmd == "STICK":
                # Placeholder for STICK
                self.log_output("STICK not implemented yet")
                return "continue"
            elif cmd == "STRIG":
                # Placeholder for STRIG
                self.log_output("STRIG not implemented yet")
                return "continue"
            elif cmd == "DATA":
                # DATA value1, value2, ... - Store data values for READ
                try:
                    args = command[4:].strip()  # Remove 'DATA'
                    if args:
                        # Parse comma-separated values
                        data_values = []
                        for item in args.split(","):
                            item = item.strip()
                            if item.startswith('"') and item.endswith('"'):
                                # String literal
                                data_values.append(item[1:-1])
                            else:
                                # Try to evaluate as expression
                                try:
                                    val = self.evaluate_expression(item)
                                    data_values.append(val)
                                except Exception:
                                    data_values.append(item)
                        # Add to data list
                        self.data_list.extend(data_values)
                except Exception as e:
                    self.log_output(f"DATA statement error: {e}")
                return "continue"
            elif cmd == "READ":
                # READ var1, var2, ... - Read values from DATA into variables
                try:
                    args = command[4:].strip()  # Remove 'READ'
                    if args:
                        var_names = [v.strip() for v in args.split(",")]
                        for var_name in var_names:
                            if self.data_pointer < len(self.data_list):
                                value = self.data_list[self.data_pointer]
                                self.variables[var_name] = value
                                self.data_pointer += 1
                            else:
                                self.log_output(
                                    f"Out of data in READ for variable {var_name}"
                                )
                                break
                except Exception as e:
                    self.log_output(f"READ statement error: {e}")
                return "continue"
            elif cmd == "RESTORE":
                # RESTORE [line] - Reset data pointer, optionally to specific line
                try:
                    args = command[7:].strip()  # Remove 'RESTORE'
                    if args:
                        # Try to parse as line number (not implemented yet)
                        self.log_output("RESTORE with line number not implemented yet")
                    # Reset data pointer to beginning
                    self.data_pointer = 0
                except Exception as e:
                    self.log_output(f"RESTORE statement error: {e}")
                return "continue"

        except Exception as e:
            self.log_output(f"BASIC command error: {e}")
            return "continue"

        return "continue"

    def execute_logo_command(self, command):
        """Execute Logo-like commands"""
        try:
            parts = command.upper().split()
            if not parts:
                return "continue"

            cmd = parts[0]

            if cmd in ["FORWARD", "FD"]:
                if len(parts) > 1:
                    distance = self.evaluate_expression(parts[1])
                    self.move_turtle(distance)
            elif cmd in ["BACK", "BK"]:
                if len(parts) > 1:
                    distance = self.evaluate_expression(parts[1])
                    self.move_turtle(-distance)
            elif cmd in ["LEFT", "LT"]:
                if len(parts) > 1:
                    degrees = self.evaluate_expression(parts[1])
                    self.turtle_heading -= degrees
            elif cmd in ["RIGHT", "RT"]:
                if len(parts) > 1:
                    degrees = self.evaluate_expression(parts[1])
                    self.turtle_heading += degrees
            elif cmd in ["PENUP", "PU"]:
                self.pen_down = False
            elif cmd in ["PENDOWN", "PD"]:
                self.pen_down = True
            elif cmd in ["CLEARSCREEN", "CS"]:
                if self.graphics_widget:
                    self.graphics_widget.delete("all")
                self.reset_turtle()
            elif cmd == "HOME":
                self.reset_turtle()
            elif cmd == "SETXY":
                if len(parts) > 2:
                    x = self.evaluate_expression(parts[1])
                    y = self.evaluate_expression(parts[2])
                    self.turtle_x = x
                    self.turtle_y = y

            elif cmd == "SETX":
                if len(parts) > 1:
                    x = self.evaluate_expression(parts[1])
                    self.turtle_x = x
            elif cmd == "SETY":
                if len(parts) > 1:
                    y = self.evaluate_expression(parts[1])
                    self.turtle_y = y
            elif cmd in ["PENCOLOR", "PC"]:
                if len(parts) > 1:
                    color_arg = parts[1]
                    if color_arg.isdigit():
                        index = int(color_arg) % len(self.colors)
                        self.pen_color = self.colors[index]
                    else:
                        self.pen_color = color_arg
            elif cmd == "PENSIZE":
                if len(parts) > 1:
                    size = self.evaluate_expression(parts[1])
                    self.pen_width = max(1, int(size))
            elif cmd in ["HIDETURTLE", "HT"]:
                # Turtle visibility - for now just log since we don't draw turtle cursor
                self.log_output("Turtle hidden")
            elif cmd in ["SHOWTURTLE", "ST"]:
                # Turtle visibility - for now just log since we don't draw turtle cursor
                self.log_output("Turtle shown")
            elif cmd in ["SETHEADING", "SETH"]:
                if len(parts) > 1:
                    heading = self.evaluate_expression(parts[1])
                    self.turtle_heading = heading
            elif cmd == "CIRCLE":
                if len(parts) > 1:
                    radius = self.evaluate_expression(parts[1])
                    extent = (
                        self.evaluate_expression(parts[2]) if len(parts) > 2 else 360
                    )
                    self.draw_circle(radius, extent)
            elif cmd == "RECT":
                if len(parts) > 2:
                    width = self.evaluate_expression(parts[1])
                    height = self.evaluate_expression(parts[2])
                    self.draw_rectangle(width, height)
            elif cmd == "DOT":
                if len(parts) > 1:
                    size = self.evaluate_expression(parts[1])
                    self.draw_dot(size)
            elif cmd == "IMAGE":
                if len(parts) > 1:
                    path = parts[1].strip('"').strip("'")
                    width = (
                        self.evaluate_expression(parts[2]) if len(parts) > 2 else None
                    )
                    height = (
                        self.evaluate_expression(parts[3]) if len(parts) > 3 else None
                    )
                    self.draw_image(path, width, height)
            elif cmd == "HUD":
                self.toggle_hud()
            elif cmd == "SNAPSHOT":
                if len(parts) > 1:
                    filename = parts[1].strip('"').strip("'")
                    self.take_snapshot(filename)
            elif cmd == "SPRITENEW":
                if len(parts) > 2:
                    name = parts[1]
                    path = parts[2].strip('"').strip("'")
                    self.create_sprite(name, path)
            elif cmd == "SPRITEPOS":
                if len(parts) > 3:
                    name = parts[1]
                    x = self.evaluate_expression(parts[2])
                    y = self.evaluate_expression(parts[3])
                    self.set_sprite_position(name, x, y)
            elif cmd == "SPRITEDRAW":
                if len(parts) > 1:
                    name = parts[1]
                    self.draw_sprite(name)

        except Exception as e:
            self.log_output(f"Logo command error: {e}")
            return "continue"

    def determine_command_type(self, command):
        """Determine which language the command belongs to"""
        command = command.strip()

        # PILOT commands start with a letter followed by colon
        if len(command) > 1 and command[1] == ":":
            return "pilot"

        # Logo commands
        logo_commands = [
            "FORWARD",
            "FD",
            "BACK",
            "BK",
            "LEFT",
            "LT",
            "RIGHT",
            "RT",
            "PENUP",
            "PU",
            "PENDOWN",
            "PD",
            "CLEARSCREEN",
            "CS",
            "HOME",
            "SETXY",
            "SETX",
            "SETY",
            "SETHEADING",
            "SETH",
            "SETCOLOR",
            "PENCOLOR",
            "PC",
            "PENSIZE",
            "HIDETURTLE",
            "HT",
            "SHOWTURTLE",
            "ST",
            "CLEARTEXT",
            "CT",
        ]
        if command.split()[0].upper() in logo_commands:
            return "logo"

        # BASIC commands
        basic_commands = [
            "LET",
            "PRINT",
            "INPUT",
            "GOTO",
            "IF",
            "THEN",
            "FOR",
            "TO",
            "NEXT",
            "GOSUB",
            "RETURN",
            "END",
            "REM",
            "SCREEN",
            "COLOR",
            "PALETTE",
            "PSET",
            "PRESET",
            "CIRCLE",
            "DRAW",
            "PAINT",
            "PLAY",
            "SOUND",
            "BEEP",
            "OBJECT",
            "DEF",
            "ACTIVATE",
            "ON",
            "OPEN",
            "CLOSE",
            "GET",
            "PUT",
            "BLOAD",
            "BSAVE",
            "CHAIN",
            "COMMON",
            "ERASE",
            "RANDOMIZE",
            "SWAP",
            "CALL",
            "USR",
            "PEEK",
            "POKE",
            "WAIT",
            "INKEY$",
            "STICK",
            "STRIG",
            "DATA",
            "READ",
            "RESTORE",
        ]
        if command.split()[0].upper() in basic_commands:
            return "basic"

        # Default to PILOT for simple commands
        return "pilot"

    def execute_line(self, line):
        """Execute a single line of code"""
        line_num, command = self.parse_line(line)

        if not command:
            return "continue"

        parts = command.split()
        if parts and parts[0].upper() in self.procedures:
            proc = self.procedures[parts[0].upper()]
            args = parts[1:]
            if len(args) != len(proc["params"]):
                self.log_output(
                    f"Procedure {parts[0]} expects {len(proc['params'])} args, got {len(args)}"
                )
                return "continue"
            old_vars = self.variables.copy()
            for param, arg in zip(proc["params"], args):
                self.variables[param] = self.evaluate_expression(arg)
            for body_line in proc["body"]:
                result = self.execute_line(body_line)
                if result == "end":
                    break
            self.variables = old_vars
            return "continue"

        if parts and parts[0].upper() in ["TO", "END"]:
            return "continue"

        # Determine command type and execute
        cmd_type = self.determine_command_type(command)

        if cmd_type == "pilot":
            return self.execute_pilot_command(command)
        elif cmd_type == "basic":
            return self.execute_basic_command(command)
        elif cmd_type == "logo":
            return self.execute_logo_command(command)

        return "continue"

    def load_program(self, program_text):
        """Load and parse a program"""
        self.reset()
        lines = program_text.strip().split("\n")

        # Parse lines and collect labels
        self.program_lines = []
        for i, line in enumerate(lines):
            line_num, command = self.parse_line(line)
            self.program_lines.append((line_num, command))

            # Collect PILOT labels
            if command.startswith("L:"):
                label = command[2:].strip()
                self.labels[label] = i

        # Parse procedures
        self.procedures = {}
        i = 0
        while i < len(self.program_lines):
            _, command = self.program_lines[i]
            if command.upper().startswith("TO "):
                parts = command.split()
                name = parts[1].upper()
                params = parts[2:] if len(parts) > 2 else []
                body = []
                i += 1
                while (
                    i < len(self.program_lines)
                    and self.program_lines[i][1].upper() != "END"
                ):
                    body.append(self.program_lines[i][1])
                    i += 1
                self.procedures[name] = {"params": params, "body": body}
            else:
                i += 1

        return True

    def run_program(self, program_text):
        """Run a complete program"""
        if not self.load_program(program_text):
            self.log_output("Error loading program")
            return False

        self.running = True
        self.current_line = 0
        iterations = 0

        try:
            while (
                self.current_line < len(self.program_lines)
                and self.running
                and iterations < self.max_iterations
            ):
                iterations += 1

                if self.debug_mode and self.current_line in self.breakpoints:
                    self.log_output(f"Breakpoint hit at line {self.current_line}")
                    # In a real debugger, this would pause execution

                line_num, command = self.program_lines[self.current_line]

                # Skip empty lines
                if not command.strip():
                    self.current_line += 1
                    continue

                result = self.execute_line(command)

                if result == "end":
                    break
                elif result.startswith("jump:"):
                    try:
                        jump_target = int(result.split(":")[1])
                        self.current_line = jump_target
                        continue
                    except Exception as e:
                        self.log_output(f"Error parsing jump target: {e}")
                elif result == "error":
                    self.log_output("Program terminated due to error")
                    break

                self.current_line += 1

            if iterations >= self.max_iterations:
                self.log_output("Program stopped: Maximum iterations reached")
                return False

        except Exception as e:
            self.log_output(f"Runtime error: {e}")
        finally:
            self.running = False
            self.log_output("Program execution completed")

        return True

    def step(self):
        """Execute a single line and pause (for debugger stepping)."""
        if not self.program_lines:
            return
        if self.current_line >= len(self.program_lines):
            return
        line_num, command = self.program_lines[self.current_line]
        result = self.execute_line(command)
        if result.startswith("jump:"):
            try:
                jump_target = int(result.split(":")[1])
                self.current_line = jump_target
                return
            except Exception:
                pass
        elif result == "end":
            self.running = False
            return
        self.current_line += 1

    def continue_running(self):
        """Continue running until breakpoint or end."""
        self.running = True
        max_iterations = 10000
        iterations = 0
        try:
            while (
                self.current_line < len(self.program_lines)
                and self.running
                and iterations < max_iterations
            ):
                iterations += 1
                if self.debug_mode and self.current_line in self.breakpoints:
                    # Pause at breakpoint
                    break
                self.step()
            if iterations >= max_iterations:
                self.log_output("Program stopped: Maximum iterations reached")
        except Exception as e:
            self.log_output(f"Runtime error during continue: {e}")

    def stop_program(self):
        """Stop program execution"""
        self.running = False

    def set_debug_mode(self, enabled):
        """Enable/disable debug mode"""
        self.debug_mode = enabled

    def toggle_breakpoint(self, line_number):
        """Toggle breakpoint at line"""
        if line_number in self.breakpoints:
            self.breakpoints.remove(line_number)
        else:
            self.breakpoints.add(line_number)

    def parse_bracketed_commands(self, commands_str):
        """Parse Logo commands from bracketed string, handling nested brackets"""
        cmd_list = []
        i = 0
        while i < len(commands_str):
            # Skip whitespace
            while i < len(commands_str) and commands_str[i].isspace():
                i += 1
            if i >= len(commands_str):
                break

            # Check for known commands that take parameters
            if commands_str[i : i + 2].upper() in ["FD", "BK", "LT", "RT"]:
                # These commands take one parameter
                cmd = commands_str[i : i + 2]
                i += 2
                # Skip whitespace
                while i < len(commands_str) and commands_str[i].isspace():
                    i += 1
                # Find the parameter (until next space or end)
                param_start = i
                while i < len(commands_str) and not commands_str[i].isspace():
                    i += 1
                param = commands_str[param_start:i]
                cmd_list.append(f"{cmd} {param}")
            elif commands_str[i : i + 8].upper() == "SETCOLOR":
                cmd = "SETCOLOR"
                i += 8
                # Skip whitespace
                while i < len(commands_str) and commands_str[i].isspace():
                    i += 1
                # Find the parameter
                param_start = i
                while i < len(commands_str) and not commands_str[i].isspace():
                    i += 1
                param = commands_str[param_start:i]
                cmd_list.append(f"{cmd} {param}")
            elif commands_str[i : i + 6].upper() == "REPEAT":
                # Handle nested REPEAT
                cmd = "REPEAT"
                i += 6
                # Skip whitespace
                while i < len(commands_str) and commands_str[i].isspace():
                    i += 1
                # Find the count parameter
                count_start = i
                while i < len(commands_str) and not commands_str[i].isspace():
                    i += 1
                count = commands_str[count_start:i]
                # Skip whitespace to [
                while i < len(commands_str) and commands_str[i].isspace():
                    i += 1
                if i < len(commands_str) and commands_str[i] == "[":
                    i += 1  # skip [
                    # Find matching closing ]
                    bracket_count = 1
                    nested_start = i
                    while i < len(commands_str) and bracket_count > 0:
                        if commands_str[i] == "[":
                            bracket_count += 1
                        elif commands_str[i] == "]":
                            bracket_count -= 1
                        i += 1
                    nested_commands = commands_str[nested_start : i - 1]  # exclude ]
                    cmd_list.append(f"{cmd} {count} [ {nested_commands} ]")
                else:
                    # Malformed, skip
                    i += 1
            else:
                # Single command without parameters
                single_cmds = ["PENUP", "PENDOWN", "CLEARSCREEN", "HOME"]
                found = False
                for sc in single_cmds:
                    if commands_str[i : i + len(sc)].upper() == sc:
                        cmd_list.append(sc)
                        i += len(sc)
                        found = True
                        break
                if not found:
                    # Unknown, skip character
                    i += 1

        return cmd_list


class IntelligentCodeCompletion:
    """Advanced code completion system for Time Warp IDE"""

    def __init__(self, text_widget, ide):
        self.text_widget = text_widget
        self.ide = ide
        self.completion_window = None
        self.current_word = ""
        self.completion_start = None

        # Command definitions with context and descriptions
        self.pilot_commands = {
            "T:": {
                "desc": "Text output - Display text to the user",
                "context": "text_output",
                "example": "T:Hello World!",
            },
            "A:": {
                "desc": "Accept input - Get input from user into variable",
                "context": "user_input",
                "example": "A:NAME",
            },
            "Y:": {
                "desc": "Yes condition - Set match flag if condition is true",
                "context": "conditional",
                "example": "Y:AGE > 18",
            },
            "N:": {
                "desc": "No condition - Set match flag if condition is false",
                "context": "conditional",
                "example": "N:AGE < 18",
            },
            "J:": {
                "desc": "Jump - Go to label or conditional jump",
                "context": "flow_control",
                "example": "J:LABEL or J(condition):LABEL",
            },
            "M:": {
                "desc": "Match - Pattern matching for text input",
                "context": "pattern_match",
                "example": "M:YES,OK,SURE",
            },
            "R:": {
                "desc": "Runtime/Resource command - Advanced features",
                "context": "advanced",
                "example": "R:ARDUINO CONNECT",
            },
            "ML:": {
                "desc": "Machine Learning command - AI/ML operations",
                "context": "ml",
                "example": "ML:LOAD mymodel linear_regression",
            },
            "GAME:": {
                "desc": "Game Development command - Create and control game objects",
                "context": "game",
                "example": "GAME:CREATE player sprite 100 100",
            },
            "C:": {
                "desc": "Compute/Call - Calculate expression or call subroutine",
                "context": "computation",
                "example": "C:RESULT = X + Y",
            },
            "L:": {
                "desc": "Label - Define a program location",
                "context": "label",
                "example": "L:START",
            },
            "U:": {
                "desc": "Use/Update - Set variable value",
                "context": "variable",
                "example": "U:COUNT=10",
            },
            "END": {
                "desc": "End program execution",
                "context": "flow_control",
                "example": "END",
            },
            "E:": {
                "desc": "End program execution (short form)",
                "context": "flow_control",
                "example": "E:",
            },
        }

        # ML subcommands for PILOT
        self.pilot_ml_commands = {
            "ML:LOAD": {
                "desc": "Load ML model",
                "context": "ml_load",
                "example": "ML:LOAD mymodel linear_regression",
            },
            "ML:DATA": {
                "desc": "Create sample dataset",
                "context": "ml_data",
                "example": "ML:DATA mydata linear",
            },
            "ML:TRAIN": {
                "desc": "Train ML model",
                "context": "ml_train",
                "example": "ML:TRAIN mymodel mydata",
            },
            "ML:PREDICT": {
                "desc": "Make prediction",
                "context": "ml_predict",
                "example": "ML:PREDICT mymodel 5.0,3.2 RESULT",
            },
            "ML:EVALUATE": {
                "desc": "Evaluate model performance",
                "context": "ml_eval",
                "example": "ML:EVALUATE mymodel testdata SCORE",
            },
            "ML:LIST": {
                "desc": "List models or data",
                "context": "ml_list",
                "example": "ML:LIST MODELS",
            },
            "ML:CLEAR": {
                "desc": "Clear all ML data",
                "context": "ml_clear",
                "example": "ML:CLEAR",
            },
            "ML:INFO": {
                "desc": "Get model information",
                "context": "ml_info",
                "example": "ML:INFO mymodel",
            },
            "ML:DEMO": {
                "desc": "Run ML demonstration",
                "context": "ml_demo",
                "example": "ML:DEMO linear",
            },
        }

        # Game Development commands for PILOT
        self.pilot_game_commands = {
            "GAME:CREATE": {
                "desc": "Create game object",
                "context": "game_create",
                "example": "GAME:CREATE player sprite 100 100 32 32",
            },
            "GAME:MOVE": {
                "desc": "Move game object",
                "context": "game_move",
                "example": "GAME:MOVE player 10 0 5",
            },
            "GAME:PHYSICS": {
                "desc": "Set physics properties",
                "context": "game_physics",
                "example": "GAME:PHYSICS GRAVITY 9.8",
            },
            "GAME:COLLISION": {
                "desc": "Check collision between objects",
                "context": "game_collision",
                "example": "GAME:COLLISION CHECK player enemy HIT",
            },
            "GAME:RENDER": {
                "desc": "Render game scene",
                "context": "game_render",
                "example": "GAME:RENDER",
            },
            "GAME:UPDATE": {
                "desc": "Update game physics",
                "context": "game_update",
                "example": "GAME:UPDATE 0.016",
            },
            "GAME:DELETE": {
                "desc": "Delete game object",
                "context": "game_delete",
                "example": "GAME:DELETE enemy1",
            },
            "GAME:LIST": {
                "desc": "List all game objects",
                "context": "game_list",
                "example": "GAME:LIST",
            },
            "GAME:CLEAR": {
                "desc": "Clear all game objects",
                "context": "game_clear",
                "example": "GAME:CLEAR",
            },
            "GAME:INFO": {
                "desc": "Get object information",
                "context": "game_info",
                "example": "GAME:INFO player",
            },
            "GAME:DEMO": {
                "desc": "Run game demonstration",
                "context": "game_demo",
                "example": "GAME:DEMO pong",
            },
        }

        self.logo_commands = {
            "FORWARD": {
                "desc": "Move turtle forward by specified distance",
                "context": "movement",
                "example": "FORWARD 100",
            },
            "FD": {
                "desc": "Move turtle forward (short form)",
                "context": "movement",
                "example": "FD 50",
            },
            "BACK": {
                "desc": "Move turtle backward by specified distance",
                "context": "movement",
                "example": "BACK 50",
            },
            "BK": {
                "desc": "Move turtle backward (short form)",
                "context": "movement",
                "example": "BK 30",
            },
            "LEFT": {
                "desc": "Turn turtle left by degrees",
                "context": "rotation",
                "example": "LEFT 90",
            },
            "LT": {
                "desc": "Turn turtle left (short form)",
                "context": "rotation",
                "example": "LT 45",
            },
            "RIGHT": {
                "desc": "Turn turtle right by degrees",
                "context": "rotation",
                "example": "RIGHT 90",
            },
            "RT": {
                "desc": "Turn turtle right (short form)",
                "context": "rotation",
                "example": "RT 45",
            },
            "PENUP": {
                "desc": "Lift pen (stop drawing)",
                "context": "pen_control",
                "example": "PENUP",
            },
            "PU": {
                "desc": "Lift pen (short form)",
                "context": "pen_control",
                "example": "PU",
            },
            "PENDOWN": {
                "desc": "Lower pen (start drawing)",
                "context": "pen_control",
                "example": "PENDOWN",
            },
            "PD": {
                "desc": "Lower pen (short form)",
                "context": "pen_control",
                "example": "PD",
            },
            "CLEARSCREEN": {
                "desc": "Clear the graphics canvas",
                "context": "canvas",
                "example": "CLEARSCREEN",
            },
            "CS": {
                "desc": "Clear screen (short form)",
                "context": "canvas",
                "example": "CS",
            },
            "HOME": {
                "desc": "Move turtle to center (0,0)",
                "context": "positioning",
                "example": "HOME",
            },
            "SETXY": {
                "desc": "Set turtle position to coordinates",
                "context": "positioning",
                "example": "SETXY 100 50",
            },
            "SETHEADING": {
                "desc": "Set turtle heading in degrees",
                "context": "rotation",
                "example": "SETHEADING 0",
            },
            "SETH": {
                "desc": "Set heading (short form)",
                "context": "rotation",
                "example": "SETH 90",
            },
            "REPEAT": {
                "desc": "Repeat commands specified number of times",
                "context": "loop",
                "example": "REPEAT 4 [FD 100 RT 90]",
            },
            "DEFINE": {
                "desc": "Define a custom procedure",
                "context": "procedure",
                "example": "DEFINE SQUARE [REPEAT 4 [FD 100 RT 90]]",
            },
            "CALL": {
                "desc": "Call a defined procedure",
                "context": "procedure",
                "example": "CALL SQUARE",
            },
            # ML Commands
            "LOADMODEL": {
                "desc": "Load machine learning model",
                "context": "ml",
                "example": "LOADMODEL mymodel linear_regression",
            },
            "CREATEDATA": {
                "desc": "Create sample ML dataset",
                "context": "ml",
                "example": "CREATEDATA mydata linear",
            },
            "TRAINMODEL": {
                "desc": "Train ML model with dataset",
                "context": "ml",
                "example": "TRAINMODEL mymodel mydata",
            },
            "PREDICT": {
                "desc": "Make ML prediction",
                "context": "ml",
                "example": "PREDICT mymodel 5.0,3.2",
            },
            "EVALUATEMODEL": {
                "desc": "Evaluate ML model performance",
                "context": "ml",
                "example": "EVALUATEMODEL mymodel testdata",
            },
            "MLDEMO": {
                "desc": "Run ML demonstration",
                "context": "ml",
                "example": "MLDEMO linear",
            },
            "LISTMODELS": {
                "desc": "List all loaded ML models",
                "context": "ml",
                "example": "LISTMODELS",
            },
            "LISTDATA": {
                "desc": "List all ML datasets",
                "context": "ml",
                "example": "LISTDATA",
            },
            "CLEARML": {
                "desc": "Clear all ML models and data",
                "context": "ml",
                "example": "CLEARML",
            },
            # Game Development Commands
            "CREATEOBJECT": {
                "desc": "Create game object",
                "context": "game",
                "example": "CREATEOBJECT player sprite 100 100 32 32",
            },
            "MOVEOBJECT": {
                "desc": "Move game object",
                "context": "game",
                "example": "MOVEOBJECT player 10 0 5",
            },
            "SETGRAVITY": {
                "desc": "Set physics gravity",
                "context": "game",
                "example": "SETGRAVITY 9.8",
            },
            "SETVELOCITY": {
                "desc": "Set object velocity",
                "context": "game",
                "example": "SETVELOCITY player 5 -10",
            },
            "CHECKCOLLISION": {
                "desc": "Check collision between objects",
                "context": "game",
                "example": "CHECKCOLLISION player enemy",
            },
            "RENDERGAME": {
                "desc": "Render game scene",
                "context": "game",
                "example": "RENDERGAME",
            },
            "UPDATEGAME": {
                "desc": "Update game physics",
                "context": "game",
                "example": "UPDATEGAME 0.016",
            },
            "GAMEDEMO": {
                "desc": "Run game demonstration",
                "context": "game",
                "example": "GAMEDEMO pong",
            },
        }

        # Bind events for code completion
        self.text_widget.bind("<KeyRelease>", self.on_key_release)
        self.text_widget.bind("<Button-1>", self.hide_completion)
        self.text_widget.bind("<Control-space>", self.show_completion)

    def on_key_release(self, event):
        """Handle key release events for triggering completion"""
        if event.keysym in ["Up", "Down", "Left", "Right", "Return", "Tab"]:
            self.hide_completion()
            return

        # Get current cursor position and word
        cursor_pos = self.text_widget.index(tk.INSERT)
        line_start = cursor_pos.split(".")[0] + ".0"
        line_text = self.text_widget.get(line_start, cursor_pos)

        # Find the current word being typed
        words = line_text.split()
        if words and not line_text.endswith(" "):
            self.current_word = words[-1].upper()
            if len(self.current_word) >= 2:  # Start completion after 2 characters
                self.show_completion_suggestions()
        else:
            self.hide_completion()

    def show_completion(self, event=None):
        """Manually trigger completion with Ctrl+Space"""
        cursor_pos = self.text_widget.index(tk.INSERT)
        line_start = cursor_pos.split(".")[0] + ".0"
        line_text = self.text_widget.get(line_start, cursor_pos)

        words = line_text.split()
        if words and not line_text.endswith(" "):
            self.current_word = words[-1].upper()
        else:
            self.current_word = ""

        self.show_completion_suggestions()

    def show_completion_suggestions(self):
        """Show completion suggestions based on current context"""
        if not self.current_word:
            return

        # Get matching commands
        suggestions = []
        all_commands = {
            **self.pilot_commands,
            **self.logo_commands,
            **self.basic_commands,
        }

        # Check for ML subcommands
        if self.current_word.startswith("ML:"):
            all_commands.update(self.pilot_ml_commands)

        # Check for Game subcommands
        if self.current_word.startswith("GAME:"):
            all_commands.update(self.pilot_game_commands)

        for cmd, info in all_commands.items():
            if cmd.startswith(self.current_word):
                suggestions.append((cmd, info))

        if not suggestions:
            self.hide_completion()
            return

        # Show completion window
        self.show_completion_window(suggestions)

    def show_completion_window(self, suggestions):
        """Display the completion popup window"""
        self.hide_completion()  # Hide any existing window

        if not suggestions:
            return

        # Create completion window
        self.completion_window = tk.Toplevel(self.text_widget)
        self.completion_window.wm_overrideredirect(True)
        self.completion_window.configure(bg="white", relief="solid", borderwidth=1)

        # Position window near cursor
        x, y, _, _ = self.text_widget.bbox(tk.INSERT)
        x += self.text_widget.winfo_rootx()
        y += self.text_widget.winfo_rooty() + 20
        self.completion_window.geometry(f"+{x}+{y}")

        # Create listbox for suggestions
        frame = tk.Frame(self.completion_window, bg="white")
        frame.pack(fill=tk.BOTH, expand=True)

        listbox = tk.Listbox(
            frame,
            height=min(8, len(suggestions)),
            font=("Consolas", 10),
            bg="white",
            selectbackground="#0078d4",
            selectforeground="white",
            borderwidth=0,
            highlightthickness=0,
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add scrollbar if needed
        if len(suggestions) > 8:
            scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            listbox.config(yscrollcommand=scrollbar.set)

        # Populate suggestions
        for cmd, info in suggestions:
            display_text = f"{cmd:<12} - {info['desc']}"
            listbox.insert(tk.END, display_text)

        # Select first item
        if suggestions:
            listbox.selection_set(0)

        # Bind events
        listbox.bind(
            "<Double-Button-1>",
            lambda e: self.insert_completion(suggestions[listbox.curselection()[0]][0]),
        )
        listbox.bind(
            "<Return>",
            lambda e: self.insert_completion(suggestions[listbox.curselection()[0]][0]),
        )
        listbox.bind("<Escape>", lambda e: self.hide_completion())

        # Focus the listbox
        listbox.focus_set()

    def insert_completion(self, command):
        """Insert selected completion into editor"""
        # Find the start position of current word
        cursor_pos = self.text_widget.index(tk.INSERT)
        line_num, col_num = cursor_pos.split(".")
        col_num = int(col_num)

        # Find start of current word
        line_text = self.text_widget.get(f"{line_num}.0", cursor_pos)
        word_start = col_num
        for i in range(col_num - 1, -1, -1):
            if i < len(line_text) and (
                line_text[i].isalnum() or line_text[i] in [":", "_"]
            ):
                word_start = i
            else:
                break

        # Replace current word with completion
        start_pos = f"{line_num}.{word_start}"
        self.text_widget.delete(start_pos, cursor_pos)
        self.text_widget.insert(start_pos, command)

        # Add space after command if appropriate
        if command.endswith(":"):
            self.text_widget.insert(tk.INSERT, " ")
        elif command in self.logo_commands or command in self.basic_commands:
            self.text_widget.insert(tk.INSERT, " ")

        self.hide_completion()

    def hide_completion(self, event=None):
        """Hide the completion window"""
        if self.completion_window:
            self.completion_window.destroy()
            self.completion_window = None

    def get_context_help(self, command):
        """Get detailed help for a command"""
        all_commands = {
            **self.pilot_commands,
            **self.logo_commands,
            **self.basic_commands,
        }
        if command in all_commands:
            info = all_commands[command]
            return f"{command}: {info['desc']}\nExample: {info['example']}"
        return None


# Integration with Time Warp IDE
class TimeWarpIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Warp IDE - Professional Edition")
        self.root.geometry("1000x700")
        # Apply a friendly theme and fonts
        self.setup_theme()

        # Initialize interpreter
        self.interpreter = TimeWarpInterpreter()

        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        # Lightweight tooltip helper
        class ToolTip:
            def __init__(self, widget, text, delay=500):
                self.widget = widget
                self.text = text
                self.delay = delay
                self.tipwindow = None
                self.id = None
                widget.bind("<Enter>", self.schedule)
                widget.bind("<Leave>", self.hide)

            def schedule(self, event=None):
                self.id = self.widget.after(self.delay, self.show)

            def show(self):
                if self.tipwindow or not self.text:
                    return
                x = self.widget.winfo_rootx() + 20
                y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
                self.tipwindow = tw = tk.Toplevel(self.widget)
                tw.wm_overrideredirect(True)
                tw.wm_geometry(f"+{x}+{y}")
                label = tk.Label(
                    tw,
                    text=self.text,
                    justify=tk.LEFT,
                    background="#ffffe0",
                    relief=tk.SOLID,
                    borderwidth=1,
                    font=("Segoe UI", 9),
                )
                label.pack(ipadx=4, ipady=2)

            def hide(self, event=None):
                if self.id:
                    try:
                        self.widget.after_cancel(self.id)
                    except Exception:
                        pass
                    self.id = None
                if self.tipwindow:
                    try:
                        self.tipwindow.destroy()
                    except Exception:
                        pass
                    self.tipwindow = None

        # Toolbar (modern, compact)
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, anchor="nw", fill=tk.X, padx=5, pady=6)
        btn_style = {"padding": (6, 3)}

        # Create a horizontal split: editor on the left, output/variables/help on the right
        self.main_pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left pane: editor container
        self.editor_container = ttk.Frame(self.main_pane)
        self.main_pane.add(self.editor_container)

        # Right pane: notebook for Output, Variables, Help
        self.right_notebook = ttk.Notebook(self.main_pane)
        self.main_pane.add(self.right_notebook)

        # Try to create professional icons using Pillow; fall back to emoji/text labels
        try:
            from tools.icon_factory import create_toolbar_icons

            icons = create_toolbar_icons(self.root, size=18)
        except Exception:
            icons = {}

        def make_btn(key, text, cmd, padx=2):
            if icons and key in icons:
                # Show both icon and text for accessibility/clarity
                b = ttk.Button(
                    toolbar,
                    image=icons[key],
                    text=text,
                    compound="left",
                    command=cmd,
                    **btn_style,
                )
                # Keep a reference to prevent garbage collection
                b.image = icons[key]
            else:
                b = ttk.Button(toolbar, text=text, command=cmd, **btn_style)
            b.pack(side=tk.LEFT, padx=padx)
            return b

        # Primary controls
        self.btn_run = make_btn("run", "Run", self.run_program)
        self.btn_stop = make_btn("stop", "Stop", self.stop_program)
        self.btn_debug = make_btn("debug", "Debug", self.debug_program)
        # Step and Continue
        self.btn_step = make_btn("debug", "Step", self.step_once)
        self.btn_continue = make_btn("run", "Continue", self.continue_execution)
        # Separator
        sep = ttk.Separator(toolbar, orient="vertical")
        sep.pack(side=tk.LEFT, fill=tk.Y, padx=8)
        self.btn_load = make_btn("load", "Load Demo", self.load_demo, padx=6)
        self.btn_save = make_btn("save", "Save", self.save_file)

        # Right-aligned help button
        help_container = ttk.Frame(toolbar)
        help_container.pack(side=tk.RIGHT)
        if icons and "help" in icons:
            self.btn_help = ttk.Button(
                help_container,
                image=icons["help"],
                text="Help",
                compound="left",
                command=lambda: messagebox.showinfo("Help", self.get_help_text()),
                padding=(6, 3),
            )
            self.btn_help.image = icons["help"]
            self.btn_help.pack(side=tk.RIGHT)
        else:
            self.btn_help = ttk.Button(
                help_container,
                text="Help",
                command=lambda: messagebox.showinfo("Help", self.get_help_text()),
                padding=(6, 3),
            )
            self.btn_help.pack(side=tk.RIGHT)

        # Add tooltips
        try:
            ToolTip(self.btn_run, "Run the program")
            ToolTip(self.btn_stop, "Stop program execution")
            ToolTip(self.btn_debug, "Run program in debug mode")
            ToolTip(self.btn_step, "Execute one line (step)")
            ToolTip(self.btn_continue, "Continue execution until breakpoint")
            ToolTip(self.btn_load, "Load the demo program")
            ToolTip(self.btn_save, "Save current file")
            ToolTip(self.btn_help, "Open language reference and help")
        except Exception:
            pass

        # Initially disable Stop/Continue while idle
        try:
            self.btn_stop.state(["disabled"])
            self.btn_continue.state(["disabled"])
        except Exception:
            pass

        # Editor area placed in left pane
        self.editor_frame = ttk.Frame(self.editor_container)
        self.editor_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Text editor
        editor_frame = ttk.Frame(self.editor_frame)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.editor = tk.Text(
            editor_frame,
            wrap=tk.NONE,
            font=("Consolas", 13),
            bg="#fbfbfd",
            fg="#102a43",
            insertbackground="#1b3a57",
            relief=tk.FLAT,
            bd=0,
        )
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbars
        y_scrollbar = ttk.Scrollbar(
            editor_frame, orient=tk.VERTICAL, command=self.editor.yview
        )
        x_scrollbar = ttk.Scrollbar(
            editor_frame, orient=tk.HORIZONTAL, command=self.editor.xview
        )
        self.editor.config(
            yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set
        )

        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Control buttons under editor
        button_frame = ttk.Frame(self.editor_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Run", command=self.run_program).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(button_frame, text="Stop", command=self.stop_program).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(button_frame, text="Debug", command=self.debug_program).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(button_frame, text="Load Demo", command=self.load_demo).pack(
            side=tk.LEFT, padx=2
        )

        # Output tab placed on the right notebook
        self.output_frame = ttk.Frame(self.right_notebook)
        self.right_notebook.add(self.output_frame, text="Output")

        self.output_text = scrolledtext.ScrolledText(
            self.output_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg="#002b36",
            fg="#eee8d5",
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Connect interpreter to output
        self.interpreter.output_widget = self.output_text

        # Status bar (bottom)
        self.status_bar = ttk.Label(self.root, text="Ready", anchor="w")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Bind editor events to update status (update_status may be defined elsewhere)
        try:
            self.editor.bind("<KeyRelease>", lambda e: self.update_status())
            self.editor.bind("<ButtonRelease>", lambda e: self.update_status())
        except Exception:
            pass

        # Variables tab on the right notebook
        self.variables_frame = ttk.Frame(self.right_notebook)
        self.right_notebook.add(self.variables_frame, text="Variables")

        self.variables_tree = ttk.Treeview(
            self.variables_frame, columns=("Value",), show="tree headings"
        )
        self.variables_tree.heading("#0", text="Variable")
        self.variables_tree.heading("Value", text="Value")
        self.variables_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Help tab on the right notebook
        self.help_frame = ttk.Frame(self.right_notebook)
        self.right_notebook.add(self.help_frame, text="Help")

        help_text = scrolledtext.ScrolledText(self.help_frame, wrap=tk.WORD)
        help_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        help_text.insert(1.0, self.get_help_text())
        help_text.config(state=tk.DISABLED, font=("Segoe UI", 10))

        # Graphics tab on the right notebook
        self.graphics_frame = ttk.Frame(self.right_notebook)
        self.right_notebook.add(self.graphics_frame, text="Graphics")

        self.canvas = tk.Canvas(self.graphics_frame, width=400, height=400, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Set canvas dimensions
        self.canvas_width = 400
        self.canvas_height = 400
        self.origin_x = self.canvas_width // 2
        self.origin_y = self.canvas_height // 2

        # Pass to interpreter
        self.interpreter.graphics_widget = self.canvas
        self.interpreter.canvas_width = self.canvas_width
        self.interpreter.canvas_height = self.canvas_height
        self.interpreter.origin_x = self.origin_x
        self.interpreter.origin_y = self.origin_y

        # Current-line highlight tag
        try:
            self.editor.tag_configure("current_line", background="#263238")
        except Exception:
            pass

    def setup_theme(self):
        """Apply simple color scheme and font choices for a modern look."""
        try:
            style = ttk.Style(self.root)
            # Use a theme that supports customization if available
            if "clam" in style.theme_names():
                style.theme_use("clam")
            style.configure(
                "TButton",
                font=("Segoe UI", 10),
                foreground="#ffffff",
                background="#007acc",
            )
            style.map("TButton", background=[("active", "#005f9e")])
            style.configure("TLabel", font=("Segoe UI", 10))
            style.configure("Treeview", font=("Segoe UI", 10))
            self.root.configure(bg="#f5f7fb")
        except Exception:
            pass

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Run menu
        run_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Run Program", command=self.run_program)
        run_menu.add_command(label="Debug Program", command=self.debug_program)
        run_menu.add_command(label="Stop Program", command=self.stop_program)

        # Examples menu
        examples_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Examples", menu=examples_menu)
        examples_menu.add_command(label="Hello World", command=self.load_hello_world)
        examples_menu.add_command(label="Math Demo", command=self.load_math_demo)
        examples_menu.add_command(label="Quiz Game", command=self.load_quiz_game)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Dark Mode", command=self.toggle_dark_mode)

    # end create_menu

    def update_status(self):
        """Update the status bar (placeholder for future use)"""
        pass

    def get_help_text(self):
        return """
TIME WARP LANGUAGE REFERENCE

=== PILOT COMMANDS ===
T:text          - Output text (variables in *VAR* format). If a T: immediately
                  follows Y: or N: the T: is conditional and only prints when the
                  match flag is set; the sentinel is consumed by this T:.
A:variable      - Accept input into variable
Y:condition     - Set the match flag when condition is TRUE (and mark the next
                  T: or J: as a conditional consumer)
N:condition     - Set the match flag when condition is TRUE (used as an
                  alternate conditional in many sample programs)
J:label         - Jump to label. If J: immediately follows a Y: or N:, it will be
                  treated as a conditional jump (consumes the sentinel and jumps
                  only when the match flag is set).
M:label         - Jump to label if match flag is set (does not consume the sentinel)
R:label         - Gosub to label (subroutine call), or extended commands:
  R: SND name="soundname", file="path.wav" - Register a sound file
  R: PLAY "soundname" - Play a registered sound
  R: SAVE "slotname" - Save current program state
  R: LOAD "slotname" - Load saved program state
C:              - Return from subroutine
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
DATA value1,value2,... - Store data values for READ
READ var1,var2,... - Read values from DATA into variables
RESTORE [line] - Reset data pointer for READ

=== GW-BASIC GRAPHICS COMMANDS ===
SCREEN [mode]  - Set screen mode (0=text, 1-7=graphics)
COLOR fg[,bg]  - Set foreground/background colors
PALETTE attr,color - Set color palette
PSET [STEP] (x,y) [,color] - Plot point at coordinates
PRESET [STEP] (x,y) [,color] - Erase point at coordinates
CIRCLE [STEP] (x,y), radius [,color [,start [,end [,aspect]]]] - Draw circle
DRAW "string"  - Execute drawing commands from string
PAINT [STEP] (x,y) [,paint_color [,border_color]] - Fill area

=== GW-BASIC SOUND COMMANDS ===
PLAY "string"  - Play music from string notation
SOUND freq, duration [,volume [,voice]] - Play tone
BEEP           - Simple beep sound

=== GW-BASIC FUNCTIONS ===
SIN(x), COS(x), TAN(x) - Trigonometric functions
LOG(x), SQR(x), EXP(x) - Logarithmic and exponential functions
ATN(x), SGN(x), ABS(x) - Arc tangent, sign, absolute value
LEFT$(s,n), RIGHT$(s,n), MID$(s,start[,length]) - String functions
INSTR(s,sub), LEN(s), CHR$(n), ASC(s) - String operations
STR$(n), VAL(s), SPACE$(n), STRING$(n,char) - Conversion functions

=== LOGO COMMANDS ===
FORWARD distance / FD distance - Move turtle forward by distance units
BACK distance / BK distance - Move turtle backward by distance units
LEFT degrees / LT degrees - Turn turtle left by degrees
RIGHT degrees / RT degrees - Turn turtle right by degrees
PENUP / PU - Lift the pen (stop drawing lines)
PENDOWN / PD - Lower the pen (start drawing lines)
PENCOLOR color / PC color - Set the color of the pen (name or number)
PENSIZE size - Set the thickness of the line drawn by the pen
HIDETURTLE / HT - Make the turtle invisible
SHOWTURTLE / ST - Make the turtle visible
CLEARSCREEN / CS - Clear all drawings and return turtle to home
CLEARTEXT / CT - Clear text from the command screen
HOME - Return turtle to center (0,0), facing up
SETXY x y - Move turtle to coordinates (x,y) without drawing
SETX x - Move turtle to specified X coordinate, keep Y
SETY y - Move turtle to specified Y coordinate, keep X
SETHEADING degrees / SETH degrees - Set turtle's heading to specified angle
REPEAT count [commands] - Execute commands count times

=== EXPRESSIONS ===