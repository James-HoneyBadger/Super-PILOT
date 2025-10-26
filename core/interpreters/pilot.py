"""
PILOT Language Executor

Handles execution of PILOT (Programmed Inquiry, Learning Or Teaching) commands.
"""

import re
from core.engine import LanguageExecutor


class PilotExecutor(LanguageExecutor):
    """Executor for PILOT language commands"""

    def __init__(self, interpreter):
        super().__init__(interpreter)
        self.pilot_commands = {
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
            "END",
            "E:",
        }

    def can_execute(self, command: str) -> bool:
        """Check if this executor can handle the PILOT command"""
        if not command:
            return False

        command = command.strip()
        if len(command) > 1 and command[1] == ":":
            return command[:2] in self.pilot_commands
        return command.upper() in ["END"]

    def execute_command(self, command: str) -> str:
        """Execute a PILOT command"""
        if not command:
            return "continue"

        try:
            # Determine the command prefix
            colon_idx = command.find(":")
            if colon_idx != -1:
                cmd_type = command[: colon_idx + 1]
            else:
                cmd_type = command[:2] if len(command) > 1 else command

            if cmd_type == "T:":
                return self._execute_text(command)
            elif cmd_type == "A:":
                return self._execute_accept(command)
            elif cmd_type == "Y:":
                return self._execute_yes(command)
            elif cmd_type == "N:":
                return self._execute_no(command)
            elif cmd_type == "J:":
                return self._execute_jump(command)
            elif cmd_type == "M:":
                return self._execute_match(command)
            elif cmd_type == "R:":
                return self._execute_runtime(command)
            elif cmd_type == "C:":
                return self._execute_compute(command)
            elif cmd_type == "L:":
                return "continue"  # Label - do nothing
            elif cmd_type == "U:":
                return self._execute_update(command)
            elif command.strip().upper() == "END":
                return "end"

        except Exception as e:
            error_msg = f"❌ Error in PILOT command '{command}': {str(e)}"
            self.interpreter.display_error(error_msg)
            return "continue"

        return "continue"

    def _execute_text(self, command: str) -> str:
        """Execute T: (Text output) command"""
        text = command[2:].strip()

        # Check if this is conditional text (following Y: or N:)
        if self.interpreter.execution_context._last_match_set:
            self.interpreter.execution_context._last_match_set = False
            if not self.interpreter.execution_context.match_flag:
                return "continue"

        text = self._interpolate_text(text)
        self.interpreter.log_output(text)
        return "continue"

    def _execute_accept(self, command: str) -> str:
        """Execute A: (Accept input) command"""
        var_name = command[2:].strip()
        prompt = f"Enter value for {var_name}: "
        value = self.interpreter.get_user_input(prompt).strip()

        # Try to convert to number, otherwise keep as string
        try:
            if "." not in value and "e" not in value.lower():
                val = int(value)
            else:
                val = float(value)
            self.interpreter.variable_manager.set_variable(var_name, val)
        except ValueError:
            self.interpreter.variable_manager.set_variable(var_name, value)

        return "continue"

    def _execute_yes(self, command: str) -> str:
        """Execute Y: (Yes condition) command"""
        condition = command[2:].strip()
        try:
            result = self.interpreter.variable_manager.evaluate_expression(condition)
            self.interpreter.execution_context.match_flag = bool(result)
        except Exception as e:
            self.interpreter.execution_context.match_flag = False
            self.interpreter.log_output(f"Error in Y: condition '{condition}': {e}")

        self.interpreter.execution_context._last_match_set = True
        return "continue"

    def _execute_no(self, command: str) -> str:
        """Execute N: (No condition) command"""
        condition = command[2:].strip()
        try:
            result = self.interpreter.variable_manager.evaluate_expression(condition)
            self.interpreter.execution_context.match_flag = bool(result)
        except Exception as e:
            self.interpreter.execution_context.match_flag = False
            self.interpreter.log_output(f"Error in N: condition '{condition}': {e}")

        self.interpreter.execution_context._last_match_set = True
        return "continue"

    def _execute_jump(self, command: str) -> str:
        """Execute J: (Jump) command"""
        label = command[2:].strip()

        # Check if conditional jump
        if self.interpreter.execution_context._last_match_set:
            self.interpreter.execution_context._last_match_set = False
            if not self.interpreter.execution_context.match_flag:
                return "continue"

        if label in self.interpreter.program_manager.labels:
            return f"jump:{self.interpreter.program_manager.labels[label]}"
        return "continue"

    def _execute_match(self, command: str) -> str:
        """Execute M: (Match) command"""
        label = command[2:].strip()
        if (
            self.interpreter.execution_context.match_flag
            and label in self.interpreter.program_manager.labels
        ):
            return f"jump:{self.interpreter.program_manager.labels[label]}"
        return "continue"

    def _execute_runtime(self, command: str) -> str:
        """Execute R: (Runtime/Resource) command"""
        arg_upper = command[2:].strip().upper() if command else ""

        # Handle various R: subcommands
        if arg_upper.startswith("SND "):
            return self._handle_sound_command(command[2:])
        elif arg_upper.startswith("PLAY "):
            return self._handle_play_command(command[2:])
        elif arg_upper.startswith("SAVE "):
            return self._handle_save_command(command[2:])
        elif arg_upper.startswith("LOAD "):
            return self._handle_load_command(command[2:])
        else:
            # Default: treat as gosub
            label = command[2:].strip()
            self.interpreter.program_manager.push_return_address(
                self.interpreter.program_manager.current_line + 1
            )
            if label in self.interpreter.program_manager.labels:
                return f"jump:{self.interpreter.program_manager.labels[label]}"
            return "continue"

    def _execute_compute(self, command: str) -> str:
        """Execute C: (Compute/Call) command"""
        # Return from subroutine
        return_addr = self.interpreter.program_manager.pop_return_address()
        if return_addr is not None:
            return f"jump:{return_addr}"
        return "continue"

    def _execute_update(self, command: str) -> str:
        """Execute U: (Update variable) command"""
        assignment = command[2:].strip()
        if "=" in assignment:
            var_name, expr = assignment.split("=", 1)
            var_name = var_name.strip()
            expr = expr.strip()

            # Check for quoted strings first
            if (expr.startswith('"') and expr.endswith('"')) or (
                expr.startswith("'") and expr.endswith("'")
            ):
                value = expr[1:-1]
                self.interpreter.variable_manager.set_variable(var_name, value)
            else:
                try:
                    value = self.interpreter.variable_manager.evaluate_expression(expr)
                    self.interpreter.variable_manager.set_variable(var_name, value)
                except Exception as e:
                    if "forbidden" in str(e).lower() or "dangerous" in str(e).lower():
                        self.interpreter.log_output(f"Assignment rejected: {e}")
                        return "error"
                    else:
                        value = expr
                        self.interpreter.variable_manager.set_variable(var_name, value)
        return "continue"

    def _handle_sound_command(self, args: str) -> str:
        """Handle R: SND command"""
        m = re.search(
            r'name\s*=\s*"([^"]+)"\s*,\s*file\s*=\s*"([^"]+)"', args, re.IGNORECASE
        )
        if m:
            name, path = m.groups()
            self.interpreter.audio_mixer.register_sound(name, path)
            self.interpreter.log_output(f"Sound '{name}' registered")
        else:
            self.interpreter.log_output(
                'Invalid SND syntax: R: SND name="soundname", file="path.wav"'
            )
        return "continue"

    def _handle_play_command(self, args: str) -> str:
        """Handle R: PLAY command"""
        m = re.search(r"\"([^\"]+)\"", args)
        if m:
            name = m.group(1)
            self.interpreter.audio_mixer.play_sound(name)
            self.interpreter.log_output(f"Playing sound '{name}'")
        else:
            self.interpreter.log_output('Invalid PLAY syntax: R: PLAY "soundname"')
        return "continue"

    def _handle_save_command(self, args: str) -> str:
        """Handle R: SAVE command"""
        m = re.search(r"\"([^\"]+)\"", args)
        if m:
            slot = m.group(1)
            # Save current state
            import os

            save_dir = os.path.expanduser("~/.time_warp_saves")
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, f"{slot}.json")
            import json

            state = {
                "variables": self.interpreter.variable_manager.variables,
                "turtle_x": self.interpreter.graphics_system.turtle_x,
                "turtle_y": self.interpreter.graphics_system.turtle_y,
                "turtle_heading": self.interpreter.graphics_system.turtle_heading,
                "pen_down": self.interpreter.graphics_system.pen_down,
                "pen_color": self.interpreter.graphics_system.pen_color,
                "pen_width": self.interpreter.graphics_system.pen_width,
            }
            with open(save_path, "w") as f:
                json.dump(state, f)
            self.interpreter.log_output(f"Game saved to slot '{slot}'")
        else:
            self.interpreter.log_output('Invalid SAVE syntax: R: SAVE "slotname"')
        return "continue"

    def _handle_load_command(self, args: str) -> str:
        """Handle R: LOAD command"""
        m = re.search(r"\"([^\"]+)\"", args)
        if m:
            slot = m.group(1)
            import os

            save_path = os.path.expanduser(f"~/.time_warp_saves/{slot}.json")
            if os.path.exists(save_path):
                import json

                with open(save_path, "r") as f:
                    state = json.load(f)
                self.interpreter.variable_manager.variables.update(
                    state.get("variables", {})
                )
                self.interpreter.graphics_system.turtle_x = state.get("turtle_x", 200)
                self.interpreter.graphics_system.turtle_y = state.get("turtle_y", 200)
                self.interpreter.graphics_system.turtle_heading = state.get(
                    "turtle_heading", 90
                )
                self.interpreter.graphics_system.pen_down = state.get("pen_down", True)
                self.interpreter.graphics_system.pen_color = state.get(
                    "pen_color", "black"
                )
                self.interpreter.graphics_system.pen_width = state.get("pen_width", 1)
                self.interpreter.log_output(f"Game loaded from slot '{slot}'")
            else:
                self.interpreter.log_output(f"Save slot '{slot}' not found")
        else:
            self.interpreter.log_output('Invalid LOAD syntax: R: LOAD "slotname"')
        return "continue"

    def _interpolate_text(self, text: str) -> str:
        """Interpolate *VAR* tokens in text"""
        # Replace explicit variable occurrences like *VAR*
        for var_name in self.interpreter.variable_manager.variables:
            var_value = self.interpreter.variable_manager.get_variable(var_name)
            text = text.replace(f"*{var_name}*", str(var_value))

        # Evaluate expression-like tokens
        try:
            tokens = re.findall(r"\*(.+?)\*", text)
            for tok in tokens:
                if tok in self.interpreter.variable_manager.variables:
                    continue
                tok_stripped = tok.strip()
                if re.fullmatch(r"[-+]?\d+(?:\.\d+)?", tok_stripped):
                    text = text.replace(f"*{tok}*", tok_stripped)
                    continue
                if re.search(r"[\(\)\+\-\*/%<>=]", tok):
                    try:
                        val = self.interpreter.variable_manager.evaluate_expression(tok)
                        text = text.replace(f"*{tok}*", str(val))
                    except Exception:
                        pass
        except Exception:
            pass

        return text
