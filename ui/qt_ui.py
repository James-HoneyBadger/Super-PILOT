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
    """Modern PySide6 main window implementation with Material Design and advanced features"""

    def __init__(
        self, title: str = "Time Warp IDE", width: int = 1400, height: int = 900
    ):
        if not PYSIDE6_AVAILABLE:
            raise ImportError("PySide6 is not available")

        super().__init__(title, width, height)

        # Create main window
        self.window = QMainWindow()
        self.window.setWindowTitle(title)
        self.window.resize(width, height)

        # Initialize theme
        self.dark_mode = False
        self.setup_theme()

        # Create central widget with modern layout
        self.setup_central_widget()

        # Initialize components
        self._menu_bar = None
        self._status_bar = None
        self._editor = None
        self._output = None
        self._canvas = None
        self._variables_tree = None

        # Setup window properties
        self.window.setMinimumSize(1000, 700)
        self.window.setWindowIcon(QIcon())  # TODO: Add app icon

    def setup_theme(self) -> None:
        """Setup modern Material Design theme"""
        if self.dark_mode:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def apply_light_theme(self) -> None:
        """Apply light Material Design theme"""
        self.window.setStyleSheet(
            """
            /* Main Window */
            QMainWindow {
                background-color: #fafafa;
                color: #212121;
            }

            /* Menu Bar */
            QMenuBar {
                background-color: #ffffff;
                border-bottom: 1px solid #e0e0e0;
                padding: 4px 8px;
                font-size: 13px;
            }
            QMenuBar::item {
                padding: 6px 12px;
                margin: 0px 2px;
                border-radius: 4px;
                color: #424242;
            }
            QMenuBar::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QMenuBar::item:pressed {
                background-color: #bbdefb;
            }

            /* Menus */
            QMenu {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
                color: #424242;
            }
            QMenu::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QMenu::separator {
                height: 1px;
                background-color: #e0e0e0;
                margin: 4px 8px;
            }

            /* Status Bar */
            QStatusBar {
                background-color: #ffffff;
                border-top: 1px solid #e0e0e0;
                padding: 4px 8px;
                font-size: 12px;
                color: #757575;
            }

            /* Toolbar */
            QToolBar {
                background-color: #ffffff;
                border-bottom: 1px solid #e0e0e0;
                padding: 8px;
                spacing: 8px;
            }
            QToolButton {
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 6px;
                padding: 8px 12px;
                color: #424242;
                font-weight: 500;
                font-size: 13px;
            }
            QToolButton:hover {
                background-color: #f5f5f5;
                border: 1px solid #e0e0e0;
            }
            QToolButton:pressed {
                background-color: #e0e0e0;
            }

            /* Tab Widget */
            QTabWidget::pane {
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #f5f5f5;
                border: 1px solid #e0e0e0;
                padding: 10px 16px;
                margin-right: 2px;
                border-radius: 6px 6px 0 0;
                color: #424242;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom: 2px solid #1976d2;
                color: #1976d2;
            }
            QTabBar::tab:hover {
                background-color: #e8f5e8;
            }

            /* Buttons */
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 16px;
                color: #424242;
                font-weight: 500;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border: 1px solid #bdbdbd;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
            QPushButton:disabled {
                background-color: #f5f5f5;
                color: #bdbdbd;
                border: 1px solid #e0e0e0;
            }

            /* Combo Box */
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 6px 12px;
                color: #424242;
                font-size: 13px;
                min-width: 100px;
            }
            QComboBox:hover {
                border: 1px solid #bdbdbd;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                selection-background-color: #e3f2fd;
                selection-color: #1976d2;
            }

            /* Tree Widget */
            QTreeWidget {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                alternate-background-color: #fafafa;
            }
            QTreeWidget::item {
                padding: 4px;
                border-bottom: 1px solid #f5f5f5;
            }
            QTreeWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QTreeWidget::item:hover {
                background-color: #f5f5f5;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                border: none;
                border-bottom: 1px solid #e0e0e0;
                padding: 8px;
                font-weight: bold;
                color: #424242;
            }

            /* Text Edit */
            QPlainTextEdit {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px;
                font-family: 'JetBrains Mono', 'Consolas', 'Monaco', monospace;
                font-size: 13px;
                color: #212121;
                selection-background-color: #e3f2fd;
            }
            QPlainTextEdit:focus {
                border: 2px solid #1976d2;
            }

            /* Graphics View */
            QGraphicsView {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
            }

            /* Scroll Bars */
            QScrollBar:vertical {
                background-color: #f5f5f5;
                width: 16px;
                border-radius: 8px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background-color: #bdbdbd;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #9e9e9e;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """
        )

    def apply_dark_theme(self) -> None:
        """Apply dark Material Design theme"""
        self.window.setStyleSheet(
            """
            /* Main Window */
            QMainWindow {
                background-color: #121212;
                color: #ffffff;
            }

            /* Menu Bar */
            QMenuBar {
                background-color: #1e1e1e;
                border-bottom: 1px solid #333333;
                padding: 4px 8px;
                font-size: 13px;
            }
            QMenuBar::item {
                padding: 6px 12px;
                margin: 0px 2px;
                border-radius: 4px;
                color: #ffffff;
            }
            QMenuBar::item:selected {
                background-color: #333333;
                color: #64b5f6;
            }
            QMenuBar::item:pressed {
                background-color: #424242;
            }

            /* Menus */
            QMenu {
                background-color: #1e1e1e;
                border: 1px solid #333333;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
                color: #ffffff;
            }
            QMenu::item:selected {
                background-color: #333333;
                color: #64b5f6;
            }
            QMenu::separator {
                height: 1px;
                background-color: #333333;
                margin: 4px 8px;
            }

            /* Status Bar */
            QStatusBar {
                background-color: #1e1e1e;
                border-top: 1px solid #333333;
                padding: 4px 8px;
                font-size: 12px;
                color: #9e9e9e;
            }

            /* Toolbar */
            QToolBar {
                background-color: #1e1e1e;
                border-bottom: 1px solid #333333;
                padding: 8px;
                spacing: 8px;
            }
            QToolButton {
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 6px;
                padding: 8px 12px;
                color: #ffffff;
                font-weight: 500;
                font-size: 13px;
            }
            QToolButton:hover {
                background-color: #333333;
                border: 1px solid #424242;
            }
            QToolButton:pressed {
                background-color: #424242;
            }

            /* Tab Widget */
            QTabWidget::pane {
                border: 1px solid #333333;
                border-radius: 6px;
                background-color: #1e1e1e;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                border: 1px solid #333333;
                padding: 10px 16px;
                margin-right: 2px;
                border-radius: 6px 6px 0 0;
                color: #ffffff;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: #1e1e1e;
                border-bottom: 2px solid #64b5f6;
                color: #64b5f6;
            }
            QTabBar::tab:hover {
                background-color: #333333;
            }

            /* Buttons */
            QPushButton {
                background-color: #2d2d2d;
                border: 1px solid #424242;
                border-radius: 6px;
                padding: 8px 16px;
                color: #ffffff;
                font-weight: 500;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #333333;
                border: 1px solid #616161;
            }
            QPushButton:pressed {
                background-color: #424242;
            }
            QPushButton:disabled {
                background-color: #1e1e1e;
                color: #616161;
                border: 1px solid #424242;
            }

            /* Combo Box */
            QComboBox {
                background-color: #2d2d2d;
                border: 1px solid #424242;
                border-radius: 6px;
                padding: 6px 12px;
                color: #ffffff;
                font-size: 13px;
                min-width: 100px;
            }
            QComboBox:hover {
                border: 1px solid #616161;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                background-color: #1e1e1e;
                border: 1px solid #333333;
                border-radius: 4px;
                selection-background-color: #333333;
                selection-color: #64b5f6;
            }

            /* Tree Widget */
            QTreeWidget {
                background-color: #1e1e1e;
                border: 1px solid #333333;
                border-radius: 6px;
                alternate-background-color: #2d2d2d;
            }
            QTreeWidget::item {
                padding: 4px;
                border-bottom: 1px solid #333333;
                color: #ffffff;
            }
            QTreeWidget::item:selected {
                background-color: #333333;
                color: #64b5f6;
            }
            QTreeWidget::item:hover {
                background-color: #424242;
            }
            QHeaderView::section {
                background-color: #2d2d2d;
                border: none;
                border-bottom: 1px solid #333333;
                padding: 8px;
                font-weight: bold;
                color: #ffffff;
            }

            /* Text Edit */
            QPlainTextEdit {
                background-color: #1e1e1e;
                border: 1px solid #333333;
                border-radius: 6px;
                padding: 8px;
                font-family: 'JetBrains Mono', 'Consolas', 'Monaco', monospace;
                font-size: 13px;
                color: #ffffff;
                selection-background-color: #333333;
            }
            QPlainTextEdit:focus {
                border: 2px solid #64b5f6;
            }

            /* Graphics View */
            QGraphicsView {
                background-color: #1e1e1e;
                border: 1px solid #333333;
                border-radius: 6px;
            }

            /* Scroll Bars */
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 16px;
                border-radius: 8px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background-color: #616161;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #757575;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """
        )

    def setup_central_widget(self) -> None:
        """Set up the central widget with modern layout"""
        central_widget = QWidget()
        self.window.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)

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
        """Set up modern toolbar with icons and better organization"""
        self.toolbar = self.window.addToolBar("Main Toolbar")
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)

        # File operations
        self.new_action = self.toolbar.addAction("New")
        self.open_action = self.toolbar.addAction("Open")
        self.save_action = self.toolbar.addAction("Save")
        self.toolbar.addSeparator()

        # Run/Debug operations
        self.run_action = self.toolbar.addAction("▶ Run")
        self.stop_action = self.toolbar.addAction("⏹ Stop")
        self.debug_action = self.toolbar.addAction("🐛 Debug")
        self.toolbar.addSeparator()

        # Language selector
        self.language_combo = QComboBox()
        self.language_combo.addItems(
            ["PILOT", "BASIC", "Logo", "Python", "JavaScript", "Perl"]
        )
        self.language_combo.setCurrentText("PILOT")
        self.language_combo.setMaximumWidth(120)
        self.language_combo.setMinimumWidth(100)
        self.toolbar.addWidget(QLabel("Language:"))
        self.toolbar.addWidget(self.language_combo)
        self.toolbar.addSeparator()

        # View options
        self.theme_action = self.toolbar.addAction("🌙 Theme")
        self.fullscreen_action = self.toolbar.addAction("⛶ Fullscreen")

        # Connect toolbar actions
        self.run_action.triggered.connect(lambda: self.run_program())
        self.stop_action.triggered.connect(lambda: self.stop_program())
        self.theme_action.triggered.connect(self.toggle_theme)
        self.fullscreen_action.triggered.connect(self.toggle_fullscreen)

    def setup_editor_panel(self) -> None:
        """Set up the editor panel with modern design"""
        editor_container = QWidget()
        editor_layout = QVBoxLayout(editor_container)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(8)

        # Editor header with controls
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)

        # File info
        self.file_label = QLabel("Untitled.tw")
        self.file_label.setStyleSheet("font-weight: bold; color: #666;")
        header_layout.addWidget(self.file_label)

        header_layout.addStretch()

        # Editor controls
        self.find_button = QPushButton("🔍 Find")
        self.find_button.setMaximumWidth(80)
        header_layout.addWidget(self.find_button)

        self.replace_button = QPushButton("🔄 Replace")
        self.replace_button.setMaximumWidth(90)
        header_layout.addWidget(self.replace_button)

        self.format_button = QPushButton("⚡ Format")
        self.format_button.setMaximumWidth(80)
        header_layout.addWidget(self.format_button)

        editor_layout.addWidget(header_widget)

        # Editor widget container
        self.editor_container = QWidget()
        editor_layout.addWidget(self.editor_container)

        self.main_splitter.addWidget(editor_container)

    def setup_right_panel(self) -> None:
        """Set up the right panel with modern tabs and better organization"""
        self.right_tabs = QTabWidget()
        self.right_tabs.setMovable(True)
        self.right_tabs.setTabsClosable(False)

        # Output tab with enhanced features
        self.output_tab = QWidget()
        output_layout = QVBoxLayout(self.output_tab)
        output_layout.setContentsMargins(8, 8, 8, 8)

        # Output controls
        output_controls = QHBoxLayout()
        self.clear_output_button = QPushButton("🗑 Clear")
        self.clear_output_button.setMaximumWidth(80)
        output_controls.addWidget(self.clear_output_button)

        output_controls.addStretch()

        self.output_filter_combo = QComboBox()
        self.output_filter_combo.addItems(["All", "Errors", "Warnings", "Info"])
        self.output_filter_combo.setMaximumWidth(100)
        output_controls.addWidget(QLabel("Filter:"))
        output_controls.addWidget(self.output_filter_combo)

        output_layout.addLayout(output_controls)

        # Output widget will be added here
        self.right_tabs.addTab(self.output_tab, "📄 Output")

        # Variables tab with search
        self.variables_tab = QWidget()
        variables_layout = QVBoxLayout(self.variables_tab)
        variables_layout.setContentsMargins(8, 8, 8, 8)

        # Variables controls
        var_controls = QHBoxLayout()
        self.var_search = QLineEdit()
        self.var_search.setPlaceholderText("Search variables...")
        self.var_search.setMaximumWidth(150)
        var_controls.addWidget(self.var_search)

        var_controls.addStretch()

        self.refresh_vars_button = QPushButton("🔄 Refresh")
        self.refresh_vars_button.setMaximumWidth(90)
        var_controls.addWidget(self.refresh_vars_button)

        variables_layout.addLayout(var_controls)

        # Variables widget will be added here
        self.right_tabs.addTab(self.variables_tab, "📊 Variables")

        # Graphics tab with controls
        self.graphics_tab = QWidget()
        graphics_layout = QVBoxLayout(self.graphics_tab)
        graphics_layout.setContentsMargins(8, 8, 8, 8)

        # Graphics controls
        graphics_controls = QHBoxLayout()
        self.clear_canvas_button = QPushButton("🗑 Clear")
        self.clear_canvas_button.setMaximumWidth(80)
        graphics_controls.addWidget(self.clear_canvas_button)

        graphics_controls.addStretch()

        self.save_canvas_button = QPushButton("💾 Save")
        self.save_canvas_button.setMaximumWidth(70)
        graphics_controls.addWidget(self.save_canvas_button)

        self.snapshot_button = QPushButton("📸 Snapshot")
        self.snapshot_button.setMaximumWidth(100)
        graphics_controls.addWidget(self.snapshot_button)

        graphics_layout.addLayout(graphics_controls)

        # Graphics widget will be added here
        self.right_tabs.addTab(self.graphics_tab, "🎨 Graphics")

        # Help tab with search
        self.help_tab = QWidget()
        help_layout = QVBoxLayout(self.help_tab)
        help_layout.setContentsMargins(8, 8, 8, 8)

        # Help controls
        help_controls = QHBoxLayout()
        self.help_search = QLineEdit()
        self.help_search.setPlaceholderText("Search help...")
        help_controls.addWidget(self.help_search)

        help_controls.addStretch()

        self.help_language_combo = QComboBox()
        self.help_language_combo.addItems(["All", "PILOT", "BASIC", "Logo"])
        self.help_language_combo.setMaximumWidth(100)
        help_controls.addWidget(QLabel("Language:"))
        help_controls.addWidget(self.help_language_combo)

        help_layout.addLayout(help_controls)

        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setPlainText(
            "Time Warp IDE Help\n\nSelect a language and start coding!"
        )
        help_layout.addWidget(help_text)
        self.right_tabs.addTab(self.help_tab, "❓ Help")

        # Plugins tab (if plugins are available)
        self.plugins_tab = QWidget()
        plugins_layout = QVBoxLayout(self.plugins_tab)
        plugins_layout.setContentsMargins(8, 8, 8, 8)

        plugins_label = QLabel("Plugin Manager - Coming Soon")
        plugins_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        plugins_layout.addWidget(plugins_label)

        self.right_tabs.addTab(self.plugins_tab, "🔌 Plugins")

        self.main_splitter.addWidget(self.right_tabs)

    def toggle_theme(self) -> None:
        """Toggle between light and dark themes"""
        self.dark_mode = not self.dark_mode
        self.setup_theme()
        theme_name = "Dark" if self.dark_mode else "Light"
        if self._status_bar:
            self._status_bar.set_text(f"Switched to {theme_name} theme")

    def toggle_fullscreen(self) -> None:
        """Toggle fullscreen mode"""
        if self.window.isFullScreen():
            self.window.showNormal()
            self.fullscreen_action.setText("⛶ Fullscreen")
        else:
            self.window.showFullScreen()
            self.fullscreen_action.setText("⛶ Windowed")

    def run_program(self) -> None:
        """Placeholder for run program functionality"""
        if self._status_bar:
            self._status_bar.set_text("Running program...")

    def stop_program(self) -> None:
        """Placeholder for stop program functionality"""
        if self._status_bar:
            self._status_bar.set_text("Program stopped")

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
        tree.setAlternatingRowColors(True)
        self.variables_tab.layout().addWidget(tree)
        return tree

    def create_splitter(self) -> Splitter:
        return QtSplitter()

    @property
    def window(self) -> QMainWindow:
        return self.window

    @property
    def run_button(self) -> QAction:
        return self.run_action

    @property
    def stop_button(self) -> QAction:
        return self.stop_action

    @property
    def language_combo(self) -> QComboBox:
        return self.language_combo

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
