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

        # Bind click events on line numbers for fold markers
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
            try:
                marker.destroy()
            except:
                pass
        self.fold_markers = {}

        # Add new markers for foldable blocks
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
            marker.place(x=0, y=(line_num - 1) * 15)  # Adjust Y based on line height
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
        line_content = self.text_widget.get(f"{start_line}.0", f"{start_line}.end")
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
        line_content = self.text_widget.get(f"{start_line}.0", f"{start_line}.end")
        if " ... [" in line_content:
            indicator_start = line_content.find(" ... [")
            self.text_widget.delete(
                f"{start_line}.{indicator_start}", f"{start_line}.end"
            )

        del self.folded_blocks[start_line]

    def on_line_number_click(self, event):
        """Handle click on line numbers for folding"""
        # Get clicked line number
        y = event.y
        line_num = int(y / 15) + 1  # Approximate line height

        # Check if there's a fold marker at this line
        if line_num in self.fold_markers:
            self.toggle_fold(line_num)


class ProjectExplorer:
    """File tree view for managing Time Warp projects and files"""

    def __init__(self, ide):
        self.ide = ide
        self.current_project_path = None
        self.tree_widget = None
        self.explorer_window = None
        self.file_watchers = {}

    def show_explorer(self):
        """Show the project explorer window"""
        if self.explorer_window and self.explorer_window.winfo_exists():
            self.explorer_window.lift()
            return

        # Create explorer window
        self.explorer_window = tk.Toplevel(self.ide.root)
        self.explorer_window.title("Project Explorer")
        self.explorer_window.geometry("300x500")

        # Create toolbar
        toolbar = tk.Frame(self.explorer_window, bg="#F0F0F0", height=30)
        toolbar.pack(fill=tk.X, padx=2, pady=2)
        toolbar.pack_propagate(False)

        # Toolbar buttons
        tk.Button(
            toolbar,
            text="📁",
            command=self.open_project_folder,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bg="#F0F0F0",
            fg="#333",
            padx=5,
        ).pack(side=tk.LEFT, padx=2)
        tk.Button(
            toolbar,
            text="📄",
            command=self.new_file,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bg="#F0F0F0",
            fg="#333",
            padx=5,
        ).pack(side=tk.LEFT, padx=2)
        tk.Button(
            toolbar,
            text="🔄",
            command=self.refresh_tree,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bg="#F0F0F0",
            fg="#333",
            padx=5,
        ).pack(side=tk.LEFT, padx=2)

        # Project path label
        self.path_label = tk.Label(
            self.explorer_window,
            text="No project opened",
            bg="#E8E8E8",
            fg="#666",
            font=("Segoe UI", 9),
            anchor=tk.W,
            padx=5,
        )
        self.path_label.pack(fill=tk.X, padx=2, pady=(0, 2))

        # Create tree view
        tree_frame = tk.Frame(self.explorer_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Tree widget with scrollbars
        self.tree_widget = ttk.Treeview(tree_frame, show="tree headings")
        self.tree_widget.heading("#0", text="Time Warp Files", anchor=tk.W)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(
            tree_frame, orient=tk.VERTICAL, command=self.tree_widget.yview
        )
        h_scrollbar = ttk.Scrollbar(
            tree_frame, orient=tk.HORIZONTAL, command=self.tree_widget.xview
        )
        self.tree_widget.configure(
            yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set
        )

        # Pack tree and scrollbars
        self.tree_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Bind events
        self.tree_widget.bind("<Double-1>", self.on_item_double_click)
        self.tree_widget.bind("<Button-3>", self.show_context_menu)

        # Set default project path to current directory
        import os

        current_dir = os.getcwd()
        time_warp_projects = os.path.join(current_dir, "Time_Warp_Projects")

        if os.path.exists(time_warp_projects):
            self.load_project(time_warp_projects)
        else:
            self.load_project(current_dir)

    def open_project_folder(self):
        """Open a project folder"""
        from tkinter import filedialog

        folder_path = filedialog.askdirectory(title="Select Project Folder")
        if folder_path:
            self.load_project(folder_path)

    def load_project(self, project_path):
        """Load a project folder into the tree"""
        self.current_project_path = project_path
        self.path_label.config(text=f"Project: {os.path.basename(project_path)}")
        self.refresh_tree()

    def refresh_tree(self):
        """Refresh the file tree"""
        if not self.tree_widget or not self.current_project_path:
            return

        # Clear existing tree
        for item in self.tree_widget.get_children():
            self.tree_widget.delete(item)

        # Populate tree
        self.populate_tree(self.current_project_path, "")

    def populate_tree(self, path, parent_node):
        """Populate tree with files and folders"""
        import os

        try:
            items = []
            # Get directories and files
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    items.append((item, item_path, "folder"))
                elif item.endswith((".spt", ".pil", ".pilot", ".logo", ".bas")):
                    items.append((item, item_path, "file"))

            # Sort: folders first, then files
            items.sort(key=lambda x: (x[2] != "folder", x[0].lower()))

            for item_name, item_path, item_type in items:
                icon = "📁" if item_type == "folder" else self.get_file_icon(item_name)
                node_text = f"{icon} {item_name}"

                node = self.tree_widget.insert(
                    parent_node, tk.END, text=node_text, values=(item_path, item_type)
                )

                # If it's a folder, add a placeholder child to make it expandable
                if item_type == "folder":
                    self.tree_widget.insert(node, tk.END, text="Loading...")

            # Bind tree expansion event
            self.tree_widget.bind("<<TreeviewOpen>>", self.on_tree_expand)

        except PermissionError:
            pass  # Skip directories we can't read

    def get_file_icon(self, filename):
        """Get icon for file based on extension"""
        ext = filename.lower().split(".")[-1] if "." in filename else ""
        icons = {
            "spt": "🎯",  # Time Warp files
            "pil": "✈️",  # PILOT files
            "pilot": "✈️",  # PILOT files
            "logo": "🐢",  # Logo files
            "bas": "💻",  # BASIC files
            "basic": "💻",  # BASIC files
            "txt": "📄",  # Text files
            "md": "📝",  # Markdown files
        }
        return icons.get(ext, "📄")

    def on_tree_expand(self, event):
        """Handle tree expansion - lazy loading of subdirectories"""
        item = self.tree_widget.selection()[0] if self.tree_widget.selection() else None
        if not item:
            return

        # Check if this is a folder and has placeholder child
        values = self.tree_widget.item(item, "values")
        if len(values) >= 2 and values[1] == "folder":
            children = self.tree_widget.get_children(item)
            if (
                len(children) == 1
                and self.tree_widget.item(children[0], "text") == "Loading..."
            ):
                # Remove placeholder and load actual contents
                self.tree_widget.delete(children[0])
                self.populate_tree(values[0], item)

    def on_item_double_click(self, event):
        """Handle double-click on tree item"""
        item = self.tree_widget.selection()[0] if self.tree_widget.selection() else None
        if not item:
            return

        values = self.tree_widget.item(item, "values")
        if len(values) >= 2:
            file_path, item_type = values[0], values[1]

            if item_type == "file":
                self.open_file(file_path)

    def open_file(self, file_path):
        """Open a file in the main editor"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Load content into main editor
            self.ide.editor.delete("1.0", tk.END)
            self.ide.editor.insert("1.0", content)

            # Update IDE title and status
            filename = os.path.basename(file_path)
            self.ide.root.title(f"HB Code - {filename}")

            if hasattr(self.ide, "status_label"):
                self.ide.status_label.config(text=f"📂 Opened: {filename}")

            # Store current file path for saving
            self.ide.current_file_path = file_path

        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{str(e)}")

    def new_file(self):
        """Create a new Time Warp file"""
        if not self.current_project_path:
            messagebox.showwarning("Warning", "Please open a project folder first")
            return

        filename = simpledialog.askstring(
            "New File", "Enter filename (with .spt extension):"
        )
        if filename:
            if not filename.endswith(".spt"):
                filename += ".spt"

            file_path = os.path.join(self.current_project_path, filename)

            try:
                # Create empty file with basic template
                template_content = """T:Welcome to HB Code!
T:This is a new HB Code program.
T:Start coding here...
E:
"""
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(template_content)

                # Refresh tree to show new file
                self.refresh_tree()

                # Open the new file
                self.open_file(file_path)

            except Exception as e:
                messagebox.showerror("Error", f"Could not create file:\n{str(e)}")

    def show_context_menu(self, event):
        """Show context menu for tree items"""
        item = self.tree_widget.identify_row(event.y)
        if not item:
            return

        self.tree_widget.selection_set(item)
        values = self.tree_widget.item(item, "values")

        context_menu = tk.Menu(self.tree_widget, tearoff=0)

        if len(values) >= 2:
            file_path, item_type = values[0], values[1]

            if item_type == "file":
                context_menu.add_command(
                    label="Open", command=lambda: self.open_file(file_path)
                )
                context_menu.add_separator()
                context_menu.add_command(
                    label="Rename", command=lambda: self.rename_item(file_path)
                )
                context_menu.add_command(
                    label="Delete", command=lambda: self.delete_item(file_path)
                )
            elif item_type == "folder":
                context_menu.add_command(
                    label="New File", command=lambda: self.new_file_in_folder(file_path)
                )
                context_menu.add_separator()
                context_menu.add_command(
                    label="Rename", command=lambda: self.rename_item(file_path)
                )
                context_menu.add_command(
                    label="Delete", command=lambda: self.delete_item(file_path)
                )

        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def rename_item(self, item_path):
        """Rename a file or folder"""
        old_name = os.path.basename(item_path)
        new_name = simpledialog.askstring(
            "Rename", f"New name for '{old_name}':", initialvalue=old_name
        )
        if new_name and new_name != old_name:
            try:
                new_path = os.path.join(os.path.dirname(item_path), new_name)
                os.rename(item_path, new_path)
                self.refresh_tree()
            except Exception as e:
                messagebox.showerror("Error", f"Could not rename:\n{str(e)}")

    def delete_item(self, item_path):
        """Delete a file or folder"""
        item_name = os.path.basename(item_path)
        if messagebox.askyesno(
            "Delete", f"Are you sure you want to delete '{item_name}'?"
        ):
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    import shutil

                    shutil.rmtree(item_path)
                self.refresh_tree()
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete:\n{str(e)}")

    def new_file_in_folder(self, folder_path):
        """Create a new file in specific folder"""
        old_project_path = self.current_project_path
        self.current_project_path = folder_path
        self.new_file()
        self.current_project_path = old_project_path


class EducationalTutorials:
    def __init__(self, ide):
        self.ide = ide
        self.current_tutorial = None
        self.tutorial_step = 0

    def start_tutorial(self, tutorial_id):
        messagebox.showinfo("Tutorial", f"Starting tutorial: {tutorial_id}")


class ExerciseMode:
    def __init__(self, ide):
        self.ide = ide
        self.current_exercise = None

    def start_exercise(self, exercise_id):
        messagebox.showinfo("Exercise", f"Starting exercise: {exercise_id}")


class VersionControlSystem:
    def __init__(self, ide):
        self.ide = ide
        self.history = []
        self.current_version = -1

    def save_version(self, comment=""):
        content = self.ide.editor.get("1.0", tk.END)
        version = {
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "comment": comment,
        }
        self.history.append(version)
        self.current_version = len(self.history) - 1


class AdvancedDebugger:
    """Enhanced debugger with step-through execution, variable inspection, and call stack visualization"""

    def __init__(self, ide):
        self.ide = ide
        self.breakpoints = set()
        self.debugging = False
        self.current_line = 0
        self.step_mode = False
        self.call_stack = []
        self.variable_watches = set()
        self.debug_windows = {}
        # Defer setup_debug_tags until editor is available
        self.tags_setup = False

    def setup_debug_tags(self):
        """Setup text tags for debugging visualization"""
        if not hasattr(self.ide, "editor") or not self.ide.editor:
            return  # Editor not ready yet

        self.ide.editor.tag_configure(
            "breakpoint", background="#FFE6E6", foreground="#CC0000"
        )
        self.ide.editor.tag_configure(
            "current_line",
            background="#E6F3FF",
            foreground="#0066CC",
            relief="raised",
            borderwidth=1,
        )
        self.ide.editor.tag_configure(
            "call_stack_line", background="#F0F8E6", foreground="#336600"
        )
        self.tags_setup = True

    def toggle_breakpoint(self, line_number):
        """Toggle breakpoint at specified line"""
        if line_number in self.breakpoints:
            self.breakpoints.remove(line_number)
            self.ide.editor.tag_remove(
                "breakpoint", f"{line_number}.0", f"{line_number}.end"
            )
        else:
            self.breakpoints.add(line_number)
            self.ide.editor.tag_add(
                "breakpoint", f"{line_number}.0", f"{line_number}.end"
            )

        # Sync with interpreter
        self.sync_breakpoints_with_interpreter()

    def sync_breakpoints_with_interpreter(self):
        """Synchronize breakpoints with the interpreter"""
        try:
            if hasattr(self.ide, "interpreter") and self.ide.interpreter is not None:
                # Clear interpreter breakpoints
                self.ide.interpreter.breakpoints.clear()
                # Add all breakpoints (convert to zero-based)
                for line_num in self.breakpoints:
                    self.ide.interpreter.breakpoints.add(line_num - 1)
        except Exception as e:
            print(f"Error syncing breakpoints: {e}")

    def start_debug_session(self):
        """Start a debugging session"""
        self.debugging = True
        self.step_mode = True
        self.call_stack.clear()

        # Show debug windows
        self.show_variables_window()
        self.show_call_stack_window()

        # Update status
        if hasattr(self.ide, "status_label"):
            self.ide.status_label.config(
                text="🐛 Debug Mode - Ready to step through code"
            )

    def stop_debug_session(self):
        """Stop the debugging session"""
        self.debugging = False
        self.step_mode = False
        self.current_line = 0

        # Clear debug highlighting
        self.ide.editor.tag_remove("current_line", "1.0", tk.END)
        self.ide.editor.tag_remove("call_stack_line", "1.0", tk.END)

        # Close debug windows
        self.close_debug_windows()

        # Update status
        if hasattr(self.ide, "status_label"):
            self.ide.status_label.config(text="✨ Ready to Code!")

    def step_over(self):
        """Execute next line (step over)"""
        if not self.debugging:
            self.start_debug_session()

        # This would integrate with the interpreter to execute one line
        if hasattr(self.ide, "interpreter") and self.ide.interpreter:
            try:
                # Set step mode in interpreter
                self.ide.interpreter.debug_mode = True
                self.ide.interpreter.step_mode = True

                # Execute one step
                # This is a simplified implementation
                self.highlight_current_line(self.current_line + 1)
                self.current_line += 1

                # Update variable watches
                self.update_variable_watches()

            except Exception as e:
                print(f"Step over error: {e}")

    def step_into(self):
        """Step into function/subroutine calls"""
        if not self.debugging:
            self.start_debug_session()

        # Similar to step_over but follows into subroutines
        self.step_over()  # Simplified implementation

    def step_out(self):
        """Step out of current function/subroutine"""
        if not self.debugging:
            return

        # Execute until return from current call level
        if self.call_stack:
            target_level = len(self.call_stack) - 1
            # Continue execution until we're back at target level
            self.continue_execution()

    def continue_execution(self):
        """Continue execution until next breakpoint"""
        if not self.debugging:
            return

        self.step_mode = False
        # This would tell interpreter to run until breakpoint
        if hasattr(self.ide, "interpreter") and self.ide.interpreter:
            self.ide.interpreter.step_mode = False

    def highlight_current_line(self, line_number):
        """Highlight the currently executing line"""
        # Clear previous highlighting
        self.ide.editor.tag_remove("current_line", "1.0", tk.END)

        # Highlight current line
        if line_number > 0:
            self.ide.editor.tag_add(
                "current_line", f"{line_number}.0", f"{line_number}.end"
            )

            # Scroll to current line
            self.ide.editor.see(f"{line_number}.0")

        self.current_line = line_number

    def add_variable_watch(self, var_name):
        """Add a variable to the watch list"""
        self.variable_watches.add(var_name)
        self.update_variable_watches()

    def remove_variable_watch(self, var_name):
        """Remove a variable from the watch list"""
        self.variable_watches.discard(var_name)
        self.update_variable_watches()

    def update_variable_watches(self):
        """Update the variable watch window"""
        if "variables" in self.debug_windows:
            try:
                window = self.debug_windows["variables"]
                text_widget = window.children["!text"]

                text_widget.delete("1.0", tk.END)
                text_widget.insert("1.0", "=== Variable Watches ===\n\n")

                if hasattr(self.ide, "interpreter") and self.ide.interpreter:
                    for var_name in sorted(self.variable_watches):
                        value = self.ide.interpreter.variables.get(
                            var_name, "undefined"
                        )
                        text_widget.insert(tk.END, f"{var_name}: {value}\n")

                    text_widget.insert(tk.END, "\n=== All Variables ===\n\n")
                    for var_name, value in sorted(
                        self.ide.interpreter.variables.items()
                    ):
                        text_widget.insert(tk.END, f"{var_name}: {value}\n")

            except Exception as e:
                print(f"Error updating variable watches: {e}")

    def show_variables_window(self):
        """Show the variables inspection window"""
        if "variables" in self.debug_windows:
            return  # Already open

        window = tk.Toplevel(self.ide.root)
        window.title("Variables Inspector")
        window.geometry("300x400")

        # Create text widget with scrollbar
        frame = tk.Frame(window)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        text_widget = tk.Text(frame, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add watch controls
        controls_frame = tk.Frame(window)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(controls_frame, text="Watch Variable:").pack(side=tk.LEFT)
        watch_entry = tk.Entry(controls_frame)
        watch_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        def add_watch():
            var_name = watch_entry.get().strip()
            if var_name:
                self.add_variable_watch(var_name)
                watch_entry.delete(0, tk.END)

        tk.Button(controls_frame, text="Add Watch", command=add_watch).pack(
            side=tk.RIGHT
        )

        # Bind Enter key to add watch
        watch_entry.bind("<Return>", lambda e: add_watch())

        self.debug_windows["variables"] = window
        self.update_variable_watches()

        # Handle window closing
        window.protocol(
            "WM_DELETE_WINDOW", lambda: self.close_debug_window("variables")
        )

    def show_call_stack_window(self):
        """Show the call stack window"""
        if "call_stack" in self.debug_windows:
            return  # Already open

        window = tk.Toplevel(self.ide.root)
        window.title("Call Stack")
        window.geometry("400x300")

        # Create listbox for call stack
        frame = tk.Frame(window)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        listbox = tk.Listbox(frame, font=("Consolas", 10))
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)

        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.debug_windows["call_stack"] = window

        # Handle window closing
        window.protocol(
            "WM_DELETE_WINDOW", lambda: self.close_debug_window("call_stack")
        )

        # Update call stack display
        self.update_call_stack_display()

    def update_call_stack_display(self):
        """Update the call stack display"""
        if "call_stack" in self.debug_windows:
            try:
                window = self.debug_windows["call_stack"]
                listbox = window.children["!frame"].children["!listbox"]

                listbox.delete(0, tk.END)

                if self.call_stack:
                    for i, frame in enumerate(self.call_stack):
                        listbox.insert(tk.END, f"Frame {i}: {frame}")
                else:
                    listbox.insert(tk.END, "No active call stack")

            except Exception as e:
                print(f"Error updating call stack: {e}")

    def close_debug_window(self, window_name):
        """Close a specific debug window"""
        if window_name in self.debug_windows:
            try:
                self.debug_windows[window_name].destroy()
                del self.debug_windows[window_name]
            except:
                pass

    def close_debug_windows(self):
        """Close all debug windows"""
        for window_name in list(self.debug_windows.keys()):
            self.close_debug_window(window_name)


class MLManagerDialog:
    """Machine Learning model and dataset management dialog"""

    def __init__(self, ide):
        self.ide = ide
        self.window = None

    def show(self):
        """Show the ML management dialog"""
        if self.window:
            self.window.lift()
            return

        self.window = tk.Toplevel(self.ide.root)
        self.window.title("AI/ML Manager")
        self.window.geometry("600x500")
        self.window.transient(self.ide.root)

        # Create notebook for tabs
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Models tab
        models_frame = ttk.Frame(notebook)
        notebook.add(models_frame, text="Models")
        self.setup_models_tab(models_frame)

        # Datasets tab
        datasets_frame = ttk.Frame(notebook)
        notebook.add(datasets_frame, text="Datasets")
        self.setup_datasets_tab(datasets_frame)

        # Quick Demo tab
        demo_frame = ttk.Frame(notebook)
        notebook.add(demo_frame, text="Quick Demo")
        self.setup_demo_tab(demo_frame)

        # Handle window closing
        self.window.protocol("WM_DELETE_WINDOW", self.close)

    def setup_models_tab(self, parent):
        """Setup the models management tab"""
        # Model list
        list_frame = ttk.LabelFrame(parent, text="Loaded Models")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Treeview for models
        columns = ("Name", "Type", "Status", "Trained")
        self.models_tree = ttk.Treeview(
            list_frame, columns=columns, show="headings", height=8
        )

        for col in columns:
            self.models_tree.heading(col, text=col)
            self.models_tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.models_tree.yview
        )
        self.models_tree.configure(yscrollcommand=scrollbar.set)

        self.models_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Model controls
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(controls_frame, text="Load Model", command=self.load_model).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(controls_frame, text="Remove Model", command=self.remove_model).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(
            controls_frame, text="Model Info", command=self.show_model_info
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="Refresh", command=self.refresh_models).pack(
            side=tk.LEFT, padx=2
        )

    def setup_datasets_tab(self, parent):
        """Setup the datasets management tab"""
        # Dataset list
        list_frame = ttk.LabelFrame(parent, text="Available Datasets")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Treeview for datasets
        columns = ("Name", "Type", "Size", "Features")
        self.datasets_tree = ttk.Treeview(
            list_frame, columns=columns, show="headings", height=8
        )

        for col in columns:
            self.datasets_tree.heading(col, text=col)
            self.datasets_tree.column(col, width=120)

        scrollbar2 = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.datasets_tree.yview
        )
        self.datasets_tree.configure(yscrollcommand=scrollbar2.set)

        self.datasets_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)

        # Dataset controls
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(
            controls_frame, text="Create Sample Data", command=self.create_sample_data
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            controls_frame, text="Remove Dataset", command=self.remove_dataset
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="View Data", command=self.view_dataset).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(controls_frame, text="Refresh", command=self.refresh_datasets).pack(
            side=tk.LEFT, padx=2
        )

    def setup_demo_tab(self, parent):
        """Setup the quick demo tab"""
        # Demo selection
        demo_frame = ttk.LabelFrame(parent, text="Educational ML Demonstrations")
        demo_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Demo buttons
        ttk.Label(
            demo_frame, text="Choose a demonstration to run:", font=("Arial", 12)
        ).pack(pady=10)

        button_frame = ttk.Frame(demo_frame)
        button_frame.pack(expand=True)

        demos = [
            (
                "Linear Regression",
                "linear",
                "Learn how linear models predict continuous values",
            ),
            (
                "Classification",
                "classification",
                "Learn how to classify data into categories",
            ),
            (
                "Clustering",
                "clustering",
                "Learn how to find patterns and group similar data",
            ),
        ]

        for i, (title, demo_type, desc) in enumerate(demos):
            frame = ttk.Frame(button_frame)
            frame.pack(fill=tk.X, padx=10, pady=5)

            ttk.Button(
                frame,
                text=f"Run {title} Demo",
                command=lambda dt=demo_type: self.run_demo(dt),
            ).pack(side=tk.LEFT)
            ttk.Label(frame, text=desc, foreground="gray").pack(side=tk.LEFT, padx=10)

        # Info text
        info_text = tk.Text(demo_frame, height=8, wrap=tk.WORD)
        info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        info_text.insert(
            tk.END,
            """🤖 AI/ML Integration Help:

• Use ML: commands in PILOT language (ML:LOAD, ML:TRAIN, ML:PREDICT)
• Use MLLOAD, MLTRAIN, MLPREDICT in BASIC
• Use LOADMODEL, TRAINMODEL, PREDICT in Logo
• All demos create sample data automatically
• Check the output window to see ML results

Educational Features:
- Visual feedback for all operations
- Sample datasets for learning
- Step-by-step ML workflow
- Real-time predictions""",
        )
        info_text.config(state=tk.DISABLED)

    def load_model(self):
        """Load a new ML model"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Load Model")
        dialog.geometry("400x200")
        dialog.transient(self.window)

        ttk.Label(dialog, text="Model Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=5)

        ttk.Label(dialog, text="Model Type:").pack(pady=5)
        type_var = tk.StringVar(value="linear_regression")
        type_combo = ttk.Combobox(dialog, textvariable=type_var, width=30)
        type_combo["values"] = (
            "linear_regression",
            "logistic_regression",
            "decision_tree",
            "kmeans",
        )
        type_combo.pack(pady=5)

        def do_load():
            name = name_entry.get().strip()
            model_type = type_var.get()
            if name and model_type:
                if self.ide.interpreter.aiml.load_model(name, model_type):
                    self.refresh_models()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to load model")
            else:
                messagebox.showwarning(
                    "Warning", "Please enter model name and select type"
                )

        ttk.Button(dialog, text="Load", command=do_load).pack(pady=10)

    def remove_model(self):
        """Remove selected model"""
        selection = self.models_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a model to remove")
            return

        model_name = self.models_tree.item(selection[0])["values"][0]
        if messagebox.askyesno("Confirm", f"Remove model '{model_name}'?"):
            if model_name in self.ide.interpreter.aiml.models:
                del self.ide.interpreter.aiml.models[model_name]
                self.refresh_models()

    def show_model_info(self):
        """Show detailed model information"""
        selection = self.models_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a model")
            return

        model_name = self.models_tree.item(selection[0])["values"][0]
        info = self.ide.interpreter.aiml.get_model_info(model_name)

        if info:
            info_text = f"""Model Information:

Name: {model_name}
Type: {info['type']}
Trained: {'Yes' if info['trained'] else 'No'}

Training History:
{self.ide.interpreter.aiml.training_history.get(model_name, 'No training history')}
"""
            messagebox.showinfo("Model Info", info_text)

    def refresh_models(self):
        """Refresh the models list"""
        for item in self.models_tree.get_children():
            self.models_tree.delete(item)

        for name, info in self.ide.interpreter.aiml.models.items():
            status = "Ready" if info["trained"] else "Not Trained"
            trained = "Yes" if info["trained"] else "No"
            self.models_tree.insert(
                "", tk.END, values=(name, info["type"], status, trained)
            )

    def create_sample_data(self):
        """Create sample dataset"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Create Sample Data")
        dialog.geometry("400x200")
        dialog.transient(self.window)

        ttk.Label(dialog, text="Dataset Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=5)

        ttk.Label(dialog, text="Data Type:").pack(pady=5)
        type_var = tk.StringVar(value="linear")
        type_combo = ttk.Combobox(dialog, textvariable=type_var, width=30)
        type_combo["values"] = ("linear", "classification", "clustering")
        type_combo.pack(pady=5)

        def do_create():
            name = name_entry.get().strip()
            data_type = type_var.get()
            if name and data_type:
                if self.ide.interpreter.aiml.create_sample_data(name, data_type):
                    self.refresh_datasets()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to create dataset")
            else:
                messagebox.showwarning(
                    "Warning", "Please enter dataset name and select type"
                )

        ttk.Button(dialog, text="Create", command=do_create).pack(pady=10)

    def remove_dataset(self):
        """Remove selected dataset"""
        selection = self.datasets_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a dataset to remove")
            return

        dataset_name = self.datasets_tree.item(selection[0])["values"][0]
        if messagebox.askyesno("Confirm", f"Remove dataset '{dataset_name}'?"):
            if dataset_name in self.ide.interpreter.aiml.datasets:
                del self.ide.interpreter.aiml.datasets[dataset_name]
                self.refresh_datasets()

    def view_dataset(self):
        """View dataset information"""
        selection = self.datasets_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a dataset")
            return

        dataset_name = self.datasets_tree.item(selection[0])["values"][0]
        dataset = self.ide.interpreter.aiml.datasets.get(dataset_name)

        if dataset:
            info_text = f"""Dataset Information:
            
Name: {dataset_name}
Type: {dataset.get('type', 'Unknown')}
Features Shape: {dataset['X'].shape if 'X' in dataset else 'N/A'}
Targets Shape: {dataset['y'].shape if 'y' in dataset else 'N/A'}
Sample Features: {str(dataset['X'][:3]) if 'X' in dataset else 'N/A'}
"""
            messagebox.showinfo("Dataset Info", info_text)

    def refresh_datasets(self):
        """Refresh the datasets list"""
        for item in self.datasets_tree.get_children():
            self.datasets_tree.delete(item)

        for name, data in self.ide.interpreter.aiml.datasets.items():
            data_type = data.get("type", "Unknown")
            size = f"{data['X'].shape[0]}" if "X" in data else "Unknown"
            features = (
                f"{data['X'].shape[1]}"
                if "X" in data and len(data["X"].shape) > 1
                else "1"
            )
            self.datasets_tree.insert(
                "", tk.END, values=(name, data_type, size, features)
            )

    def run_demo(self, demo_type):
        """Run ML demonstration"""
        try:
            self.ide.interpreter._run_ml_demo(demo_type)
            self.refresh_models()
            self.refresh_datasets()
            messagebox.showinfo(
                "Demo Complete",
                f"{demo_type.title()} demonstration completed!\nCheck the output window for results.",
            )
        except Exception as e:
            messagebox.showerror("Demo Error", f"Error running demo: {e}")

    def close(self):
        """Close the ML manager window"""
        if self.window:
            self.window.destroy()
            self.window = None


class GameManagerDialog:
    """Game development and object management dialog"""

    def __init__(self, ide):
        self.ide = ide
        self.window = None

    def show(self):
        """Show the game management dialog"""
        if self.window:
            self.window.lift()
            return

        self.window = tk.Toplevel(self.ide.root)
        self.window.title("🎮 Game Development Manager")
        self.window.geometry("700x600")
        self.window.transient(self.ide.root)

        # Create notebook for tabs
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Game Objects tab
        objects_frame = ttk.Frame(notebook)
        notebook.add(objects_frame, text="🎯 Game Objects")
        self.setup_objects_tab(objects_frame)

        # Physics tab
        physics_frame = ttk.Frame(notebook)
        notebook.add(physics_frame, text="⚡ Physics")
        self.setup_physics_tab(physics_frame)

        # Scene Preview tab
        preview_frame = ttk.Frame(notebook)
        notebook.add(preview_frame, text="🎨 Scene Preview")
        self.setup_preview_tab(preview_frame)

        # Quick Demo tab
        demo_frame = ttk.Frame(notebook)
        notebook.add(demo_frame, text="🚀 Quick Demo")
        self.setup_demo_tab(demo_frame)

        # Handle window closing
        self.window.protocol("WM_DELETE_WINDOW", self.close)

    def setup_objects_tab(self, parent):
        """Setup the game objects management tab"""
        # Objects list
        list_frame = ttk.LabelFrame(parent, text="Game Objects")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Treeview for objects
        columns = ("Name", "Type", "Position", "Size", "Velocity")
        self.objects_tree = ttk.Treeview(
            list_frame, columns=columns, show="headings", height=10
        )

        for col in columns:
            self.objects_tree.heading(col, text=col)
            self.objects_tree.column(col, width=120)

        # Scrollbar for tree
        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.objects_tree.yview
        )
        self.objects_tree.configure(yscrollcommand=scrollbar.set)

        self.objects_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons frame
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(
            buttons_frame, text="🎯 Create Object", command=self.create_object
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            buttons_frame, text="📝 Edit Properties", command=self.edit_object
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            buttons_frame, text="🗑️ Delete Object", command=self.delete_object
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="🔄 Refresh", command=self.refresh_objects).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(
            buttons_frame, text="🧹 Clear All", command=self.clear_all_objects
        ).pack(side=tk.LEFT, padx=2)

        self.refresh_objects()

    def setup_physics_tab(self, parent):
        """Setup the physics configuration tab"""
        # Global physics settings
        global_frame = ttk.LabelFrame(parent, text="Global Physics Settings")
        global_frame.pack(fill=tk.X, padx=5, pady=5)

        # Gravity control
        gravity_frame = ttk.Frame(global_frame)
        gravity_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(gravity_frame, text="Gravity:").pack(side=tk.LEFT)
        self.gravity_var = tk.DoubleVar(value=9.8)
        gravity_scale = ttk.Scale(
            gravity_frame,
            from_=0,
            to=20,
            variable=self.gravity_var,
            orient=tk.HORIZONTAL,
        )
        gravity_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))

        gravity_label = ttk.Label(gravity_frame, text="9.8")
        gravity_label.pack(side=tk.LEFT)

        def update_gravity_label(*args):
            gravity_label.config(text=f"{self.gravity_var.get():.1f}")
            self.ide.interpreter.game_manager.set_gravity(self.gravity_var.get())

        self.gravity_var.trace("w", update_gravity_label)

        ttk.Button(
            gravity_frame,
            text="🌍 Apply Gravity",
            command=lambda: self.ide.interpreter.game_manager.set_gravity(
                self.gravity_var.get()
            ),
        ).pack(side=tk.RIGHT, padx=5)

        # Physics simulation controls
        sim_frame = ttk.LabelFrame(parent, text="Simulation Controls")
        sim_frame.pack(fill=tk.X, padx=5, pady=5)

        control_frame = ttk.Frame(sim_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(
            control_frame, text="▶️ Start Physics", command=self.start_physics
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            control_frame, text="⏸️ Pause Physics", command=self.pause_physics
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            control_frame, text="⏹️ Stop Physics", command=self.stop_physics
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            control_frame, text="🔄 Single Step", command=self.step_physics
        ).pack(side=tk.LEFT, padx=2)

        # Physics info
        info_frame = ttk.LabelFrame(parent, text="Physics Information")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.physics_info = tk.Text(info_frame, height=8, font=("Consolas", 10))
        info_scrollbar = ttk.Scrollbar(
            info_frame, orient=tk.VERTICAL, command=self.physics_info.yview
        )
        self.physics_info.configure(yscrollcommand=info_scrollbar.set)
        self.physics_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.update_physics_info()

    def setup_preview_tab(self, parent):
        """Setup the scene preview tab"""
        # Canvas for scene preview
        canvas_frame = ttk.LabelFrame(parent, text="Scene Preview")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.preview_canvas = tk.Canvas(canvas_frame, bg="white", width=600, height=400)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Preview controls
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(
            control_frame, text="🎨 Render Scene", command=self.render_preview
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            control_frame, text="🔄 Auto-Refresh", command=self.toggle_auto_refresh
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="💾 Save Scene", command=self.save_scene).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(control_frame, text="📁 Load Scene", command=self.load_scene).pack(
            side=tk.LEFT, padx=2
        )

        self.auto_refresh = False
        self.render_preview()

    def setup_demo_tab(self, parent):
        """Setup the quick demo tab"""
        # Demo buttons
        demos = [
            ("🏓 Pong Game", "pong", "Classic Pong with paddles and ball physics"),
            ("🌍 Physics Demo", "physics", "Falling objects with gravity simulation"),
            ("🏃 Platformer", "platformer", "Jump and run game with platforms"),
            ("🎯 Collision Test", "collision", "Test collision detection systems"),
        ]

        for name, demo_type, description in demos:
            demo_frame = ttk.LabelFrame(parent, text=name)
            demo_frame.pack(fill=tk.X, padx=5, pady=5)

            desc_label = ttk.Label(
                demo_frame, text=description, font=("Arial", 9), foreground="gray"
            )
            desc_label.pack(anchor=tk.W, padx=5, pady=2)

            ttk.Button(
                demo_frame,
                text=f"🚀 Run {name}",
                command=lambda dt=demo_type: self.run_demo(dt),
            ).pack(padx=5, pady=5, anchor=tk.W)

        # Custom demo section
        custom_frame = ttk.LabelFrame(parent, text="🛠️ Custom Demo")
        custom_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(
            custom_frame,
            text="Create your own demo with custom parameters:",
            font=("Arial", 9),
            foreground="gray",
        ).pack(anchor=tk.W, padx=5, pady=2)

        params_frame = ttk.Frame(custom_frame)
        params_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(params_frame, text="Objects:").pack(side=tk.LEFT)
        self.demo_objects = tk.IntVar(value=5)
        ttk.Spinbox(
            params_frame, from_=1, to=20, textvariable=self.demo_objects, width=5
        ).pack(side=tk.LEFT, padx=5)

        ttk.Label(params_frame, text="Gravity:").pack(side=tk.LEFT, padx=(10, 0))
        self.demo_gravity = tk.DoubleVar(value=9.8)
        ttk.Spinbox(
            params_frame,
            from_=0,
            to=20,
            textvariable=self.demo_gravity,
            width=8,
            increment=0.1,
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            custom_frame, text="🎮 Run Custom Demo", command=self.run_custom_demo
        ).pack(padx=5, pady=5, anchor=tk.W)

    def create_object(self):
        """Create a new game object"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Create Game Object")
        dialog.geometry("400x300")
        dialog.transient(self.window)

        # Object properties
        ttk.Label(dialog, text="Object Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=5)

        ttk.Label(dialog, text="Object Type:").pack(pady=5)
        type_var = tk.StringVar(value="rectangle")
        type_combo = ttk.Combobox(dialog, textvariable=type_var, width=30)
        type_combo["values"] = (
            "rectangle",
            "circle",
            "sprite",
            "platform",
            "projectile",
        )
        type_combo.pack(pady=5)

        # Position
        pos_frame = ttk.Frame(dialog)
        pos_frame.pack(pady=5)
        ttk.Label(pos_frame, text="X:").pack(side=tk.LEFT)
        x_var = tk.DoubleVar(value=100)
        ttk.Entry(pos_frame, textvariable=x_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(pos_frame, text="Y:").pack(side=tk.LEFT)
        y_var = tk.DoubleVar(value=100)
        ttk.Entry(pos_frame, textvariable=y_var, width=10).pack(side=tk.LEFT, padx=5)

        # Size
        size_frame = ttk.Frame(dialog)
        size_frame.pack(pady=5)
        ttk.Label(size_frame, text="Width:").pack(side=tk.LEFT)
        width_var = tk.DoubleVar(value=32)
        ttk.Entry(size_frame, textvariable=width_var, width=10).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Label(size_frame, text="Height:").pack(side=tk.LEFT)
        height_var = tk.DoubleVar(value=32)
        ttk.Entry(size_frame, textvariable=height_var, width=10).pack(
            side=tk.LEFT, padx=5
        )

        def do_create():
            name = name_entry.get().strip()
            obj_type = type_var.get()
            x, y = x_var.get(), y_var.get()
            width, height = width_var.get(), height_var.get()

            if name and obj_type:
                if self.ide.interpreter.game_manager.create_object(
                    name, obj_type, x, y, width, height
                ):
                    self.refresh_objects()
                    self.render_preview()
                    dialog.destroy()
                    messagebox.showinfo("Success", f"Created object '{name}'")
                else:
                    messagebox.showerror("Error", "Failed to create object")
            else:
                messagebox.showwarning(
                    "Warning", "Please enter object name and select type"
                )

        ttk.Button(dialog, text="🎯 Create", command=do_create).pack(pady=10)

    def edit_object(self):
        """Edit selected object properties"""
        selection = self.objects_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an object to edit")
            return

        obj_name = self.objects_tree.item(selection[0])["values"][0]
        obj_info = self.ide.interpreter.game_manager.get_object_info(obj_name)

        if not obj_info:
            messagebox.showerror("Error", f"Object '{obj_name}' not found")
            return

        dialog = tk.Toplevel(self.window)
        dialog.title(f"Edit Object: {obj_name}")
        dialog.geometry("400x300")
        dialog.transient(self.window)

        # Current properties
        ttk.Label(dialog, text=f"Editing: {obj_name}", font=("Arial", 12, "bold")).pack(
            pady=5
        )

        # Position controls
        pos_frame = ttk.LabelFrame(dialog, text="Position")
        pos_frame.pack(fill=tk.X, padx=5, pady=5)

        pos_control_frame = ttk.Frame(pos_frame)
        pos_control_frame.pack(pady=5)

        ttk.Label(pos_control_frame, text="X:").pack(side=tk.LEFT)
        x_var = tk.DoubleVar(value=obj_info["x"])
        ttk.Entry(pos_control_frame, textvariable=x_var, width=10).pack(
            side=tk.LEFT, padx=5
        )

        ttk.Label(pos_control_frame, text="Y:").pack(side=tk.LEFT)
        y_var = tk.DoubleVar(value=obj_info["y"])
        ttk.Entry(pos_control_frame, textvariable=y_var, width=10).pack(
            side=tk.LEFT, padx=5
        )

        # Velocity controls
        vel_frame = ttk.LabelFrame(dialog, text="Velocity")
        vel_frame.pack(fill=tk.X, padx=5, pady=5)

        vel_control_frame = ttk.Frame(vel_frame)
        vel_control_frame.pack(pady=5)

        ttk.Label(vel_control_frame, text="VX:").pack(side=tk.LEFT)
        vx_var = tk.DoubleVar(value=0)
        ttk.Entry(vel_control_frame, textvariable=vx_var, width=10).pack(
            side=tk.LEFT, padx=5
