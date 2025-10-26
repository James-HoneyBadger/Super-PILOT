"""
Abstract UI Interface for Time Warp IDE

This module defines the interface that all UI implementations must follow,
enabling support for multiple UI frameworks (tkinter, PyQt6, PySide6, etc.)
"""

from abc import ABC, abstractmethod
from typing import Any, Optional, Protocol


class UICallback(Protocol):
    """Protocol for UI callback functions"""

    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


class UIComponent(ABC):
    """Abstract base class for UI components"""

    @abstractmethod
    def show(self) -> None:
        """Show the component"""
        pass

    @abstractmethod
    def hide(self) -> None:
        """Hide the component"""
        pass

    @abstractmethod
    def destroy(self) -> None:
        """Destroy the component and free resources"""
        pass


class TextWidget(UIComponent):
    """Abstract text display/edit widget"""

    @abstractmethod
    def set_text(self, text: str) -> None:
        """Set the text content"""
        pass

    @abstractmethod
    def get_text(self) -> str:
        """Get the current text content"""
        pass

    @abstractmethod
    def append_text(self, text: str) -> None:
        """Append text to the current content"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all text"""
        pass

    @abstractmethod
    def set_readonly(self, readonly: bool) -> None:
        """Set readonly state"""
        pass

    @property
    def widget(self) -> Any:
        """Get underlying widget (optional for direct access)"""
        return None


class CanvasWidget(UIComponent):
    """Abstract canvas for graphics rendering"""

    @abstractmethod
    def clear(self) -> None:
        """Clear the canvas"""
        pass

    @abstractmethod
    def draw_line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: str = "black",
        width: int = 1,
    ) -> None:
        """Draw a line"""
        pass

    @abstractmethod
    def draw_circle(
        self, x: float, y: float, radius: float, color: str = "black", width: int = 1
    ) -> None:
        """Draw a circle"""
        pass

    @abstractmethod
    def draw_rectangle(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: str = "black",
        width: int = 1,
    ) -> None:
        """Draw a rectangle"""
        pass

    @abstractmethod
    def draw_text(self, x: float, y: float, text: str, color: str = "black") -> None:
        """Draw text"""
        pass


class MenuBar(UIComponent):
    """Abstract menu bar"""

    @abstractmethod
    def add_menu(self, name: str) -> "Menu":
        """Add a new menu and return it"""
        pass


class Menu(UIComponent):
    """Abstract menu"""

    @abstractmethod
    def add_command(
        self, label: str, command: UICallback, accelerator: Optional[str] = None
    ) -> None:
        """Add a menu command"""
        pass

    @abstractmethod
    def add_separator(self) -> None:
        """Add a separator"""
        pass

    @abstractmethod
    def add_submenu(self, label: str) -> "Menu":
        """Add a submenu and return it"""
        pass


class StatusBar(UIComponent):
    """Abstract status bar"""

    @abstractmethod
    def set_text(self, text: str) -> None:
        """Set status bar text"""
        pass


class MainWindow(UIComponent):
    """Abstract main application window"""

    def __init__(
        self, title: str = "Time Warp IDE", width: int = 1200, height: int = 800
    ):
        self.title = title
        self.width = width
        self.height = height
        self._menu_bar: Optional[MenuBar] = None
        self._status_bar: Optional[StatusBar] = None
        self._central_widget: Optional[UIComponent] = None

    @abstractmethod
    def set_title(self, title: str) -> None:
        """Set window title"""
        pass

    @abstractmethod
    def set_size(self, width: int, height: int) -> None:
        """Set window size"""
        pass

    @abstractmethod
    def center_on_screen(self) -> None:
        """Center window on screen"""
        pass

    @abstractmethod
    def create_menu_bar(self) -> MenuBar:
        """Create and return the menu bar"""
        pass

    @abstractmethod
    def create_status_bar(self) -> StatusBar:
        """Create and return the status bar"""
        pass

    @abstractmethod
    def create_text_editor(self) -> TextWidget:
        """Create a text editor widget"""
        pass

    @abstractmethod
    def create_output_panel(self) -> TextWidget:
        """Create an output text panel"""
        pass

    @abstractmethod
    def create_canvas(self, width: int = 400, height: int = 400) -> CanvasWidget:
        """Create a graphics canvas"""
        pass

    @abstractmethod
    def create_splitter(self) -> "Splitter":
        """Create a splitter widget for layout"""
        pass

    # Modern UI specific methods (optional implementations)
    def create_variables_tree(self) -> Any:
        """Create variables tree widget (optional for modern UI)"""
        return None

    @property
    def window(self) -> Any:
        """Get underlying window widget (optional for modern UI)"""
        return None

    @property
    def run_button(self) -> Any:
        """Get run button widget (optional for modern UI)"""
        return None

    @property
    def stop_button(self) -> Any:
        """Get stop button widget (optional for modern UI)"""
        return None

    @property
    def language_combo(self) -> Any:
        """Get language combo box widget (optional for modern UI)"""
        return None

    @property
    def menu_bar(self) -> MenuBar:
        """Get the menu bar, creating it if necessary"""
        if self._menu_bar is None:
            self._menu_bar = self.create_menu_bar()
        return self._menu_bar

    @property
    def status_bar(self) -> StatusBar:
        """Get the status bar, creating it if necessary"""
        if self._status_bar is None:
            self._status_bar = self.create_status_bar()
        return self._status_bar


class Splitter(UIComponent):
    """Abstract splitter for dividing UI areas"""

    @abstractmethod
    def add_widget(self, widget: UIComponent, stretch: int = 1) -> None:
        """Add a widget to the splitter"""
        pass

    @abstractmethod
    def set_orientation(self, horizontal: bool) -> None:
        """Set splitter orientation (horizontal=True for side-by-side)"""
        pass


class UIApplication(ABC):
    """Abstract UI application"""

    @abstractmethod
    def create_main_window(
        self, title: str = "Time Warp IDE", width: int = 1200, height: int = 800
    ) -> MainWindow:
        """Create the main application window"""
        pass

    @abstractmethod
    def run_event_loop(self) -> int:
        """Run the UI event loop and return exit code"""
        pass

    @abstractmethod
    def quit(self) -> None:
        """Quit the application"""
        pass

    @abstractmethod
    def process_events(self) -> None:
        """Process pending UI events (for non-blocking operations)"""
        pass

    @abstractmethod
    def schedule_callback(self, callback: UICallback, delay_ms: int = 0) -> None:
        """Schedule a callback to run (optionally after delay)"""
        pass


class UIFactory(ABC):
    """Factory for creating UI components"""

    @abstractmethod
    def create_application(self) -> UIApplication:
        """Create the UI application instance"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this UI framework is available"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the framework name"""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Get the framework version"""
        pass
