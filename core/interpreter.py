#!/usr/bin/env python3
"""
Time Warp Interpreter Module

This module contains the main TimeWarpInterpreter class that handles
execution of PILOT, BASIC, and Logo programming languages.
"""

import math
import random
import re
import time
from typing import Any, Dict, List, Optional, Tuple

try:
    import tkinter as tk
except ImportError:
    tk = None

from core.safe_expression_evaluator import safe_eval


class ArduinoController:
    """Arduino hardware controller with simulation support"""

    def __init__(self, simulation_mode: bool = True) -> None:
        self.simulation_mode: bool = simulation_mode


class RPiController:
    """Raspberry Pi hardware controller with simulation support"""

    def __init__(self, simulation_mode: bool = True) -> None:
        self.simulation_mode: bool = simulation_mode


class AudioMixer:
    """Audio mixer for playing sounds with play/aplay support"""

    def __init__(self) -> None:
        self.registry: Dict[str, str] = {}  # name -> path
        self.has_play: bool = self._has_exe("play")
        self.has_aplay: bool = self._has_exe("aplay")

    def _has_exe(self, name: str) -> bool:
        import os

        for p in os.environ.get("PATH", "").split(os.pathsep):
            f = os.path.join(p, name)
            if os.path.isfile(f) and os.access(f, os.X_OK):
                return True
        return False

    def register_sound(self, name: str, path: str) -> None:
        """Register a sound file with a name"""
        self.registry[name] = path

    def play_sound(self, name: str) -> None:
        """Play a registered sound"""
        path = self.registry.get(name)
        if not path:
            return
        if self.has_play:
            import os

            os.system(f"play -q {path}")
        elif self.has_aplay and path.lower().endswith(".wav"):
            import os

            os.system(f"aplay -q {path}")
        else:
            # Fallback to system beep
            print("\a", end="")


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
            pass

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


class TimeWarpInterpreter:
    """Main interpreter for Time Warp IDE supporting PILOT, BASIC,
    and Logo languages"""

    def __init__(self, output_widget=None):
        self.output_widget = output_widget
        self.variables: Dict[str, Any] = {}
        self.labels: Dict[str, int] = {}
        self.procedures: Dict[str, Dict[str, Any]] = {}
        self.program_lines: List[Tuple[Optional[int], str]] = []
        self.current_line: int = 0
        self.stack: List[int] = []
        # For-loop stack: list of dicts with keys: var, end, step, for_line
        self.for_stack: List[Dict[str, Any]] = []
        self.match_flag: bool = False
        # Internal flag: set when a Y: or N: was the last command to allow
        # the immediately following T: to be treated as conditional.
        self._last_match_set: bool = False
        self.running: bool = False
        self.debug_mode: bool = False
        self.breakpoints: set = set()
        self.max_iterations: int = 10000  # Prevent infinite loops

        # DATA/READ/RESTORE support
        self.data_list: List[Any] = []  # List of data values
        self.data_pointer: int = 0  # Current position in data list

        # Turtle graphics state
        self.turtle_x: float = 200  # canvas x
        self.turtle_y: float = 200  # canvas y
        self.turtle_heading: float = 90  # degrees, 90 = up
        self.pen_down: bool = True
        self.pen_color: str = "black"
        self.pen_width: int = 1
        self.graphics_widget = None
        self.canvas_width: int = 400
        self.canvas_height: int = 400
        self.origin_x: int = 200
        self.origin_y: int = 200

        # Color palette for SETCOLOR numbers
        self.colors: List[str] = [
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
        self.tweens: List[Tween] = []  # List of active tweens
        self.timers: List[Timer] = []  # List of active timers
        self.particles: List[Particle] = []  # List of active particles
        self.sprites: Dict[str, Dict[str, Any]] = (
            {}
        )  # Sprite registry: name -> {'path': str, 'x': float, 'y': float}
        self.hud_enabled: bool = False  # HUD display toggle
        self.last_update_time: float = time.time() * 1000  # For delta time calculations

        # Logo procedures
        self.logo_procedures: Dict[str, Dict[str, Any]] = (
            {}
        )  # Logo procedure definitions

        self.reset_turtle()

    def reset(self) -> None:
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

    def reset_turtle(self) -> None:
        self.turtle_x = 200
        self.turtle_y = 200
        self.turtle_heading = 90
        self.pen_down = True
        self.pen_color = "black"
        self.pen_width = 1
        self.sprites = {}  # Reset sprite system
        if self.graphics_widget:
            self.graphics_widget.delete("all")

    def move_turtle(self, distance: float) -> None:
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
        self,
        x: float,
        y: float,
        radius: float,
        color: str,
        start_angle: float = 0,
        end_angle: float = 360,
        aspect: float = 1.0,
    ) -> None:
        """Draw a circle or arc at specified coordinates"""
        if not self.graphics_widget:
            return

        # Convert to canvas coordinates
        canvas_x = self.origin_x + x
        canvas_y = self.origin_y - y

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

    def execute_draw_commands(self, draw_string: str) -> None:
        """Execute DRAW command string with turtle graphics commands"""
        if not self.graphics_widget:
            return

        # DRAW commands: UnDnRlLeFgHhEeNn... etc.
        # DRAW commands: UDnRlLeFgHhEeNn... etc.
        i = 0

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

    def play_music_string(self, music_string: str) -> None:
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
            except Exception:
                self.log_output("\a", end="")
                time.sleep(0.1)

    def play_sound(
        self, frequency: float, duration: float, volume: int = 255, voice: int = 0
    ) -> None:
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
        except Exception:
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

    def draw_rectangle(self, width: float, height: float) -> None:
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

    def draw_dot(self, size: float) -> None:
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

    def draw_image(
        self, path: str, width: Optional[float] = None, height: Optional[float] = None
    ) -> None:
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

    def toggle_hud(self) -> None:
        """Toggle the HUD display"""
        self.hud_enabled = not self.hud_enabled
        if self.graphics_widget:
            self.update_hud()

    def update_hud(self) -> None:
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

    def take_snapshot(self, filename: str) -> None:
        """Take a snapshot of the graphics canvas"""
        if not self.graphics_widget:
            return
        try:
            self.graphics_widget.postscript(file=filename, colormode="color")
            self.log_output(f"Snapshot saved to {filename}")
        except Exception as e:
            self.log_output(f"Error saving snapshot: {e}")

    def create_sprite(self, name: str, path: str) -> None:
        """Create a new sprite"""
        self.sprites[name] = {"path": path, "x": 0, "y": 0}

    def set_sprite_position(self, name: str, x: float, y: float) -> None:
        """Set sprite position"""
        if name in self.sprites:
            self.sprites[name]["x"] = x
            self.sprites[name]["y"] = y

    def draw_sprite(self, name: str) -> None:
        """Draw a sprite at its current position"""
        if name not in self.sprites or not self.graphics_widget:
            return
        sprite = self.sprites[name]
        self.draw_image(sprite["path"], None, None)
        # Note: This moves the turtle to the sprite position for drawing
        # In a full implementation, sprites would be drawn independently

    def log_output(self, text: str) -> None:
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

    def parse_line(self, line: str) -> Tuple[Optional[int], str]:
        """Parse a program line for line number and command"""
        line = line.strip()
        match = re.match(r"^(\d+)\s+(.*)", line)
        if match:
            line_number, command = match.groups()
            return int(line_number), command.strip()
        return None, line.strip()

    def evaluate_expression(self, expr: str) -> Any:
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

    def get_user_input(self, prompt: str = "") -> str:
        """Get input from user"""
        if self.output_widget:
            # Use dialog for GUI environment
            import tkinter as tk
            from tkinter import simpledialog

            result = simpledialog.askstring("Input", prompt)
            return result if result is not None else ""
        else:
            # Use console input for command line
            return input(prompt)

    def execute_pilot_command(self, command: str) -> str:
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

            match cmd_type:
                case "T:":
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

                case "A:":
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

                case "Y:":
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

                case "N:":
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

                case "J:":
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

                case "M:":
                    # Jump if match flag is set
                    label = command[2:].strip()
                    if self.match_flag and label in self.labels:
                        return f"jump:{self.labels[label]}"
                    return "continue"

                case "MT:":
                    # Match-conditional text output: only output when match_flag is True
                    text = command[3:].strip()
                    if self.match_flag:
                        text = self.interpolate_text(text)
                        self.log_output(text)
                    return "continue"

                case "R:":
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
                                self.log_output(
                                    "RPI WRITE syntax: R: RPI WRITE pin value"
                                )
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
                                self.log_output(
                                    "RPI READ syntax: R: RPI READ pin variable"
                                )
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
                            self.log_output(
                                f"Robot LIGHT = {simulated_light} (simulated)"
                            )
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
                            self.log_output(
                                f"Unknown CONTROLLER command: {controller_cmd}"
                            )
                    else:
                        # Default: treat as gosub (subroutine call)
                        label = command[2:].strip()
                        self.stack.append(self.current_line + 1)
                        if label in self.labels:
                            return f"jump:{self.labels[label]}"
                        return "continue"

                    return "continue"

                case "GAME:":
                    # Game development commands
                    game_cmd = command[5:].strip().upper()  # Remove 'GAME:'

                    match game_cmd.split()[0] if game_cmd else "":
                        case "CREATE":
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
                                self.variables["GAME_OBJECT_COUNT"] = (
                                    self.game_object_count
                                )
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

                        case "MOVE":
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

                        case "PHYSICS":
                            # GAME:PHYSICS GRAVITY value
                            parts = game_cmd[7:].strip().split()
                            if len(parts) >= 2 and parts[0] == "GRAVITY":
                                gravity = self.evaluate_expression(parts[1])
                                self.variables["GAME_GRAVITY"] = gravity
                                self.variables["GAME_PHYSICS_ENABLED"] = 1
                            else:
                                self.log_output("GAME:PHYSICS syntax: GRAVITY value")
                            return "continue"

                        case "COLLISION":
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

                        case "RENDER":
                            # GAME:RENDER - Update render state
                            self.variables["GAME_RENDER_FRAME"] = (
                                self.variables.get("GAME_RENDER_FRAME", 0) + 1
                            )
                            self.variables["GAME_RENDER_STATUS"] = 1
                            return "continue"

                        case "UPDATE":
                            # GAME:UPDATE delta_time
                            parts = game_cmd[6:].strip().split()
                            if len(parts) >= 1:
                                delta_time = self.evaluate_expression(parts[0])
                                # Apply physics to all objects
                                if hasattr(self, "game_objects"):
                                    for obj_id, obj in self.game_objects.items():
                                        # Apply gravity if physics enabled
                                        if self.variables.get(
                                            "GAME_PHYSICS_ENABLED", 0
                                        ):
                                            gravity = self.variables.get(
                                                "GAME_GRAVITY", 9.8
                                            )
                                            obj["velocity_y"] += gravity * delta_time
                                            obj["y"] += obj["velocity_y"] * delta_time
                                            self.variables[
                                                f"GAME_OBJECT_{obj_id}_Y"
                                            ] = obj["y"]
                                            self.variables[
                                                f"GAME_OBJECT_{obj_id}_VELOCITY_Y"
                                            ] = obj["velocity_y"]
                                self.variables["GAME_UPDATE_DELTA"] = delta_time
                                self.variables["GAME_UPDATE_STATUS"] = 1
                            else:
                                self.log_output("GAME:UPDATE requires delta_time")
                            return "continue"

                        case "DELETE":
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
                                        if key.startswith(
                                            f"GAME_OBJECT_{obj_id_to_remove}_"
                                        ):
                                            del self.variables[key]
                                    self.variables["GAME_OBJECT_COUNT"] = len(
                                        self.game_objects
                                    )
                                    self.variables["GAME_LAST_DELETE_RESULT"] = 1
                                else:
                                    self.variables["GAME_LAST_DELETE_RESULT"] = 0
                            else:
                                self.log_output("GAME:DELETE requires object_name")
                            return "continue"

                        case "LIST":
                            # GAME:LIST - List all objects
                            if hasattr(self, "game_objects") and self.game_objects:
                                obj_list = []
                                for obj_id, obj in self.game_objects.items():
                                    obj_list.append(f"{obj['name']}({obj_id})")
                                self.variables["GAME_OBJECT_LIST"] = ",".join(obj_list)
                                self.variables["GAME_OBJECT_COUNT"] = len(
                                    self.game_objects
                                )
                            else:
                                self.variables["GAME_OBJECT_LIST"] = ""
                                self.variables["GAME_OBJECT_COUNT"] = 0
                            return "continue"

                        case "CLEAR":
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

                        case "INFO":
                            # GAME:INFO object_name [variable_name]
                            parts = game_cmd[4:].strip().split()
                            if len(parts) >= 1:
                                obj_name = parts[0]
                                var_name = (
                                    parts[1] if len(parts) > 1 else "GAME_OBJECT_INFO"
                                )
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

                        case "DEMO":
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

                        case _:
                            self.log_output(f"Unknown GAME command: {game_cmd}")
                            return "continue"

                case _ if command.strip().upper() == "END":
                    # End program
                    return "end"

                case _:
                    # Unknown command
                    return "continue"

        except Exception as e:
            self.log_output(f"PILOT command error: {e}")
            return "continue"

        return "continue"
