#!/usr/bin/env python3
# Time Warp Interpreter - Complete Implementation
# For integration with Time Warp IDE

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog, filedialog
import random
import math
import re
import time
from datetime import datetime

# Import plugin system
from core.plugin_system import PluginManager

# Import safe expression evaluator
from core.safe_expression_evaluator import safe_eval

# Import asyncio support
from core.async_support import (
    init_async_support,
    shutdown_async_support,
    AsyncInterpreterRunner,
    get_async_runner,
)


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

        # Logo procedures
        self.logo_procedures = {}  # Logo procedure definitions

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
        # Calculate new position
        angle_rad = math.radians(self.turtle_heading)
        new_x = self.turtle_x + distance * math.cos(angle_rad)
        new_y = self.turtle_y - distance * math.sin(angle_rad)  # Negative for up

        if self.graphics_widget:
            if self.pen_down:
                # Draw line from current to new position
                x1 = self.origin_x + self.turtle_x
                y1 = self.origin_y - self.turtle_y
                x2 = self.origin_x + new_x
                y2 = self.origin_y - new_y
                self.graphics_widget.create_line(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=self.pen_color,
                    width=self.pen_width,
                    tags="turtle",
                )
                self.graphics_widget.update()

        # Update turtle position (always, regardless of graphics)
        self.turtle_x = new_x
        self.turtle_y = new_y

        # Update HUD if enabled
        if self.hud_enabled and self.graphics_widget:
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
            raise ValueError("Expression contains forbidden characters")

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

            result = safe_eval(expr, safe_dict)
            return result
        except SyntaxError as e:
            self.log_output(f"Syntax error in expression '{expr}': {e}")
            raise e
        except Exception as e:
            self.log_output(f"Expression error: {e}")
            raise e

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
        if not command:
            return "continue"

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
                # Try to convert to number, otherwise keep as string
                try:
                    # Try int first
                    if "." not in value and "e" not in value.lower():
                        val = int(value)
                    else:
                        val = float(value)
                    self.variables[var_name] = val
                except ValueError:
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
                arg_upper = command[2:].strip().upper() if command else ""
                if arg_upper and arg_upper.startswith("SND "):
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
                elif arg_upper and arg_upper.startswith("PLAY "):
                    # R: PLAY "soundname"
                    m = re.search(r"\"([^\"]+)\"", command[2:])
                    if m:
                        name = m.group(1)
                        self.audio_mixer.play_sound(name)
                        self.log_output(f"Playing sound '{name}'")
                    else:
                        self.log_output('Invalid PLAY syntax: R: PLAY "soundname"')
                elif arg_upper and arg_upper.startswith("SAVE "):
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
                elif arg_upper and arg_upper.startswith("LOAD "):
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
                elif arg_upper.startswith("RPI "):
                    # R: RPI command - Raspberry Pi hardware simulation
                    rpi_cmd = arg_upper[4:].strip()
                    if rpi_cmd.startswith("PIN "):
                        # R: RPI PIN pin_num OUTPUT/INPUT
                        parts = rpi_cmd[4:].strip().split()
                        if len(parts) >= 2:
                            pin_num = int(self.evaluate_expression(parts[0]))
                            pin_mode = parts[1].upper()
                            self.log_output(f"RPi PIN {pin_num} {pin_mode} (sim)")
                        else:
                            self.log_output(
                                "RPI PIN syntax: R: RPI PIN number OUTPUT/INPUT"
                            )
                    elif rpi_cmd.startswith("WRITE "):
                        # R: RPI WRITE pin_num value
                        parts = rpi_cmd[6:].strip().split()
                        if len(parts) >= 2:
                            pin_num = int(self.evaluate_expression(parts[0]))
                            value = int(self.evaluate_expression(parts[1]))
                            self.log_output(f"RPi WRITE {pin_num}={value} (sim)")
                        else:
                            self.log_output("RPI WRITE syntax: R: RPI WRITE pin value")
                    elif rpi_cmd.startswith("READ "):
                        # R: RPI READ pin_num variable
                        parts = rpi_cmd[5:].strip().split()
                        if len(parts) >= 2:
                            pin_num = int(self.evaluate_expression(parts[0]))
                            var_name = parts[1]
                            # Simulate reading a value (0 or 1)
                            simulated_value = 0  # Always return 0 in simulation
                            self.variables[var_name] = simulated_value
                            self.log_output(
                                f"RPi READ {pin_num}={simulated_value} (sim)"
                            )
                        else:
                            self.log_output("RPI READ syntax: R: RPI READ pin variable")
                    else:
                        self.log_output(f"Unknown RPI command: {rpi_cmd}")
                elif arg_upper.startswith("ARDUINO "):
                    # R: ARDUINO command - Arduino hardware simulation
                    arduino_cmd = arg_upper[8:].strip()
                    if arduino_cmd.startswith("CONNECT "):
                        # R: ARDUINO CONNECT port baud
                        parts = arduino_cmd[8:].strip().split()
                        if len(parts) >= 2:
                            port = parts[0]
                            baud = int(self.evaluate_expression(parts[1]))
                            self.log_output(
                                f"Arduino CONNECT {port} {baud} (simulated)"
                            )
                        else:
                            self.log_output(
                                "ARDUINO CONNECT syntax: R: ARDUINO CONNECT port baud"
                            )
                    elif arduino_cmd.startswith("SEND "):
                        # R: ARDUINO SEND "message"
                        message = arduino_cmd[5:].strip().strip('"').strip("'")
                        self.log_output(f"Arduino SEND '{message}' (simulated)")
                    elif arduino_cmd.startswith("READ "):
                        # R: ARDUINO READ variable
                        var_name = arduino_cmd[5:].strip()
                        # Simulate reading sensor data
                        simulated_data = "SIMULATED_SENSOR_DATA"
                        self.variables[var_name] = simulated_data
                        self.log_output(
                            f"Arduino READ = '{simulated_data}' (simulated)"
                        )
                    else:
                        self.log_output(f"Unknown ARDUINO command: {arduino_cmd}")
                elif arg_upper.startswith("ROBOT "):
                    # R: ROBOT command - Robotics hardware simulation
                    robot_cmd = arg_upper[6:].strip()
                    if robot_cmd.startswith("FORWARD "):
                        # R: ROBOT FORWARD distance
                        distance = self.evaluate_expression(robot_cmd[8:].strip())
                        self.log_output(f"Robot FORWARD {distance} (simulated)")
                    elif robot_cmd.startswith("DISTANCE "):
                        # R: ROBOT DISTANCE variable
                        var_name = robot_cmd[9:].strip()
                        # Simulate distance reading
                        simulated_distance = 50  # cm
                        self.variables[var_name] = simulated_distance
                        self.log_output(
                            f"Robot DISTANCE = {simulated_distance}cm (simulated)"
                        )
                    elif robot_cmd.startswith("LIGHT "):
                        # R: ROBOT LIGHT variable
                        var_name = robot_cmd[6:].strip()
                        # Simulate light reading
                        simulated_light = 75  # arbitrary units
                        self.variables[var_name] = simulated_light
                        self.log_output(f"Robot LIGHT = {simulated_light} (simulated)")
                    else:
                        self.log_output(f"Unknown ROBOT command: {robot_cmd}")
                elif arg_upper.startswith("CONTROLLER "):
                    # R: CONTROLLER command - Game controller simulation
                    controller_cmd = arg_upper[11:].strip()
                    if controller_cmd == "UPDATE":
                        # R: CONTROLLER UPDATE
                        self.log_output("Controller UPDATE (simulated)")
                    elif controller_cmd.startswith("BUTTON "):
                        # R: CONTROLLER BUTTON button_num variable
                        parts = controller_cmd[7:].strip().split()
                        if len(parts) >= 2:
                            button_num = int(self.evaluate_expression(parts[0]))
                            var_name = parts[1]
                            # Simulate button state (0 = not pressed, 1 = pressed)
                            simulated_state = 0
                            self.variables[var_name] = simulated_state
                            self.log_output(
                                f"Controller BUTTON {button_num} = {simulated_state} (simulated)"
                            )
                        else:
                            self.log_output(
                                "CONTROLLER BUTTON syntax: R: CONTROLLER BUTTON num variable"
                            )
                    else:
                        self.log_output(f"Unknown CONTROLLER command: {controller_cmd}")
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
                    # Check for quoted strings first
                    if (expr.startswith('"') and expr.endswith('"')) or (
                        expr.startswith("'") and expr.endswith("'")
                    ):
                        value = expr[1:-1]  # Remove quotes
                        self.variables[var_name] = value
                    else:
                        # Try to evaluate as expression
                        try:
                            value = self.evaluate_expression(expr)
                            self.variables[var_name] = value
                        except Exception as e:
                            # If evaluation fails, check if it's a security issue
                            if (
                                "forbidden" in str(e).lower()
                                or "dangerous" in str(e).lower()
                            ):
                                # Don't store dangerous expressions
                                self.log_output(f"Assignment rejected: {e}")
                                return "error"
                            else:
                                # For other errors, treat as literal string
                                value = expr  # Keep as-is
                                self.variables[var_name] = value
                return "continue"

            elif cmd_type == "GAME:":
                # Game development commands
                game_cmd = command[5:].strip().upper()  # Remove 'GAME:'

                if game_cmd.startswith("CREATE"):
                    # GAME:CREATE object_name type x y width height
                    parts = game_cmd[6:].strip().split()
                    if len(parts) >= 6:
                        obj_name = parts[0]
                        obj_type = parts[1]
                        x = self.evaluate_expression(parts[2])
                        y = self.evaluate_expression(parts[3])
                        width = self.evaluate_expression(parts[4])
                        height = self.evaluate_expression(parts[5])

                        # Initialize game objects storage if needed
                        if not hasattr(self, "game_objects"):
                            self.game_objects = {}
                        if not hasattr(self, "game_object_count"):
                            self.game_object_count = 0

                        # Create the game object
                        obj_id = self.game_object_count + 1
                        self.game_objects[obj_id] = {
                            "name": obj_name,
                            "type": obj_type,
                            "x": x,
                            "y": y,
                            "width": width,
                            "height": height,
                            "visible": True,
                            "velocity_x": 0,
                            "velocity_y": 0,
                        }
                        self.game_object_count = obj_id

                        # Set variables as expected by tests
                        self.variables["GAME_OBJECT_COUNT"] = self.game_object_count
                        self.variables[f"GAME_OBJECT_{obj_id}_NAME"] = obj_name
                        self.variables[f"GAME_OBJECT_{obj_id}_TYPE"] = obj_type
                        self.variables[f"GAME_OBJECT_{obj_id}_X"] = x
                        self.variables[f"GAME_OBJECT_{obj_id}_Y"] = y
                        self.variables[f"GAME_OBJECT_{obj_id}_WIDTH"] = width
                        self.variables[f"GAME_OBJECT_{obj_id}_HEIGHT"] = height
                        self.variables[f"GAME_OBJECT_{obj_id}_VISIBLE"] = 1
                        self.variables[f"GAME_OBJECT_{obj_id}_VELOCITY_X"] = 0
                        self.variables[f"GAME_OBJECT_{obj_id}_VELOCITY_Y"] = 0
                    else:
                        self.log_output(
                            "GAME:CREATE requires: name type x y width height"
                        )
                    return "continue"

                elif game_cmd.startswith("MOVE"):
                    # GAME:MOVE object_name dx dy speed
                    parts = game_cmd[4:].strip().split()
                    if len(parts) >= 4:
                        obj_name = parts[0]
                        dx = self.evaluate_expression(parts[1])
                        dy = self.evaluate_expression(parts[2])
                        speed = self.evaluate_expression(parts[3])

                        # Find object by name
                        obj_id = None
                        for oid, obj in self.game_objects.items():
                            if obj["name"] == obj_name:
                                obj_id = oid
                                break

                        if obj_id:
                            # Update position
                            self.game_objects[obj_id]["x"] += dx * speed
                            self.game_objects[obj_id]["y"] += dy * speed

                            # Update variables
                            self.variables[f"GAME_OBJECT_{obj_id}_X"] = (
                                self.game_objects[obj_id]["x"]
                            )
                            self.variables[f"GAME_OBJECT_{obj_id}_Y"] = (
                                self.game_objects[obj_id]["y"]
                            )
                            self.variables["GAME_LAST_MOVE_RESULT"] = 1
                        else:
                            self.variables["GAME_LAST_MOVE_RESULT"] = 0
                    else:
                        self.log_output("GAME:MOVE requires: name dx dy speed")
                    return "continue"

                elif game_cmd.startswith("PHYSICS"):
                    # GAME:PHYSICS GRAVITY value
                    parts = game_cmd[7:].strip().split()
                    if len(parts) >= 2 and parts[0] == "GRAVITY":
                        gravity = self.evaluate_expression(parts[1])
                        self.variables["GAME_GRAVITY"] = gravity
                        self.variables["GAME_PHYSICS_ENABLED"] = 1
                    else:
                        self.log_output("GAME:PHYSICS syntax: GRAVITY value")
                    return "continue"

                elif game_cmd.startswith("COLLISION"):
                    # GAME:COLLISION CHECK obj1 obj2 result_var
                    parts = game_cmd[9:].strip().split()
                    if len(parts) >= 4 and parts[0] == "CHECK":
                        obj1_name = parts[1]
                        obj2_name = parts[2]
                        result_var = parts[3]

                        # Find objects
                        obj1 = None
                        obj2 = None
                        for oid, obj in self.game_objects.items():
                            if obj["name"] == obj1_name:
                                obj1 = obj
                            elif obj["name"] == obj2_name:
                                obj2 = obj

                        if obj1 and obj2:
                            # Simple AABB collision detection
                            x_overlap = (
                                obj1["x"] < obj2["x"] + obj2["width"]
                                and obj1["x"] + obj1["width"] > obj2["x"]
                            )
                            y_overlap = (
                                obj1["y"] < obj2["y"] + obj2["height"]
                                and obj1["y"] + obj1["height"] > obj2["y"]
                            )
                            collision = x_overlap and y_overlap
                            self.variables[result_var] = 1 if collision else 0
                            self.variables["GAME_LAST_COLLISION_CHECK"] = 1
                        else:
                            self.variables[result_var] = 0
                            self.variables["GAME_LAST_COLLISION_CHECK"] = 0
                    else:
                        self.log_output(
                            "GAME:COLLISION syntax: CHECK obj1 obj2 result_var"
                        )
                    return "continue"

                elif game_cmd == "RENDER":
                    # GAME:RENDER - Update render state
                    self.variables["GAME_RENDER_FRAME"] = (
                        self.variables.get("GAME_RENDER_FRAME", 0) + 1
                    )
                    self.variables["GAME_RENDER_STATUS"] = 1
                    return "continue"

                elif game_cmd.startswith("UPDATE"):
                    # GAME:UPDATE delta_time
                    parts = game_cmd[6:].strip().split()
                    if len(parts) >= 1:
                        delta_time = self.evaluate_expression(parts[0])
                        # Apply physics to all objects
                        if hasattr(self, "game_objects"):
                            for obj_id, obj in self.game_objects.items():
                                # Apply gravity if physics enabled
                                if self.variables.get("GAME_PHYSICS_ENABLED", 0):
                                    gravity = self.variables.get("GAME_GRAVITY", 9.8)
                                    obj["velocity_y"] += gravity * delta_time
                                    obj["y"] += obj["velocity_y"] * delta_time
                                    self.variables[f"GAME_OBJECT_{obj_id}_Y"] = obj["y"]
                                    self.variables[
                                        f"GAME_OBJECT_{obj_id}_VELOCITY_Y"
                                    ] = obj["velocity_y"]
                        self.variables["GAME_UPDATE_DELTA"] = delta_time
                        self.variables["GAME_UPDATE_STATUS"] = 1
                    else:
                        self.log_output("GAME:UPDATE requires delta_time")
                    return "continue"

                elif game_cmd.startswith("DELETE"):
                    # GAME:DELETE object_name
                    parts = game_cmd[6:].strip().split()
                    if len(parts) >= 1:
                        obj_name = parts[0]
                        # Find and remove object
                        obj_id_to_remove = None
                        for oid, obj in self.game_objects.items():
                            if obj["name"] == obj_name:
                                obj_id_to_remove = oid
                                break

                        if obj_id_to_remove:
                            del self.game_objects[obj_id_to_remove]
                            # Clean up variables
                            for key in list(self.variables.keys()):
                                if key.startswith(f"GAME_OBJECT_{obj_id_to_remove}_"):
                                    del self.variables[key]
                            self.variables["GAME_OBJECT_COUNT"] = len(self.game_objects)
                            self.variables["GAME_LAST_DELETE_RESULT"] = 1
                        else:
                            self.variables["GAME_LAST_DELETE_RESULT"] = 0
                    else:
                        self.log_output("GAME:DELETE requires object_name")
                    return "continue"

                elif game_cmd == "LIST":
                    # GAME:LIST - List all objects
                    if hasattr(self, "game_objects") and self.game_objects:
                        obj_list = []
                        for obj_id, obj in self.game_objects.items():
                            obj_list.append(f"{obj['name']}({obj_id})")
                        self.variables["GAME_OBJECT_LIST"] = ",".join(obj_list)
                        self.variables["GAME_OBJECT_COUNT"] = len(self.game_objects)
                    else:
                        self.variables["GAME_OBJECT_LIST"] = ""
                        self.variables["GAME_OBJECT_COUNT"] = 0
                    return "continue"

                elif game_cmd == "CLEAR":
                    # GAME:CLEAR - Clear all game objects
                    if hasattr(self, "game_objects"):
                        self.game_objects.clear()
                    # Clean up all game variables
                    for key in list(self.variables.keys()):
                        if key.startswith("GAME_"):
                            del self.variables[key]
                    self.variables["GAME_OBJECT_COUNT"] = 0
                    self.variables["GAME_CLEAR_STATUS"] = 1
                    return "continue"

                elif game_cmd.startswith("INFO"):
                    # GAME:INFO object_name [variable_name]
                    parts = game_cmd[4:].strip().split()
                    if len(parts) >= 1:
                        obj_name = parts[0]
                        var_name = parts[1] if len(parts) > 1 else "GAME_OBJECT_INFO"
                        # Find object
                        obj_info = None
                        for oid, obj in self.game_objects.items():
                            if obj["name"] == obj_name:
                                obj_info = obj
                                obj_id = oid
                                break

                        if obj_info:
                            info_str = (
                                f"{obj_info['name']}({obj_id}): "
                                f"pos({obj_info['x']},{obj_info['y']}) "
                                f"size({obj_info['width']},{obj_info['height']}) "
                                f"type({obj_info['type']}) "
                                f"visible({1 if obj_info['visible'] else 0})"
                            )
                            self.variables[var_name] = info_str
                            self.variables["GAME_INFO_FOUND"] = 1
                        else:
                            self.variables[var_name] = "OBJECT_NOT_FOUND"
                            self.variables["GAME_INFO_FOUND"] = 0
                    else:
                        self.log_output("GAME:INFO requires object_name")
                    return "continue"

                elif game_cmd.startswith("DEMO"):
                    # GAME:DEMO demo_type
                    parts = game_cmd[4:].strip().split()
                    if len(parts) >= 1:
                        demo_type = parts[0].lower()
                        self.variables["GAME_DEMO_TYPE"] = demo_type
                        self.variables["GAME_DEMO_STATUS"] = 1
                        # Create demo objects based on type
                        if demo_type == "pong":
                            # Create paddle and ball for pong demo
                            self.variables["GAME_DEMO_PADDLE_Y"] = 200
                            self.variables["GAME_DEMO_BALL_X"] = 300
                            self.variables["GAME_DEMO_BALL_Y"] = 200
                            self.variables["GAME_DEMO_SCORE"] = 0
                        elif demo_type == "platformer":
                            # Create player and platforms
                            self.variables["GAME_DEMO_PLAYER_X"] = 100
                            self.variables["GAME_DEMO_PLAYER_Y"] = 300
                            self.variables["GAME_DEMO_LEVEL"] = 1
                    else:
                        self.log_output("GAME:DEMO requires demo_type")
                    return "continue"

                else:
                    self.log_output(f"Unknown GAME command: {game_cmd}")
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
            if not command:
                return "continue"
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
                # Try to convert to number, otherwise keep as string
                try:
                    # Try int first
                    val = int(value)
                    self.variables[var_name] = val
                except ValueError:
                    try:
                        # Try float
                        val = float(value)
                        self.variables[var_name] = val
                    except ValueError:
                        # Keep as string
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
                # OBJECT.ADD object_name, x, y, width, height - Create graphics object
                try:
                    args = command[6:].strip()  # Remove 'OBJECT'
                    if args.startswith(".ADD"):
                        params = args[4:].strip().split(",")
                        if len(params) >= 5:
                            obj_name = params[0].strip()
                            x = int(self.evaluate_expression(params[1].strip()))
                            y = int(self.evaluate_expression(params[2].strip()))
                            width = int(self.evaluate_expression(params[3].strip()))
                            height = int(self.evaluate_expression(params[4].strip()))

                            # Create object (simplified - just store in dictionary)
                            if not hasattr(self, "objects"):
                                self.objects = {}
                            self.objects[obj_name] = {
                                "x": x,
                                "y": y,
                                "width": width,
                                "height": height,
                                "visible": True,
                            }
                            self.log_output(
                                f"Created object '{obj_name}' at ({x},{y}) size {width}x{height}"
                            )
                        else:
                            self.log_output(
                                "OBJECT.ADD requires name, x, y, width, height"
                            )
                    else:
                        self.log_output(
                            "OBJECT syntax: OBJECT.ADD name, x, y, width, height"
                        )
                except Exception as e:
                    self.log_output(f"OBJECT statement error: {e}")
                return "continue"
            elif cmd == "DEF":
                # DEF FNname(params) = expression - Define user function
                try:
                    args = command[3:].strip()  # Remove 'DEF'
                    if args.startswith("FN"):
                        # Parse function definition: FNname(params) = expression
                        fn_part = args[2:]  # Remove 'FN'
                        if "=" in fn_part:
                            name_expr, expression = fn_part.split("=", 1)
                            name_expr = name_expr.strip()

                            # Extract function name and parameters
                            if "(" in name_expr and name_expr.endswith(")"):
                                func_name = name_expr[: name_expr.find("(")].strip()
                                params_str = name_expr[name_expr.find("(") + 1 : -1]

                                # Store function definition
                                if not hasattr(self, "user_functions"):
                                    self.user_functions = {}
                                self.user_functions[func_name] = {
                                    "params": (
                                        [p.strip() for p in params_str.split(",")]
                                        if params_str
                                        else []
                                    ),
                                    "expression": expression.strip(),
                                }
                                self.log_output(f"Defined function {func_name}")
                            else:
                                self.log_output(
                                    "DEF FN syntax: DEF FNname(params) = expression"
                                )
                        else:
                            self.log_output("DEF FN requires = expression")
                    else:
                        self.log_output("DEF syntax: DEF FNname(params) = expression")
                except Exception as e:
                    self.log_output(f"DEF statement error: {e}")
                return "continue"
            elif cmd == "ACTIVATE":
                # ACTIVATE object_name - Make object active/visible
                try:
                    args = command[8:].strip()  # Remove 'ACTIVATE'
                    if args:
                        obj_name = args.strip()
                        if hasattr(self, "objects") and obj_name in self.objects:
                            self.objects[obj_name]["visible"] = True
                            self.log_output(f"Activated object '{obj_name}'")
                        else:
                            self.log_output(f"Object '{obj_name}' not found")
                    else:
                        self.log_output("ACTIVATE requires object name")
                except Exception as e:
                    self.log_output(f"ACTIVATE statement error: {e}")
                return "continue"
            elif cmd == "ON":
                # ON event GOSUB line - Event trapping (simplified)
                try:
                    args = command[2:].strip()  # Remove 'ON'
                    if args:
                        parts = args.split()
                        if len(parts) >= 3 and parts[1].upper() == "GOSUB":
                            event = parts[0].upper()
                            line_num = int(self.evaluate_expression(parts[2]))

                            # Store event handler (simplified)
                            if not hasattr(self, "event_handlers"):
                                self.event_handlers = {}
                            self.event_handlers[event] = line_num
                            self.log_output(
                                f"Set {event} event handler to line {line_num}"
                            )
                        else:
                            self.log_output("ON syntax: ON event GOSUB line_number")
                    else:
                        self.log_output("ON requires event and GOSUB line")
                except Exception as e:
                    self.log_output(f"ON statement error: {e}")
                return "continue"
            elif cmd == "OPEN":
                # OPEN file_path FOR mode AS #file_number
                try:
                    args = command[4:].strip()  # Remove 'OPEN'
                    if args:
                        # Parse OPEN syntax: "filename" FOR mode AS #number
                        parts = args.split()
                        if len(parts) >= 5:
                            filename_part = parts[0].strip('"').strip("'")
                            mode = parts[2].upper()  # INPUT/OUTPUT/APPEND
                            file_num_part = parts[4]

                            if file_num_part.startswith("#"):
                                file_num = int(file_num_part[1:])
                            else:
                                file_num = int(file_num_part)

                            # Open the file
                            if mode == "INPUT":
                                file_obj = open(filename_part, "r")
                            elif mode == "OUTPUT":
                                file_obj = open(filename_part, "w")
                            elif mode == "APPEND":
                                file_obj = open(filename_part, "a")
                            else:
                                self.log_output(f"Unsupported file mode: {mode}")
                                return "continue"

                            # Store file handle
                            if not hasattr(self, "open_files"):
                                self.open_files = {}
                            self.open_files[file_num] = file_obj
                            self.log_output(
                                f"Opened file '{filename_part}' as #{file_num}"
                            )
                        else:
                            self.log_output(
                                'OPEN syntax: OPEN "filename" FOR mode AS #number'
                            )
                    else:
                        self.log_output("OPEN requires filename, mode, and file number")
                except Exception as e:
                    self.log_output(f"OPEN statement error: {e}")
                return "continue"
            elif cmd == "CLOSE":
                # CLOSE [#file_number] or CLOSE
                try:
                    args = command[5:].strip()  # Remove 'CLOSE'
                    if hasattr(self, "open_files"):
                        if args:
                            # Close specific file
                            if args.startswith("#"):
                                file_num = int(args[1:])
                            else:
                                file_num = int(args)

                            if file_num in self.open_files:
                                self.open_files[file_num].close()
                                del self.open_files[file_num]
                                self.log_output(f"Closed file #{file_num}")
                            else:
                                self.log_output(f"File #{file_num} not open")
                        else:
                            # Close all files
                            for file_num, file_obj in self.open_files.items():
                                file_obj.close()
                            self.open_files.clear()
                            self.log_output("Closed all open files")
                    else:
                        self.log_output("No files currently open")
                except Exception as e:
                    self.log_output(f"CLOSE statement error: {e}")
                return "continue"
            elif cmd == "GET":
                # GET #file_number, variable
                try:
                    args = command[3:].strip()  # Remove 'GET'
                    if hasattr(self, "open_files") and args:
                        parts = args.split(",")
                        if len(parts) >= 2:
                            file_num_part = parts[0].strip()
                            var_name = parts[1].strip()

                            if file_num_part.startswith("#"):
                                file_num = int(file_num_part[1:])
                            else:
                                file_num = int(file_num_part)

                            if file_num in self.open_files:
                                file_obj = self.open_files[file_num]
                                line = file_obj.readline()
                                if line:
                                    # Remove newline and store
                                    self.variables[var_name] = line.rstrip("\n\r")
                                    self.log_output(
                                        f"Read from file #{file_num} into {var_name}"
                                    )
                                else:
                                    self.variables[var_name] = ""  # EOF
                                    self.log_output(f"End of file #{file_num} reached")
                            else:
                                self.log_output(f"File #{file_num} not open")
                        else:
                            self.log_output("GET syntax: GET #number, variable")
                    else:
                        self.log_output("No files open or invalid GET syntax")
                except Exception as e:
                    self.log_output(f"GET statement error: {e}")
                return "continue"
            elif cmd == "PUT":
                # PUT #file_number, expression
                try:
                    args = command[3:].strip()  # Remove 'PUT'
                    if hasattr(self, "open_files") and args:
                        parts = args.split(",", 1)
                        if len(parts) >= 2:
                            file_num_part = parts[0].strip()
                            expr = parts[1].strip()

                            if file_num_part.startswith("#"):
                                file_num = int(file_num_part[1:])
                            else:
                                file_num = int(file_num_part)

                            if file_num in self.open_files:
                                file_obj = self.open_files[file_num]
                                value = self.evaluate_expression(expr)
                                file_obj.write(str(value) + "\n")
                                file_obj.flush()  # Ensure it's written
                                self.log_output(f"Wrote to file #{file_num}")
                            else:
                                self.log_output(f"File #{file_num} not open")
                        else:
                            self.log_output("PUT syntax: PUT #number, expression")
                    else:
                        self.log_output("No files open or invalid PUT syntax")
                except Exception as e:
                    self.log_output(f"PUT statement error: {e}")
                return "continue"
            elif cmd == "BLOAD":
                # BLOAD file_path, offset
                try:
                    args = command[5:].strip()  # Remove 'BLOAD'
                    if args:
                        parts = args.split(",")
                        filename = parts[0].strip().strip('"').strip("'")
                        offset = 0
                        if len(parts) > 1:
                            offset = int(self.evaluate_expression(parts[1].strip()))

                        # Read binary file
                        with open(filename, "rb") as f:
                            data = f.read()

                        # Store in memory (simplified - just log for now)
                        if not hasattr(self, "binary_data"):
                            self.binary_data = {}
                        self.binary_data[offset] = data
                        self.log_output(
                            f"Loaded {len(data)} bytes from '{filename}' at offset {offset}"
                        )
                    else:
                        self.log_output('BLOAD syntax: BLOAD "filename" [, offset]')
                except Exception as e:
                    self.log_output(f"BLOAD statement error: {e}")
                return "continue"
            elif cmd == "BSAVE":
                # BSAVE file_path, offset, length
                try:
                    args = command[5:].strip()  # Remove 'BSAVE'
                    if args:
                        parts = args.split(",")
                        if len(parts) >= 3:
                            filename = parts[0].strip().strip('"').strip("'")
                            offset = int(self.evaluate_expression(parts[1].strip()))
                            length = int(self.evaluate_expression(parts[2].strip()))

                            # Get data from memory
                            if (
                                hasattr(self, "binary_data")
                                and offset in self.binary_data
                            ):
                                data = self.binary_data[offset]
                                if length > 0:
                                    data = data[:length]

                                # Write binary file
                                with open(filename, "wb") as f:
                                    f.write(data)
                                self.log_output(
                                    f"Saved {len(data)} bytes to '{filename}'"
                                )
                            else:
                                self.log_output(f"No data available at offset {offset}")
                        else:
                            self.log_output(
                                'BSAVE syntax: BSAVE "filename", offset, length'
                            )
                    else:
                        self.log_output("BSAVE requires filename, offset, and length")
                except Exception as e:
                    self.log_output(f"BSAVE statement error: {e}")
                return "continue"
            elif cmd == "CHAIN":
                # CHAIN filename - Load and run another BASIC program
                try:
                    args = command[5:].strip()  # Remove 'CHAIN'
                    if args:
                        filename = args.strip().strip('"').strip("'")
                        self.log_output(
                            f"CHAIN to '{filename}' (simplified - would load and run new program)"
                        )
                        # In a real implementation, this would:
                        # 1. Save current COMMON variables
                        # 2. Load the new program
                        # 3. Transfer COMMON variables
                        # 4. Execute the new program
                    else:
                        self.log_output("CHAIN requires a filename")
                except Exception as e:
                    self.log_output(f"CHAIN statement error: {e}")
                return "continue"
            elif cmd == "COMMON":
                # COMMON var1, var2, ... - Mark variables to be shared with CHAINed programs
                try:
                    args = command[6:].strip()  # Remove 'COMMON'
                    if args:
                        var_names = [v.strip() for v in args.split(",")]
                        if not hasattr(self, "common_vars"):
                            self.common_vars = set()
                        self.common_vars.update(var_names)
                        self.log_output(
                            f"Marked variables as COMMON: {', '.join(var_names)}"
                        )
                    else:
                        self.log_output("COMMON requires variable names")
                except Exception as e:
                    self.log_output(f"COMMON statement error: {e}")
                return "continue"
            elif cmd == "ERASE":
                # ERASE array1, array2, ... - Delete array variables
                try:
                    args = command[5:].strip()  # Remove 'ERASE'
                    if args:
                        array_names = [v.strip() for v in args.split(",")]
                        erased = []
                        for array_name in array_names:
                            # Remove array variables (variables ending with ())
                            array_vars = [
                                k
                                for k in self.variables.keys()
                                if k.startswith(array_name + "(")
                            ]
                            for var in array_vars:
                                if var in self.variables:
                                    del self.variables[var]
                                    erased.append(var)
                        if erased:
                            self.log_output(f"Erased arrays: {', '.join(erased)}")
                        else:
                            self.log_output("No matching arrays found to erase")
                    else:
                        self.log_output("ERASE requires array names")
                except Exception as e:
                    self.log_output(f"ERASE statement error: {e}")
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
                # PEEK(address) - Read byte from memory address
                try:
                    args = command[4:].strip()  # Remove 'PEEK'
                    if args.startswith("(") and args.endswith(")"):
                        address_expr = args[1:-1].strip()
                        address = int(self.evaluate_expression(address_expr))

                        # Simulate memory access (simplified - return 0 for now)
                        # In a real implementation, this would access actual memory
                        value = 0  # Placeholder for memory read
                        self.log_output(f"PEEK({address}) returned {value}")
                        return str(value)
                    else:
                        self.log_output("PEEK syntax: PEEK(address)")
                except Exception as e:
                    self.log_output(f"PEEK function error: {e}")
                return "0"
            elif cmd == "POKE":
                # POKE address, value - Write byte to memory address
                try:
                    args = command[4:].strip()  # Remove 'POKE'
                    if args:
                        parts = args.split(",")
                        if len(parts) == 2:
                            address = int(self.evaluate_expression(parts[0].strip()))
                            value = int(self.evaluate_expression(parts[1].strip()))

                            # Simulate memory write (simplified - just log)
                            # In a real implementation, this would write to actual memory
                            self.log_output(f"POKE {address}, {value}")
                        else:
                            self.log_output("POKE syntax: POKE address, value")
                    else:
                        self.log_output("POKE requires address and value")
                except Exception as e:
                    self.log_output(f"POKE statement error: {e}")
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
                # STICK(axis) - Read joystick position (-1 to 1)
                try:
                    args = command[5:].strip()  # Remove 'STICK'
                    if args.startswith("(") and args.endswith(")"):
                        axis_expr = args[1:-1].strip()
                        axis = int(self.evaluate_expression(axis_expr))

                        # Simulate joystick input (simplified - return 0 for now)
                        # In a real implementation, this would read from actual joystick
                        value = 0.0  # Placeholder for joystick axis
                        self.log_output(f"STICK({axis}) returned {value}")
                        return str(value)
                    else:
                        self.log_output("STICK syntax: STICK(axis)")
                except Exception as e:
                    self.log_output(f"STICK function error: {e}")
                return "0"
            elif cmd == "STRIG":
                # STRIG(button) - Read joystick button state (0 or -1)
                try:
                    args = command[5:].strip()  # Remove 'STRIG'
                    if args.startswith("(") and args.endswith(")"):
                        button_expr = args[1:-1].strip()
                        button = int(self.evaluate_expression(button_expr))

                        # Simulate joystick button (simplified - return 0 for now)
                        # In a real implementation, this would read from actual joystick
                        value = 0  # Placeholder for button state (0=not pressed, -1=pressed)
                        self.log_output(f"STRIG({button}) returned {value}")
                        return str(value)
                    else:
                        self.log_output("STRIG syntax: STRIG(button)")
                except Exception as e:
                    self.log_output(f"STRIG function error: {e}")
                return "0"
            elif cmd == "NEW":
                # NEW - Clear current program and reset interpreter state
                try:
                    # Save current state for potential OLD command
                    if not hasattr(self, "saved_state"):
                        self.saved_state = None

                    # Save current state before clearing
                    self.saved_state = {
                        "variables": self.variables.copy(),
                        "labels": self.labels.copy(),
                        "procedures": self.procedures.copy(),
                        "program_lines": self.program_lines.copy(),
                        "current_line": self.current_line,
                        "stack": self.stack.copy(),
                        "for_stack": self.for_stack.copy(),
                        "match_flag": self.match_flag,
                        "_last_match_set": self._last_match_set,
                        "running": self.running,
                        "turtle_x": self.turtle_x,
                        "turtle_y": self.turtle_y,
                        "turtle_heading": self.turtle_heading,
                        "pen_down": self.pen_down,
                        "pen_color": self.pen_color,
                        "pen_width": self.pen_width,
                        "data_list": self.data_list.copy(),
                        "data_pointer": self.data_pointer,
                        "common_vars": getattr(self, "common_vars", set()).copy(),
                        "objects": getattr(self, "objects", {}).copy(),
                        "user_functions": getattr(self, "user_functions", {}).copy(),
                        "event_handlers": getattr(self, "event_handlers", {}).copy(),
                        "open_files": getattr(self, "open_files", {}).copy(),
                        "binary_data": getattr(self, "binary_data", {}).copy(),
                        "sprites": self.sprites.copy(),
                    }

                    # Reset interpreter state
                    self.reset()

                    # Clear graphics if available
                    if self.graphics_widget:
                        self.graphics_widget.delete("all")

                    self.log_output(
                        "Program cleared. Use OLD to restore previous program."
                    )
                except Exception as e:
                    self.log_output(f"NEW command error: {e}")
                return "continue"
            elif cmd == "OLD":
                # OLD - Restore previously saved program state
                try:
                    if hasattr(self, "saved_state") and self.saved_state is not None:
                        # Restore saved state
                        state = self.saved_state
                        self.variables = state.get("variables", {}).copy()
                        self.labels = state.get("labels", {}).copy()
                        self.procedures = state.get("procedures", {}).copy()
                        self.program_lines = state.get("program_lines", []).copy()
                        self.current_line = state.get("current_line", 0)
                        self.stack = state.get("stack", []).copy()
                        self.for_stack = state.get("for_stack", []).copy()
                        self.match_flag = state.get("match_flag", False)
                        self._last_match_set = state.get("_last_match_set", False)
                        self.running = state.get("running", False)

                        # Restore turtle state
                        self.turtle_x = state.get("turtle_x", 200)
                        self.turtle_y = state.get("turtle_y", 200)
                        self.turtle_heading = state.get("turtle_heading", 90)
                        self.pen_down = state.get("pen_down", True)
                        self.pen_color = state.get("pen_color", "black")
                        self.pen_width = state.get("pen_width", 1)

                        # Restore other state
                        self.data_list = state.get("data_list", []).copy()
                        self.data_pointer = state.get("data_pointer", 0)
                        self.common_vars = state.get("common_vars", set()).copy()
                        self.objects = state.get("objects", {}).copy()
                        self.user_functions = state.get("user_functions", {}).copy()
                        self.event_handlers = state.get("event_handlers", {}).copy()
                        self.open_files = state.get("open_files", {}).copy()
                        self.binary_data = state.get("binary_data", {}).copy()
                        self.sprites = state.get("sprites", {}).copy()

                        # Clear saved state after restoration
                        self.saved_state = None

                        # Redraw graphics if available
                        if self.graphics_widget:
                            self.graphics_widget.delete("all")
                            # Note: We don't restore graphics automatically as that would be complex
                            # The program would need to redraw itself

                        self.log_output("Previous program restored.")
                    else:
                        self.log_output(
                            "No previous program to restore. Use NEW first."
                        )
                except Exception as e:
                    self.log_output(f"OLD command error: {e}")
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
                        # Try to parse as line number
                        line_num = int(self.evaluate_expression(args))
                        # Find the line number in the program and set data pointer accordingly
                        # For now, just reset to beginning (simplified implementation)
                        self.data_pointer = 0
                        self.log_output(
                            f"RESTORE to line {line_num} (simplified - reset to beginning)"
                        )
                    else:
                        # Reset data pointer to beginning
                        self.data_pointer = 0
                        self.log_output("Data pointer reset to beginning")
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
            if not command:
                return "continue"
            parts = command.upper().split()
            if not parts:
                return "continue"

            cmd = parts[0]

            print(f"DEBUG: Executing Logo command: {cmd}")  # Debug print

            if cmd in ["FORWARD", "FD"]:
                if len(parts) > 1:
                    distance = self.evaluate_expression(parts[1])
                    self.move_turtle(distance)
            elif cmd in ["BACK", "BK", "BACKWARD"]:
                if len(parts) > 1:
                    distance = self.evaluate_expression(parts[1])
                    self.move_turtle(-distance)  # Move backward
            elif cmd in ["LEFT", "LT"]:
                if len(parts) > 1:
                    degrees = self.evaluate_expression(parts[1])
                    self.turtle_heading += degrees
            elif cmd in ["RIGHT", "RT"]:
                if len(parts) > 1:
                    degrees = self.evaluate_expression(parts[1])
                    self.turtle_heading -= degrees
            elif cmd in ["PENUP", "PU"]:
                self.pen_down = False
            elif cmd in ["PENDOWN", "PD"]:
                self.pen_down = True
            elif cmd in ["CLEARSCREEN", "CS"]:
                if self.graphics_widget:
                    self.graphics_widget.delete("all")
                self.reset_turtle()
            elif cmd == "HOME":
                self.turtle_x = 200
                self.turtle_y = 200
                self.turtle_heading = 90
                self.pen_down = True
                self.pen_color = "black"
                self.pen_width = 1
            elif cmd in ["SETHEADING", "SETH"]:
                if len(parts) > 1:
                    degrees = self.evaluate_expression(parts[1])
                    self.turtle_heading = degrees

            elif cmd == "SETX":
                if len(parts) > 1:
                    x = self.evaluate_expression(parts[1])
                    self.turtle_x = x
            elif cmd == "SETY":
                if len(parts) > 1:
                    y = self.evaluate_expression(parts[1])
                    self.turtle_y = y
            elif cmd == "SETXY":
                if len(parts) > 2:
                    x = self.evaluate_expression(parts[1])
                    y = self.evaluate_expression(parts[2])
                    self.turtle_x = x
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
            elif cmd in ["SETCOLOR", "SC"]:
                print(
                    f"DEBUG: SETCOLOR command detected with parts: {parts}"
                )  # Debug print
                if len(parts) > 1:
                    color_arg = parts[1]
                    print(f"DEBUG: color_arg = {color_arg}")  # Debug print
                    if color_arg.isdigit():
                        index = int(color_arg) % len(self.colors)
                        print(
                            f"DEBUG: index = {index}, color = {self.colors[index]}"
                        )  # Debug print
                        self.pen_color = self.colors[index]
                        print(
                            f"DEBUG: pen_color set to {self.pen_color}"
                        )  # Debug print
                    else:
                        self.pen_color = color_arg
            elif cmd in ["CLEARTEXT", "CT"]:
                # Clear text output
                if self.output_widget:
                    self.output_widget.delete(1.0, tk.END)
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
            elif cmd == "REPEAT":
                if len(parts) > 2:
                    count = self.evaluate_expression(parts[1])
                    # Parse the bracketed commands
                    command_str = " ".join(parts[2:])
                    if command_str.startswith("[") and command_str.endswith("]"):
                        # Remove brackets and parse commands
                        inner_commands = command_str[1:-1].strip()
                        for _ in range(int(count)):
                            # Split by spaces but preserve quoted strings and brackets
                            sub_commands = self.parse_bracketed_commands(inner_commands)
                            for sub_cmd in sub_commands:
                                if sub_cmd.strip():
                                    self.execute_logo_command(sub_cmd.strip())
            elif cmd == "TO":
                # Define a procedure: TO procname :param1 :param2 ... commands END
                if len(parts) > 1:
                    proc_name = parts[1].upper()
                    # Extract parameters from TO line (everything after proc name starting with :)
                    params = []
                    for part in parts[2:]:
                        if part.startswith(":"):
                            params.append(part[1:].upper())  # Remove : and uppercase

                    # Find the END
                    end_idx = -1
                    for i, line in enumerate(self.program_lines):
                        if (
                            i > self.current_line
                            and line[1]
                            and line[1].upper().strip() == "END"
                        ):
                            end_idx = i
                            break
                    if end_idx > self.current_line:
                        # Extract procedure body (skip the TO line itself)
                        body_lines = []
                        for i in range(self.current_line + 1, end_idx):
                            if self.program_lines[i][1]:
                                body_lines.append(self.program_lines[i][1])
                        # Store procedure with parameters
                        if not hasattr(self, "logo_procedures"):
                            self.logo_procedures = {}
                        self.logo_procedures[proc_name] = {
                            "params": params,
                            "body": body_lines,
                        }
                        # Skip to END
                        return f"jump:{end_idx}"
            elif cmd in self.logo_procedures:
                # Call a defined procedure
                proc = self.logo_procedures[cmd]
                # Handle parameters if any
                params = parts[1:] if len(parts) > 1 else []
                param_vars = {}

                # Check parameter count
                expected_params = len(proc["params"])
                if len(params) != expected_params:
                    self.display_error(
                        f"Procedure {cmd} expects {expected_params} parameters, got {len(params)}"
                    )
                    return "continue"

                # Assign parameters to variables
                for i, param_name in enumerate(proc["params"]):
                    if i < len(params):
                        param_vars[param_name] = self.evaluate_expression(params[i])

                # Execute procedure body with parameter variables
                old_vars = self.variables.copy()
                self.variables.update(param_vars)
                try:
                    for body_line in proc["body"]:
                        if body_line.strip():
                            # Substitute Logo :param syntax with actual values
                            substituted_line = body_line
                            for param_name, param_value in param_vars.items():
                                substituted_line = substituted_line.replace(
                                    f":{param_name}", str(param_value)
                                )
                            self.execute_line(substituted_line)
                finally:
                    self.variables = old_vars

        except Exception as e:
            error_msg = f"❌ Error in Logo command '{command}': {str(e)}"
            self.display_error(error_msg)
            return "continue"

    def determine_command_type(self, command):
        """Determine which language the command belongs to"""
        if not command:
            return "pilot"

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
            "BACKWARD",
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
            "REPEAT",
            "TO",
        ]
        if command.split()[0].upper() in logo_commands:
            return "logo"

        # Check if it's a Logo procedure call
        if command.split()[0].upper() in self.logo_procedures:
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

        if parts and parts[0].upper() == "END":
            return "continue"

        # Determine command type and execute
        cmd_type = self.determine_command_type(command)

        if cmd_type == "pilot":
            result = self.execute_pilot_command(command)
        elif cmd_type == "basic":
            result = self.execute_basic_command(command)
        elif cmd_type == "logo":
            result = self.execute_logo_command(command)
        else:
            result = "continue"

        # Ensure we always return a string
        return result if isinstance(result, str) else "continue"

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
            if command and command.startswith("L:"):
                label = command[2:].strip()
                self.labels[label] = i

        # Parse procedures (skip Logo TO commands as they are handled
        # during execution)
        self.procedures = {}
        i = 0
        while i < len(self.program_lines):
            _, command = self.program_lines[i]
            # Skip Logo TO commands - they are handled during execution,
            # not loading
            if (
                command
                and command.upper().startswith("TO ")
                and self.determine_command_type(command) == "logo"
            ):
                i += 1
                # Skip the procedure body until END
                while (
                    i < len(self.program_lines)
                    and self.program_lines[i][1]
                    and self.program_lines[i][1].upper() != "END"
                ):
                    i += 1
                if i < len(self.program_lines):
                    i += 1  # Skip the END
            elif command and command.upper().startswith("TO "):
                # Parse as other language procedures (if any)
                parts = command.split()
                name = parts[1].upper()
                params = parts[2:] if len(parts) > 2 else []
                body = []
                i += 1
                while (
                    i < len(self.program_lines)
                    and self.program_lines[i][1]
                    and self.program_lines[i][1].upper() != "END"
                ):
                    body.append(self.program_lines[i][1])
                    i += 1
                self.procedures[name] = {"params": params, "body": body}
            else:
                i += 1

        return True

    def execute_program(self, program_text):
        """Execute a program - wrapper for run_program"""
        return self.run_program(program_text)

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
                elif result and result.startswith("jump:"):
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
        if result and result.startswith("jump:"):
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
            elif commands_str[i : i + 6].upper() == "FORWARD":
                cmd = "FORWARD"
                i += 6
                # Skip whitespace
                while i < len(commands_str) and commands_str[i].isspace():
                    i += 1
                # Find the parameter
                param_start = i
                while i < len(commands_str) and not commands_str[i].isspace():
                    i += 1
                param = commands_str[param_start:i]
                cmd_list.append(f"{cmd} {param}")
            elif commands_str[i : i + 4].upper() == "BACK":
                cmd = "BACK"
                i += 4
                # Skip whitespace
                while i < len(commands_str) and commands_str[i].isspace():
                    i += 1
                # Find the parameter
                param_start = i
                while i < len(commands_str) and not commands_str[i].isspace():
                    i += 1
                param = commands_str[param_start:i]
                cmd_list.append(f"{cmd} {param}")
            elif commands_str[i : i + 4].upper() == "LEFT":
                cmd = "LEFT"
                i += 4
                # Skip whitespace
                while i < len(commands_str) and commands_str[i].isspace():
                    i += 1
                # Find the parameter
                param_start = i
                while i < len(commands_str) and not commands_str[i].isspace():
                    i += 1
                param = commands_str[param_start:i]
                cmd_list.append(f"{cmd} {param}")
            elif commands_str[i : i + 5].upper() == "RIGHT":
                cmd = "RIGHT"
                i += 5
                # Skip whitespace
                while i < len(commands_str) and commands_str[i].isspace():
                    i += 1
                # Find the parameter
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
            if len(self.current_word) >= 2:  # Start completion after 2 chars
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
        if self.current_word and self.current_word.startswith("ML:"):
            all_commands.update(self.pilot_ml_commands)

        # Check for Game subcommands
        if self.current_word and self.current_word.startswith("GAME:"):
            all_commands.update(self.pilot_game_commands)

        for cmd, info in all_commands.items():
            if self.current_word and cmd.startswith(self.current_word):
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


class RealTimeSyntaxChecker:
    """Real-time syntax error detection and highlighting"""

    def __init__(self, text_widget, ide):
        self.text_widget = text_widget
        self.ide = ide
        self.error_tag = "syntax_error"
        self.warning_tag = "syntax_warning"
        self.setup_error_tags()

    def setup_error_tags(self):
        """Setup text tags for error highlighting"""
        self.text_widget.tag_configure(
            self.error_tag, background="#FFE6E6", foreground="#CC0000", underline=True
        )
        self.text_widget.tag_configure(
            self.warning_tag, background="#FFF4E6", foreground="#CC6600", underline=True
        )

    def on_key_release(self, event=None):
        """Handle key release events for syntax checking"""
        # Debounce syntax checking - only check after a short delay
        if hasattr(self, "_check_timer"):
            self.text_widget.after_cancel(self._check_timer)
        self._check_timer = self.text_widget.after(
            300, self.check_syntax
        )  # Check after 300ms delay

    def check_syntax(self, event=None):
        """Check syntax of current content and highlight errors"""
        # Clear existing error highlights
        self.text_widget.tag_remove(self.error_tag, "1.0", tk.END)
        self.text_widget.tag_remove(self.warning_tag, "1.0", tk.END)

        content = self.text_widget.get("1.0", tk.END)
        lines = content.split("\n")

        errors = []
        warnings = []

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue

            # Check PILOT syntax
            pilot_errors = self.check_pilot_syntax(line, line_num)
            errors.extend(pilot_errors)

            # Check Logo syntax
            logo_errors = self.check_logo_syntax(line, line_num)
            errors.extend(logo_errors)

            # Check BASIC syntax
            basic_errors = self.check_basic_syntax(line, line_num)
            errors.extend(basic_errors)

            # Check for common issues
            common_warnings = self.check_common_issues(line, line_num)
            warnings.extend(common_warnings)

        # Highlight errors and warnings
        self.highlight_issues(errors, warnings)

        # Update status bar with error count
        if hasattr(self.ide, "status_label"):
            if errors:
                self.ide.status_label.config(
                    text=f"❌ {len(errors)} syntax errors found"
                )
            elif warnings:
                self.ide.status_label.config(text=f"⚠️ {len(warnings)} warnings")
            else:
                self.ide.status_label.config(text="✅ No syntax errors")

    def check_pilot_syntax(self, line, line_num):
        """Check PILOT command syntax"""
        errors = []

        if ":" in line and len(line) > 1:
            if line[1] == ":":  # PILOT command
                cmd = line[:2]
                payload = line[2:].strip()

                valid_pilot_cmds = [
                    "T:",
                    "A:",
                    "Y:",
                    "N:",
                    "J:",
                    "M:",
                    "R:",
                    "C:",
                    "L:",
                    "U:",
                ]

                if cmd not in valid_pilot_cmds:
                    errors.append(
                        {
                            "line": line_num,
                            "message": f"Unknown PILOT command: {cmd}",
                            "type": "error",
                        }
                    )

                # Command-specific validation
                if cmd == "J:" and payload:
                    # Check conditional jump syntax J(condition):label
                    import re

                    if "(" in payload and ")" in payload and ":" in payload:
                        match = re.match(r"^\((.+?)\):(.+)$", payload)
                        if not match:
                            errors.append(
                                {
                                    "line": line_num,
                                    "message": "Invalid conditional jump syntax. Use J(condition):label",
                                    "type": "error",
                                }
                            )
                    elif payload and not payload.isalnum():
                        # Simple jump to label - should be alphanumeric
                        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", payload):
                            errors.append(
                                {
                                    "line": line_num,
                                    "message": "Invalid label name. Use letters, numbers, and underscores only",
                                    "type": "error",
                                }
                            )

                elif cmd == "L:" and payload:
                    # Label definition - should be alphanumeric
                    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", payload):
                        errors.append(
                            {
                                "line": line_num,
                                "message": "Invalid label name. Use letters, numbers, and underscores only",
                                "type": "error",
                            }
                        )

        return errors

    def check_logo_syntax(self, line, line_num):
        """Check Logo command syntax"""
        errors = []

        words = line.upper().split()
        if not words:
            return errors

        first_word = words[0]
        logo_movement_cmds = [
            "FORWARD",
            "FD",
            "BACK",
            "BK",
            "LEFT",
            "LT",
            "RIGHT",
            "RT",
        ]
        logo_positioning_cmds = ["SETXY", "SETHEADING", "SETH"]
        logo_repeat_cmds = ["REPEAT"]

        if first_word in logo_movement_cmds:
            # Movement commands need a numeric parameter
            if len(words) < 2:
                errors.append(
                    {
                        "line": line_num,
                        "message": f"{first_word} command requires a numeric parameter",
                        "type": "error",
                    }
                )
            elif not self.is_numeric_or_variable(words[1]):
                errors.append(
                    {
                        "line": line_num,
                        "message": f"{first_word} parameter must be a number or variable",
                        "type": "error",
                    }
                )

        elif first_word in logo_positioning_cmds:
            if first_word == "SETXY" and len(words) < 3:
                errors.append(
                    {
                        "line": line_num,
                        "message": "SETXY requires two parameters (X and Y coordinates)",
                        "type": "error",
                    }
                )
            elif first_word in ["SETHEADING", "SETH"] and len(words) < 2:
                errors.append(
                    {
                        "line": line_num,
                        "message": f"{first_word} requires a numeric parameter (degrees)",
                        "type": "error",
                    }
                )

        elif first_word == "REPEAT":
            if len(words) < 3:
                errors.append(
                    {
                        "line": line_num,
                        "message": "REPEAT requires count and command list [...]",
                        "type": "error",
                    }
                )
            elif "[" not in line or "]" not in line:
                errors.append(
                    {
                        "line": line_num,
                        "message": "REPEAT commands must be enclosed in brackets [...]",
                        "type": "error",
                    }
                )

        return errors

    def check_basic_syntax(self, line, line_num):
        """Check BASIC syntax"""
        errors = []

        # Check for line numbers at start
        words = line.split()
        if words and words[0].isdigit():
            # BASIC line with line number
            if len(words) < 2:
                errors.append(
                    {
                        "line": line_num,
                        "message": "Line number must be followed by a command",
                        "type": "error",
                    }
                )
            else:
                command = words[1].upper()
                basic_cmds = [
                    "LET",
                    "PRINT",
                    "INPUT",
                    "GOTO",
                    "IF",
                    "FOR",
                    "GOSUB",
                    "RETURN",
                    "END",
                    "REM",
                ]

                if command not in basic_cmds:
                    errors.append(
                        {
                            "line": line_num,
                            "message": f"Unknown BASIC command: {command}",
                            "type": "error",
                        }
                    )

                # Command-specific validation
                if command == "LET" and "=" not in line:
                    errors.append(
                        {
                            "line": line_num,
                            "message": "LET statement requires assignment with =",
                            "type": "error",
                        }
                    )
                elif command == "GOTO" and len(words) < 3:
                    errors.append(
                        {
                            "line": line_num,
                            "message": "GOTO requires a line number",
                            "type": "error",
                        }
                    )

        return errors

    def check_common_issues(self, line, line_num):
        """Check for common programming issues"""
        warnings = []

        # Check for potential variable naming issues
        if "*" in line:
            # Variable interpolation - check for proper format
            import re

            vars_in_line = re.findall(r"\*([^*]+)\*", line)
            for var in vars_in_line:
                if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", var):
                    warnings.append(
                        {
                            "line": line_num,
                            "message": f"Variable name '{var}' should use letters, numbers, and underscores only",
                            "type": "warning",
                        }
                    )

        # Check for missing colons in PILOT commands
        if len(line) >= 2 and line[1] in "TAYNMJRCLU" and line[1] != ":":
            warnings.append(
                {
                    "line": line_num,
                    "message": "PILOT commands should end with colon (:)",
                    "type": "warning",
                }
            )

        return warnings

    def is_numeric_or_variable(self, value):
        """Check if value is numeric or a valid variable reference"""
        # Check if it's a number
        try:
            float(value)
            return True
        except ValueError:
            pass

        # Check if it's a variable (contains *)
        if "*" in value:
            return True

        # Check if it's a valid identifier
        import re

        return bool(re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", value))

    def highlight_issues(self, errors, warnings):
        """Highlight errors and warnings in the text"""
        for error in errors:
            line_start = f"{error['line']}.0"
            line_end = f"{error['line']}.end"
            self.text_widget.tag_add(self.error_tag, line_start, line_end)

        for warning in warnings:
            line_start = f"{warning['line']}.0"
            line_end = f"{warning['line']}.end"
            self.text_widget.tag_add(self.warning_tag, line_start, line_end)


class CodeFoldingSystem:
    """Code folding system for collapsing/expanding code blocks"""

    def __init__(self, text_widget, line_numbers_widget, ide):
        self.text_widget = text_widget
        self.line_numbers_widget = line_numbers_widget
        self.ide = ide
        self.folded_blocks = {}  # {start_line: end_line}
        self.fold_markers = {}  # {line: marker_widget}
        self.setup_folding()

    def setup_folding(self):
        """Setup code folding functionality"""
        # Configure folding tags
        self.text_widget.tag_configure("folded", elide=True)
        self.text_widget.tag_configure(
            "fold_marker",
            background="#E8F4FD",
            foreground="#0066CC",
            font=("Consolas", 8, "bold"),
        )

        # Bind click events on line numbers for fold markers (if line numbers exist)
        if self.line_numbers_widget:
            self.line_numbers_widget.bind("<Button-1>", self.on_line_number_click)

    def detect_foldable_blocks(self):
        """Detect blocks that can be folded"""
        content = self.text_widget.get("1.0", tk.END)
        lines = content.split("\n")
        foldable_blocks = []

        # Detect REPEAT blocks in Logo
        for i, line in enumerate(lines, 1):
            line_upper = line.strip().upper()

            # REPEAT blocks with brackets
            if line_upper.startswith("REPEAT") and "[" in line:
                bracket_count = 0
                start_line = i

                # Find matching closing bracket
                for j in range(i - 1, len(lines)):
                    line_content = lines[j]
                    bracket_count += line_content.count("[")
                    bracket_count -= line_content.count("]")

                    if bracket_count == 0 and j > i - 1:
                        end_line = j + 1
                        if end_line > start_line:
                            foldable_blocks.append((start_line, end_line))
                        break

            # BASIC FOR...NEXT loops
            elif line_upper.strip().startswith("FOR "):
                start_line = i
                # Find matching NEXT
                for j in range(i, len(lines)):
                    next_line = lines[j].strip().upper()
                    if next_line.startswith("NEXT"):
                        end_line = j + 1
                        if end_line > start_line:
                            foldable_blocks.append((start_line, end_line))
                        break

            # PILOT subroutines (sequences between labels)
            elif line_upper.startswith("L:") and line_upper != "L:END":
                start_line = i
                # Find next label or END
                for j in range(i, len(lines)):
                    next_line = lines[j].strip().upper()
                    if (next_line.startswith("L:") and j > i - 1) or next_line in [
                        "END",
                        "E:",
                    ]:
                        end_line = j
                        if end_line > start_line + 2:  # Only fold if more than 2 lines
                            foldable_blocks.append((start_line, end_line))
                        break

        return foldable_blocks

    def update_fold_markers(self):
        """Update fold markers in line numbers"""
        # Clear existing markers
        for marker in self.fold_markers.values():
            if marker:
                try:
                    marker.destroy()
                except Exception as e:
                    print(f"Error destroying fold marker: {e}")
        self.fold_markers = {}

        # Add new markers for foldable blocks (only if line numbers exist)
        if self.line_numbers_widget:
            foldable_blocks = self.detect_foldable_blocks()

            for start_line, end_line in foldable_blocks:
                if start_line not in self.folded_blocks:
                    # Add expand marker (▼)
                    self.add_fold_marker(start_line, "▼", False)
                else:
                    # Add collapse marker (▶)
                    self.add_fold_marker(start_line, "▶", True)

    def add_fold_marker(self, line_num, symbol, is_folded):
        """Add a fold marker to the line numbers widget"""
        try:
            # Create marker button
            marker = tk.Button(
                self.line_numbers_widget,
                text=symbol,
                font=("Consolas", 8, "bold"),
                bg="#F0F0F0",
                fg="#0066CC",
                relief=tk.FLAT,
                borderwidth=0,
                padx=2,
                pady=0,
                command=lambda: self.toggle_fold(line_num),
            )

            # Position marker at the line
            marker.place(x=0, y=(line_num - 1) * 15)
            # Adjust Y based on line height
            self.fold_markers[line_num] = marker

        except Exception as e:
            print(f"Error adding fold marker: {e}")

    def toggle_fold(self, start_line):
        """Toggle folding of a code block"""
        foldable_blocks = self.detect_foldable_blocks()

        # Find the block that starts at this line
        block_to_fold = None
        for start, end in foldable_blocks:
            if start == start_line:
                block_to_fold = (start, end)
                break

        if not block_to_fold:
            return

        start, end = block_to_fold

        if start_line in self.folded_blocks:
            # Unfold the block
            self.unfold_block(start_line)
        else:
            # Fold the block
            self.fold_block(start, end)

        # Update markers
        self.update_fold_markers()

    def fold_block(self, start_line, end_line):
        """Fold a code block"""
        # Hide lines from start+1 to end
        start_pos = f"{start_line + 1}.0"
        end_pos = f"{end_line}.0"

        self.text_widget.tag_add("folded", start_pos, end_pos)
        self.folded_blocks[start_line] = end_line

        # Add folded indicator to the start line
        fold_indicator = f" ... [{end_line - start_line - 1} lines folded]"

        # Insert fold indicator at end of line
        self.text_widget.insert(f"{start_line}.end", fold_indicator)
        self.text_widget.tag_add(
            "fold_marker",
            f"{start_line}.end-{len(fold_indicator)}c",
            f"{start_line}.end",
        )

    def unfold_block(self, start_line):
        """Unfold a code block"""
        if start_line not in self.folded_blocks:
            return

        end_line = self.folded_blocks[start_line]

        # Remove folded tag
        start_pos = f"{start_line + 1}.0"
        end_pos = f"{end_line}.0"
        self.text_widget.tag_remove("folded", start_pos, end_pos)

        # Remove fold indicator from start line
        current_content = self.text_widget.get(f"{start_line}.0", f"{start_line}.end")
        if " ... [" in current_content:
            indicator_start = current_content.find(" ... [")
            self.text_widget.delete(
                f"{start_line}.{indicator_start}", f"{start_line}.end"
            )

        del self.folded_blocks[start_line]

    def on_line_number_click(self, event):
        """Handle click on line numbers for folding"""
        if not self.line_numbers_widget:
            return

        # Get clicked line number
        y = event.y
        line_num = int(y / 15) + 1  # Approximate line height

        # Check if there's a fold marker at this line
        if line_num in self.fold_markers:
            self.toggle_fold(line_num)


# Integration with Time Warp IDE
class TimeWarpIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Warp IDE - Professional Edition")
        self.root.geometry("1000x700")
        # Apply a friendly theme and fonts
        self.setup_theme()

        # Initialize asyncio support
        init_async_support()

        # Initialize interpreter
        self.interpreter = TimeWarpInterpreter()

        # Initialize plugin system
        self.plugin_manager = PluginManager(self)

        self.create_widgets()
        self.create_menu()

        # Load plugins after UI is created
        self.load_plugins()

    def log_output(self, message):
        """Log a message to the output widget"""
        if hasattr(self, "output_text") and self.output_text:
            try:
                self.output_text.insert(tk.END, str(message) + "\n")
                self.output_text.see(tk.END)
            except tk.TclError:
                # Widget has been destroyed
                print(message)
        else:
            print(message)

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

        # Create a horizontal split: editor on the left,
        # output/variables/help on the right
        self.main_pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left pane: editor container
        self.editor_container = ttk.Frame(self.main_pane)
        self.main_pane.add(self.editor_container)

        # Right pane: notebook for Output, Variables, Help
        self.right_notebook = ttk.Notebook(self.main_pane)
        self.main_pane.add(self.right_notebook)

        # Try to create professional icons using Pillow;
        # fall back to emoji/text labels
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

        # Initialize code completion system
        self.code_completion = IntelligentCodeCompletion(self.editor, self)

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

        # Bind editor events to update status
        # (update_status may be defined elsewhere)
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

        # Real-time syntax checker
        self.syntax_checker = RealTimeSyntaxChecker(self.editor, self)

        # Bind editor events for syntax checking
        self.editor.bind("<KeyRelease>", self.syntax_checker.on_key_release)

        # Code folding system (without line numbers for now)
        self.code_folding = CodeFoldingSystem(self.editor, None, self)

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

        # Plugins menu
        plugins_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Plugins", menu=plugins_menu)
        plugins_menu.add_command(label="Reload Plugins", command=self.reload_plugins)
        plugins_menu.add_separator()
        plugins_menu.add_command(
            label="Plugin Manager", command=self.show_plugin_manager
        )

    # end create_menu

    def update_status(self):
        """Update the status bar (placeholder for future use)"""
        pass

    def run_program(self):
        """Run the program in the editor using asyncio for non-blocking execution"""
        try:
            code = self.editor.get(1.0, tk.END).strip()
            if code:
                self.interpreter.reset()
                self.output_text.delete(1.0, tk.END)

                # Split code into lines for async execution
                program_lines = [
                    line.strip() for line in code.split("\n") if line.strip()
                ]

                # Create async interpreter runner
                runner = get_async_runner()
                async_runner = AsyncInterpreterRunner(
                    self.interpreter.__class__, runner
                )

                # Run program asynchronously
                async def run_async():
                    try:
                        result = await async_runner.execute_program_async(
                            program_lines, self.interpreter.variables.copy()
                        )
                        # Update variables after execution
                        self.interpreter.variables.update(result.get("variables", {}))
                        self.update_variables_display()
                        self.status_bar.config(text="Program completed successfully")
                    except Exception as e:
                        self.log_output(f"Async execution error: {e}")
                        self.status_bar.config(text="Program execution failed")

                # Schedule the async task
                runner.run_async(run_async())
                self.status_bar.config(text="Program running...")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to run program: {e}")

    def stop_program(self):
        """Stop program execution"""
        self.interpreter.running = False
        self.status_bar.config(text="Program stopped")

    def debug_program(self):
        """Run program in debug mode"""
        # Placeholder for debug functionality
        messagebox.showinfo("Debug", "Debug mode not yet implemented")

    def step_once(self):
        """Execute one line (step)"""
        # Placeholder for step functionality
        messagebox.showinfo("Step", "Step execution not yet implemented")

    def continue_execution(self):
        """Continue execution until breakpoint"""
        # Placeholder for continue functionality
        messagebox.showinfo("Continue", "Continue execution not yet implemented")

    def load_demo(self):
        """Load the demo program"""
        demo_code = """T:Hello World!
T:Welcome to Time Warp IDE
A:name
T:*name*, nice to meet you!"""
        self.editor.delete(1.0, tk.END)
        self.editor.insert(1.0, demo_code)

    def save_file(self):
        """Save current file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".tw",
                filetypes=[("Time Warp files", "*.tw"), ("All files", "*.*")],
            )
            if filename:
                with open(filename, "w") as f:
                    f.write(self.editor.get(1.0, tk.END))
                self.status_bar.config(text=f"Saved: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

    def new_file(self):
        """Create a new file"""
        self.editor.delete(1.0, tk.END)
        self.status_bar.config(text="New file")

    def open_file(self):
        """Open a file"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("Time Warp files", "*.tw"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, "r") as f:
                    content = f.read()
                self.editor.delete(1.0, tk.END)
                self.editor.insert(1.0, content)
                self.status_bar.config(text=f"Opened: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

    def load_hello_world(self):
        """Load Hello World example"""
        code = """T:Hello World!
T:Welcome to Time Warp IDE"""
        self.editor.delete(1.0, tk.END)
        self.editor.insert(1.0, code)

    def load_math_demo(self):
        """Load Math Demo example"""
        code = """U:x=5
U:y=3
T:The sum of *x* and *y* is *x+y*
T:The product is *x*y*"""
        self.editor.delete(1.0, tk.END)
        self.editor.insert(1.0, code)

    def load_quiz_game(self):
        """Load Quiz Game example"""
        code = """T:Math Quiz Game
T:What is 2 + 2?
A:answer
Y:*answer*=4
T:Correct! Well done.
N:*answer*=4
T:Sorry, the answer is 4.
END"""
        self.editor.delete(1.0, tk.END)
        self.editor.insert(1.0, code)

    def toggle_dark_mode(self):
        """Toggle dark mode"""
        # Placeholder for dark mode toggle
        messagebox.showinfo("Dark Mode", "Dark mode toggle not yet implemented")

    def load_plugins(self):
        """Load all plugins on startup"""
        try:
            loaded_count = self.plugin_manager.load_all_plugins()
            self.log_output(f"Plugin system initialized: {loaded_count} plugins loaded")
            if loaded_count > 0:
                self.status_bar.config(text=f"Loaded {loaded_count} plugins")
        except Exception as e:
            self.log_output(f"Error loading plugins: {e}")
            messagebox.showerror("Plugin Error", f"Failed to load plugins: {e}")

    def reload_plugins(self):
        """Reload all plugins"""
        try:
            # Unload existing plugins
            unloaded_count = self.plugin_manager.unload_all_plugins()
            self.log_output(f"Unloaded {unloaded_count} plugins")

            # Reload plugins
            loaded_count = self.plugin_manager.load_all_plugins()
            self.status_bar.config(text=f"Reloaded {loaded_count} plugins")
            self.log_output(f"Plugin system reloaded: {loaded_count} plugins loaded")

            messagebox.showinfo(
                "Plugins Reloaded", f"Successfully reloaded {loaded_count} plugins"
            )
        except Exception as e:
            self.log_output(f"Error reloading plugins: {e}")
            messagebox.showerror("Plugin Error", f"Failed to reload plugins: {e}")

    def show_plugin_manager(self):
        """Show the plugin manager dialog"""
        try:
            # Create plugin manager dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Plugin Manager")
            dialog.geometry("600x400")
            dialog.transient(self.root)
            dialog.grab_set()

            # Create main frame
            main_frame = ttk.Frame(dialog, padding="10")
            main_frame.pack(fill=tk.BOTH, expand=True)

            # Title
            title_label = ttk.Label(
                main_frame, text="Installed Plugins", font=("Segoe UI", 14, "bold")
            )
            title_label.pack(pady=(0, 10))

            # Plugin list frame
            list_frame = ttk.Frame(main_frame)
            list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

            # Create treeview for plugins
            columns = ("Type", "Version", "Status")
            tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)

            # Configure columns
            tree.heading("#0", text="Plugin Name")
            tree.heading("Type", text="Type")
            tree.heading("Version", text="Version")
            tree.heading("Status", text="Status")

            tree.column("#0", width=200)
            tree.column("Type", width=100)
            tree.column("Version", width=80)
            tree.column("Status", width=80)

            # Add scrollbar
            scrollbar = ttk.Scrollbar(
                list_frame, orient=tk.VERTICAL, command=tree.yview
            )
            tree.configure(yscrollcommand=scrollbar.set)

            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Populate plugin list
            for plugin_name in self.plugin_manager.list_plugins():
                plugin = self.plugin_manager.get_plugin(plugin_name)
                if plugin:
                    tree.insert(
                        "",
                        tk.END,
                        text=plugin.metadata.name,
                        values=(
                            plugin.metadata.plugin_type.title(),
                            plugin.metadata.version,
                            "Loaded",
                        ),
                    )

            # Button frame
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.X, pady=(10, 0))

            ttk.Button(
                button_frame, text="Reload All", command=self.reload_plugins
            ).pack(side=tk.LEFT, padx=(0, 5))
            ttk.Button(button_frame, text="Close", command=dialog.destroy).pack(
                side=tk.RIGHT
            )

        except Exception as e:
            messagebox.showerror(
                "Plugin Manager Error", f"Failed to open plugin manager: {e}"
            )

    def update_variables_display(self):
        """Update the variables tree display"""
        # Clear existing items
        for item in self.variables_tree.get_children():
            self.variables_tree.delete(item)

        # Add current variables
        for var_name, var_value in self.interpreter.variables.items():
            self.variables_tree.insert(
                "", tk.END, text=var_name, values=(str(var_value),)
            )

    def get_help_text(self):
        return """
TIME WARP LANGUAGE REFERENCE

=== PILOT COMMANDS ===
T:text          - Output text (variables in *VAR* format). If a T: immediately
                  follows Y: or N: the T: is conditional and only prints when\n"
                  "the
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
SETXY x y - Move turtle to coordinates (x,y) without drawing"""


def create_demo_program():
    """Create a demo program for testing purposes"""
    return """L:START
T:Time Warp Demo Program
U:A=10
U:B=20
U:SUM=*A*+*B*
T:Welcome to Time Warp!
T:A = *A*, B = *B*
T:Sum = *SUM*
END"""


def main():
    root = tk.Tk()
    TimeWarpIDE(root)

    # Show welcome message
    root.after(
        1000,
        lambda: messagebox.showinfo(
            "Welcome to Time Warp IDE",
            "Welcome to Time Warp IDE - Educational Programming\n"
            "Environment!\n\n"
            "Features:\n"
            "• Multi-language support (PILOT, BASIC, Logo)\n"
            "• Turtle graphics\n"
            "• Interactive debugging\n"
            "• Hardware integration\n"
            "• Game development\n\n"
            "Select a language from the menu to begin!",
        ),
    )

    root.mainloop()


if __name__ == "__main__":
    main()
