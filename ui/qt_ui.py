"""
PySide6 UI Implementation for Time Warp IDE

This module provides a modern PySide6-based implementation of the UI interface,
offering responsive UI components with Qt's rich feature set and modern design.
"""

import sys
from typing import Any, Optional, Dict, List, Callable
from pathlib import Path

try:
    from PySide6.QtWidgets import (
        QApplication,
        QMainWindow,
        QWidget,
        QVBoxLayout,
        QHBoxLayout,
        QSplitter,
        QTextEdit,
        QPlainTextEdit,
        QMenuBar,
        QMenu,
        QStatusBar,
        QLabel,
        QGraphicsView,
        QGraphicsScene,
        QGraphicsItem,
        QTabWidget,
        QTreeWidget,
        QTreeWidgetItem,
        QToolBar,
        QPushButton,
        QComboBox,
        QLineEdit,
        QFrame,
        QScrollArea,
        QGroupBox,
        QProgressBar,
        QMessageBox,
        QFileDialog,
        QColorDialog,
        QFontDialog,
        QInputDialog,
        QDialog,
        QDialogButtonBox,
    )
    from PySide6.QtGui import (
        QPainter,
        QPen,
        QBrush,
        QColor,
        QFont,
        QAction,
        QKeySequence,
        QIcon,
        QPixmap,
        QFontMetrics,
        QSyntaxHighlighter,
        QTextCharFormat,
        QTextDocument,
    )
    from PySide6.QtCore import (
        Qt,
        QTimer,
        QPointF,
        QRectF,
        Signal,
        QObject,
        QThread,
        QEvent,
        QMimeData,
        QUrl,
        QSize,
        QSettings,
    )

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False
    # Define dummy classes for type hints when PySide6 is not available
    QApplication = Any
    QMainWindow = Any
    QWidget = Any
    QVBoxLayout = Any
    QHBoxLayout = Any
    QSplitter = Any
    QTextEdit = Any
    QPlainTextEdit = Any
    QMenuBar = Any
    QMenu = Any
    QStatusBar = Any
    QLabel = Any
    QGraphicsView = Any
    QGraphicsScene = Any
    QGraphicsItem = Any
    QTabWidget = Any
    QTreeWidget = Any
    QTreeWidgetItem = Any
    QToolBar = Any
    QPushButton = Any
    QComboBox = Any
    QLineEdit = Any
    QFrame = Any
    QScrollArea = Any
    QGroupBox = Any
    QProgressBar = Any
    QMessageBox = Any
    QFileDialog = Any
    QColorDialog = Any
    QFontDialog = Any
    QInputDialog = Any
    QDialog = Any
    QDialogButtonBox = Any
    QPainter = Any
    QPen = Any
    QBrush = Any
    QColor = Any
    QFont = Any
    QAction = Any
    QKeySequence = Any
    QIcon = Any
    QPixmap = Any
    QFontMetrics = Any
    QSyntaxHighlighter = Any
    QTextCharFormat = Any
    QTextDocument = Any
    Qt = Any
    QTimer = Any
    QPointF = Any
    QRectF = Any
    Signal = Any
    QObject = Any
    QThread = Any
    QEvent = Any
    QMimeData = Any
    QUrl = Any
    QSize = Any
    QSettings = Any

from .base import (
    UIComponent,
    TextWidget,
    CanvasWidget,
    MenuBar,
    Menu,
    StatusBar,
    MainWindow,
    Splitter,
    UIApplication,
    UIFactory,
    UICallback,
)


class TimeWarpSyntaxHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Time Warp languages"""

    def __init__(self, document: QTextDocument) -> None:
        super().__init__(document)

        # Define formats for different syntax elements
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("#0000ff"))  # Blue
        self.keyword_format.setFontWeight(QFont.Weight.Bold)

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#008000"))  # Green

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#a31515"))  # Dark red

        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor("#09885a"))  # Teal

        # Keywords for different languages
        self.pilot_keywords = {
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
        }

        self.basic_keywords = {
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
            "DATA",
            "READ",
            "RESTORE",
        }

        self.logo_keywords = {
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
            "SETHEADING",
            "SETH",
            "REPEAT",
            "TO",
            "END",
        }

    def highlightBlock(self, text: str) -> None:
        """Highlight a block of text"""
        # Simple highlighting - could be enhanced with more sophisticated parsing
        import re

        # Highlight PILOT commands (single letter followed by colon)
        pilot_pattern = r"\b[A-Z]:\b"
        for match in re.finditer(pilot_pattern, text):
            self.setFormat(
                match.start(), match.end() - match.start(), self.keyword_format
            )

        # Highlight BASIC keywords
        for keyword in self.basic_keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"
            for match in re.finditer(pattern, text, re.IGNORECASE):
                self.setFormat(
                    match.start(), match.end() - match.start(), self.keyword_format
                )

        # Highlight Logo keywords
        for keyword in self.logo_keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"
            for match in re.finditer(pattern, text, re.IGNORECASE):
                self.setFormat(
                    match.start(), match.end() - match.start(), self.keyword_format
                )

        # Highlight strings
        string_pattern = r'"[^"]*"|\'[^\']*\''
        for match in re.finditer(string_pattern, text):
            self.setFormat(
                match.start(), match.end() - match.start(), self.string_format
            )

        # Highlight numbers
        number_pattern = r"\b\d+\.?\d*\b"
        for match in re.finditer(number_pattern, text):
            self.setFormat(
                match.start(), match.end() - match.start(), self.number_format
            )

        # Highlight comments (REM in BASIC, # in Python-like syntax)
        comment_pattern = r"(REM.*$|#.*$)"
        for match in re.finditer(comment_pattern, text, re.IGNORECASE):
            self.setFormat(
                match.start(), match.end() - match.start(), self.comment_format
            )


class QtTextWidget(TextWidget):
    """PySide6 text widget implementation with syntax highlighting"""

    def __init__(self, readonly: bool = False):
        if not PYSIDE6_AVAILABLE:
            raise ImportError("PySide6 is not available")
        self.widget = QPlainTextEdit()
        self.widget.setReadOnly(readonly)

        # Set up modern font and styling
        font = (
            QFont("JetBrains Mono", 11)
            if QFont("JetBrains Mono").exactMatch()
            else QFont("Consolas", 11)
        )
        self.widget.setFont(font)

        # Enable line numbers and syntax highlighting
        self.highlighter = TimeWarpSyntaxHighlighter(self.widget.document())

    @property
    def widget(self) -> QPlainTextEdit:
        """Get the underlying widget"""
        return self._widget

    @widget.setter
    def widget(self, widget: QPlainTextEdit) -> None:
        """Set the underlying widget"""
        self._widget = widget

    def show(self) -> None:
        self.widget.show()

    def hide(self) -> None:
        self.widget.hide()

    def destroy(self) -> None:
        self.widget.deleteLater()

    def set_text(self, text: str) -> None:
        self.widget.setPlainText(text)

    def get_text(self) -> str:
        return self.widget.toPlainText()

    def append_text(self, text: str) -> None:
        self.widget.appendPlainText(text)

    def clear(self) -> None:
        self.widget.clear()

    def set_readonly(self, readonly: bool) -> None:
        self.widget.setReadOnly(readonly)

    def get_cursor_position(self) -> tuple[int, int]:
        """Get current cursor position (line, column)"""
        cursor = self.widget.textCursor()
        return cursor.blockNumber() + 1, cursor.columnNumber() + 1

    def set_cursor_position(self, line: int, column: int) -> None:
        """Set cursor position"""
        cursor = self.widget.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)
        cursor.movePosition(cursor.MoveOperation.Down, cursor.MoveAnchor, line - 1)
        cursor.movePosition(cursor.MoveOperation.Right, cursor.MoveAnchor, column - 1)
        self.widget.setTextCursor(cursor)

    def highlight_line(self, line: int, color: str = "#e3f2fd") -> None:
        """Highlight a specific line"""
        # This would require more complex implementation with extra selections
        pass


class QtCanvasWidget(CanvasWidget):
    """PySide6 canvas widget implementation"""

    def __init__(self, width: int = 400, height: int = 400):
        if not PYSIDE6_AVAILABLE:
            raise ImportError("PySide6 is not available")
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setFixedSize(width, height)
        self._items = []

    def show(self) -> None:
        self.view.show()

    def hide(self) -> None:
        self.view.hide()

    def destroy(self) -> None:
        self.view.deleteLater()

    def clear(self) -> None:
        self.scene.clear()
        self._items.clear()

    def draw_line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: str = "black",
        width: int = 1,
    ) -> None:
        pen = QPen(QColor(color), width)
        line = self.scene.addLine(x1, y1, x2, y2, pen)
        self._items.append(line)

    def draw_circle(
        self, x: float, y: float, radius: float, color: str = "black", width: int = 1
    ) -> None:
        pen = QPen(QColor(color), width)
        brush = QBrush(Qt.BrushStyle.NoBrush)
        circle = self.scene.addEllipse(
            x - radius, y - radius, radius * 2, radius * 2, pen, brush
        )
        self._items.append(circle)

    def draw_rectangle(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: str = "black",
        width: int = 1,
    ) -> None:
        pen = QPen(QColor(color), width)
        brush = QBrush(Qt.BrushStyle.NoBrush)
        rect = self.scene.addRect(x1, y1, x2 - x1, y2 - y1, pen, brush)
        self._items.append(rect)

    def draw_text(self, x: float, y: float, text: str, color: str = "black") -> None:
        text_item = self.scene.addText(text)
        text_item.setPos(x, y)
        text_item.setDefaultTextColor(QColor(color))
        self._items.append(text_item)


class QtMenuBar(MenuBar):
    """PySide6 menu bar implementation"""

    def __init__(self, menu_bar: QMenuBar):
        self.menu_bar = menu_bar
        self._menus = {}

    def show(self) -> None:
        pass  # Menu bar is always visible

    def hide(self) -> None:
        pass  # Menu bar cannot be hidden

    def destroy(self) -> None:
        pass  # Menu bar is managed by main window

    def add_menu(self, name: str) -> Menu:
        menu = self.menu_bar.addMenu(name)
        qt_menu = QtMenu(menu)
        self._menus[name] = qt_menu
        return qt_menu


class QtMenu(Menu):
    """PySide6 menu implementation"""

    def __init__(self, menu: QMenu):
        self.menu = menu

    def show(self) -> None:
        pass

    def hide(self) -> None:
        pass

    def destroy(self) -> None:
        pass

    def add_command(
        self, label: str, command: UICallback, accelerator: Optional[str] = None
    ) -> None:
        action = QAction(label, self.menu)
        if accelerator:
            action.setShortcut(QKeySequence(accelerator))
        action.triggered.connect(command)
        self.menu.addAction(action)

    def add_separator(self) -> None:
        self.menu.addSeparator()

    def add_submenu(self, label: str) -> Menu:
        submenu = self.menu.addMenu(label)
        return QtMenu(submenu)


class QtStatusBar(StatusBar):
    """PySide6 status bar implementation"""

    def __init__(self, status_bar: QStatusBar):
        self.status_bar = status_bar
        self.label = QLabel()
        self.status_bar.addWidget(self.label)

    def show(self) -> None:
        self.status_bar.show()

    def hide(self) -> None:
        self.status_bar.hide()

    def destroy(self) -> None:
        pass

    def set_text(self, text: str) -> None:
        self.label.setText(text)


class QtSplitter(Splitter):
    """PySide6 splitter implementation"""

    def __init__(self):
        if not PYSIDE6_AVAILABLE:
            raise ImportError("PySide6 is not available")
        self.splitter = QSplitter()

    def show(self) -> None:
        self.splitter.show()

    def hide(self) -> None:
        self.splitter.hide()

    def destroy(self) -> None:
        self.splitter.deleteLater()

    def add_widget(self, widget: UIComponent, stretch: int = 1) -> None:
        if hasattr(widget, "widget"):
            self.splitter.addWidget(widget.widget)
        elif hasattr(widget, "view"):
            self.splitter.addWidget(widget.view)
        elif hasattr(widget, "splitter"):
            self.splitter.addWidget(widget.splitter)

    def set_orientation(self, horizontal: bool) -> None:
        orientation = (
            Qt.Orientation.Horizontal if horizontal else Qt.Orientation.Vertical
        )
        self.splitter.setOrientation(orientation)


class QtMainWindow(MainWindow):
    """Modern PySide6 main window implementation with advanced features"""

    def __init__(
        self, title: str = "Time Warp IDE", width: int = 1400, height: int = 900
    ):
        if not PYSIDE6_AVAILABLE:
            raise ImportError("PySide6 is not available")

        super().__init__(title, width, height)

        # Initialize components first
        self._menu_bar = None
        self._status_bar = None
        self._editor = None
        self._output = None
        self._canvas = None
        self._variables_tree = None
        self._run_button = None
        self._stop_button = None
        self._language_combo = None

        # Create main window
        self.window = QMainWindow()
        self.window.setWindowTitle(title)
        self.window.resize(width, height)

        # Set up modern styling
        self.window.setStyleSheet(
            """
            QMainWindow {
                background-color: #f8f9fa;
            }
            QMenuBar {
                background-color: #ffffff;
                border-bottom: 1px solid #e1e5e9;
                padding: 4px;
            }
            QMenuBar::item {
                padding: 8px 12px;
                margin: 0px 2px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QStatusBar {
                background-color: #ffffff;
                border-top: 1px solid #e1e5e9;
                padding: 4px;
            }
            QTabWidget::pane {
                border: 1px solid #e1e5e9;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #f5f5f5;
                border: 1px solid #e1e5e9;
                padding: 8px 16px;
                margin-right: 2px;
                border-radius: 4px 4px 0 0;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom: 2px solid #1976d2;
            }
            QTabBar::tab:hover {
                background-color: #e3f2fd;
            }
        """
        )

        # Create central widget with modern layout
        self.setup_central_widget()

    def setup_central_widget(self) -> None:
        """Set up the central widget with modern layout"""
        central_widget = QWidget()
        self.window.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        # Create toolbar
        self.setup_toolbar()

        # Create main splitter (editor | right panel)
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self.main_splitter)

        # Left side: Editor container
        self.setup_editor_panel()

        # Right side: Tabbed panel
        self.setup_right_panel()

        # Set splitter proportions
        self.main_splitter.setSizes([800, 600])

    def setup_toolbar(self) -> None:
        """Set up modern toolbar"""
        self.toolbar = self.window.addToolBar("Main Toolbar")
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolbar.setMovable(False)

        # Style toolbar
        self.toolbar.setStyleSheet(
            """
            QToolBar {
                background-color: #ffffff;
                border-bottom: 1px solid #e1e5e9;
                padding: 4px;
                spacing: 8px;
            }
            QToolButton {
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 4px;
                padding: 8px 12px;
                color: #424242;
                font-weight: 500;
            }
            QToolButton:hover {
                background-color: #e3f2fd;
                border: 1px solid #bbdefb;
            }
            QToolButton:pressed {
                background-color: #bbdefb;
            }
        """
        )

    def setup_editor_panel(self) -> None:
        """Set up the editor panel"""
        editor_container = QWidget()
        editor_layout = QVBoxLayout(editor_container)
        editor_layout.setContentsMargins(0, 0, 0, 0)

        # Editor controls
        controls_layout = QHBoxLayout()

        # Language selector
        self._language_combo = QComboBox()
        self._language_combo.addItems(
            ["PILOT", "BASIC", "Logo", "Python", "JavaScript", "Perl"]
        )
        self._language_combo.setCurrentText("PILOT")
        self._language_combo.setMaximumWidth(120)
        controls_layout.addWidget(QLabel("Language:"))
        controls_layout.addWidget(self._language_combo)

        controls_layout.addStretch()

        # Run button
        self._run_button = QPushButton("▶ Run")
        self._run_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """
        )
        controls_layout.addWidget(self._run_button)

        # Stop button
        self._stop_button = QPushButton("⏹ Stop")
        self._stop_button.setStyleSheet(
            """
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
        """
        )
        controls_layout.addWidget(self._stop_button)

        editor_layout.addLayout(controls_layout)

        # Editor widget will be added here
        self.editor_container = QWidget()
        editor_layout.addWidget(self.editor_container)

        self.main_splitter.addWidget(editor_container)

    def setup_right_panel(self) -> None:
        """Set up the right panel with tabs"""
        self.right_tabs = QTabWidget()

        # Output tab
        self.output_tab = QWidget()
        output_layout = QVBoxLayout(self.output_tab)
        # Output widget will be added here
        self.right_tabs.addTab(self.output_tab, "Output")

        # Variables tab
        self.variables_tab = QWidget()
        variables_layout = QVBoxLayout(self.variables_tab)
        # Variables widget will be added here
        self.right_tabs.addTab(self.variables_tab, "Variables")

        # Graphics tab
        self.graphics_tab = QWidget()
        graphics_layout = QVBoxLayout(self.graphics_tab)
        # Graphics widget will be added here
        self.right_tabs.addTab(self.graphics_tab, "Graphics")

        # Help tab
        self.help_tab = QWidget()
        help_layout = QVBoxLayout(self.help_tab)
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setPlainText(
            "Time Warp IDE Help\n\nSelect a language and start coding!"
        )
        help_layout.addWidget(help_text)
        self.right_tabs.addTab(self.help_tab, "Help")

        self.main_splitter.addWidget(self.right_tabs)

    def show(self) -> None:
        self.window.show()

    def hide(self) -> None:
        self.window.hide()

    def destroy(self) -> None:
        self.window.deleteLater()

    def set_title(self, title: str) -> None:
        self.window.setWindowTitle(title)

    def set_size(self, width: int, height: int) -> None:
        self.window.resize(width, height)

    def center_on_screen(self) -> None:
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.window.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.window.move(x, y)

    def create_menu_bar(self) -> MenuBar:
        self._menu_bar = QtMenuBar(self.window.menuBar())
        return self._menu_bar

    def create_status_bar(self) -> StatusBar:
        self._status_bar = QtStatusBar(self.window.statusBar())
        return self._status_bar

    def create_text_editor(self) -> TextWidget:
        self._editor = QtTextWidget(readonly=False)
        # Add to editor container
        layout = QVBoxLayout(self.editor_container)
        layout.addWidget(self._editor.widget)
        return self._editor

    def create_output_panel(self) -> TextWidget:
        self._output = QtTextWidget(readonly=True)
        # Add to output tab
        self.output_tab.layout().addWidget(self._output.widget)
        return self._output

    def create_canvas(self, width: int = 400, height: int = 400) -> CanvasWidget:
        self._canvas = QtCanvasWidget(width, height)
        # Add to graphics tab
        self.graphics_tab.layout().addWidget(self._canvas.view)
        return self._canvas

    def create_variables_tree(self) -> QTreeWidget:
        """Create variables tree widget"""
        tree = QTreeWidget()
        tree.setHeaderLabels(["Variable", "Value"])
        tree.setColumnWidth(0, 150)
        tree.setStyleSheet(
            """
            QTreeWidget {
                background-color: #ffffff;
                border: 1px solid #e1e5e9;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                border: none;
                border-bottom: 1px solid #e1e5e9;
                padding: 8px;
                font-weight: bold;
            }
        """
        )
        self.variables_tab.layout().addWidget(tree)
        return tree

    def create_splitter(self) -> Splitter:
        return QtSplitter()

    @property
    def menu_bar(self) -> Optional[QtMenuBar]:
        return self._menu_bar

    @property
    def status_bar(self) -> Optional[QtStatusBar]:
        return self._status_bar

    @property
    def editor(self) -> Optional[QtTextWidget]:
        return self._editor

    @property
    def output(self) -> Optional[QtTextWidget]:
        return self._output

    @property
    def canvas(self) -> Optional[QtCanvasWidget]:
        return self._canvas

    @property
    def window(self) -> QMainWindow:
        """Get the underlying QMainWindow"""
        return self._window

    @window.setter
    def window(self, window: QMainWindow) -> None:
        """Set the underlying QMainWindow"""
        self._window = window

    @property
    def run_button(self) -> QPushButton:
        """Get run button widget"""
        return self._run_button

    @run_button.setter
    def run_button(self, button: QPushButton) -> None:
        """Set run button widget"""
        self._run_button = button

    @property
    def stop_button(self) -> QPushButton:
        """Get stop button widget"""
        return self._stop_button

    @stop_button.setter
    def stop_button(self, button: QPushButton) -> None:
        """Set stop button widget"""
        self._stop_button = button

    @property
    def language_combo(self) -> QComboBox:
        """Get language combo box widget"""
        return self._language_combo

    @language_combo.setter
    def language_combo(self, combo: QComboBox) -> None:
        """Set language combo box widget"""
        self._language_combo = combo


class QtUIApplication(UIApplication):
    """PySide6 application implementation"""

    def __init__(self):
        if not PYSIDE6_AVAILABLE:
            raise ImportError("PySide6 is not available")
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)

    def create_main_window(
        self, title: str = "Time Warp IDE", width: int = 1200, height: int = 800
    ) -> MainWindow:
        return QtMainWindow(title, width, height)

    def run_event_loop(self) -> int:
        return self.app.exec()

    def quit(self) -> None:
        self.app.quit()

    def process_events(self) -> None:
        self.app.processEvents()

    def schedule_callback(self, callback: UICallback, delay_ms: int = 0) -> None:
        if delay_ms == 0:
            # Schedule for next event loop iteration
            QTimer.singleShot(0, callback)
        else:
            QTimer.singleShot(delay_ms, callback)


class QtUIFactory(UIFactory):
    """Factory for creating PySide6 UI components"""

    def create_application(self) -> UIApplication:
        return QtUIApplication()

    def is_available(self) -> bool:
        return PYSIDE6_AVAILABLE

    @property
    def name(self) -> str:
        return "PySide6"

    @property
    def version(self) -> str:
        if PYSIDE6_AVAILABLE:
            try:
                import PySide6

                return PySide6.__version__
            except AttributeError:
                return "Unknown"
        return "Not Available"
