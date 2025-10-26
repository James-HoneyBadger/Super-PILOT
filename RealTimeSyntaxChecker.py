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


