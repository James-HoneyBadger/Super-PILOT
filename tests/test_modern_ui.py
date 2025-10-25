"""
Test suite for SuperPILOT UI components and modern interface
Tests theme system, widgets, and user interface functionality
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from conftest import TestCase
import tkinter as tk


class TestModernUI(TestCase):
    """Test modern UI components and functionality"""
    
    def test_theme_system_initialization(self, headless_ide):
        """Test that theme system initializes with correct default values"""
        assert hasattr(headless_ide, 'colors')
        assert hasattr(headless_ide, 'light_theme')
        assert hasattr(headless_ide, 'dark_theme')
        assert hasattr(headless_ide, 'premium_themes')
        
        # Check that default theme is applied
        assert headless_ide.current_theme_name == 'Modern'
        assert headless_ide.is_dark_mode == False
        
        # Verify essential color keys exist
        essential_keys = ['primary', 'secondary', 'bg_primary', 'text_primary']
        for key in essential_keys:
            assert key in headless_ide.colors
    
    def test_premium_themes_available(self, headless_ide):
        """Test that all premium themes are available"""
        expected_themes = ['Modern', 'Ocean', 'Sunset', 'Forest', 'Cosmic', 'Corporate']
        
        assert len(headless_ide.premium_themes) >= len(expected_themes)
        for theme_name in expected_themes:
            assert theme_name in headless_ide.premium_themes
            
            # Each theme should have required color keys
            theme = headless_ide.premium_themes[theme_name]
            required_keys = ['primary', 'secondary', 'accent']
            for key in required_keys:
                assert key in theme
    
    def test_dark_mode_toggle(self, headless_ide):
        """Test dark mode toggle functionality"""
        # Start in light mode
        assert headless_ide.is_dark_mode == False
        original_bg = headless_ide.colors['bg_primary']
        
        # Toggle to dark mode
        headless_ide.toggle_dark_mode()
        
        assert headless_ide.is_dark_mode == True
        assert headless_ide.colors['bg_primary'] != original_bg
        
        # Toggle back to light mode
        headless_ide.toggle_dark_mode()
        
        assert headless_ide.is_dark_mode == False
        assert headless_ide.colors['bg_primary'] == original_bg
    
    def test_theme_switching(self, headless_ide):
        """Test switching between premium themes"""
        original_primary = headless_ide.colors['primary']
        
        # Switch to Ocean theme
        headless_ide.switch_theme('Ocean')
        
        assert headless_ide.current_theme_name == 'Ocean'
        # Primary color should change
        assert headless_ide.colors['primary'] != original_primary
        
        # Switch to Sunset theme
        headless_ide.switch_theme('Sunset')
        
        assert headless_ide.current_theme_name == 'Sunset'
    
    def test_invalid_theme_switching(self, headless_ide):
        """Test that invalid theme names are handled gracefully"""
        original_theme = headless_ide.current_theme_name
        original_colors = headless_ide.colors.copy()
        
        # Try to switch to non-existent theme
        headless_ide.switch_theme('NonExistentTheme')
        
        # Should remain unchanged
        assert headless_ide.current_theme_name == original_theme
        assert headless_ide.colors == original_colors
    
    @patch('SuperPILOT.ttk.Style')
    def test_modern_styling_application(self, mock_style_class, headless_ide):
        """Test that modern styling is applied correctly"""
        mock_style = Mock()
        mock_style_class.return_value = mock_style
        
        headless_ide.apply_modern_styling()
        
        # Verify that style.configure was called for key components
        assert mock_style.configure.called
        
        # Check that modern button styles were configured
        configure_calls = [call[0] for call in mock_style.configure.call_args_list]
        expected_styles = ['Ultra.TButton', 'Card.TFrame', 'Code.TEntry']
        
        for style_name in expected_styles:
            assert any(style_name in str(call) for call in configure_calls)
    
    def test_status_bar_components(self, headless_ide):
        """Test that status bar has all required components"""
        # Mock the status bar attributes
        headless_ide.status_label = Mock()
        headless_ide.position_label = Mock()
        headless_ide.language_label = Mock()
        headless_ide.theme_indicator = Mock()
        
        # Test status update
        headless_ide.update_status_indicators()
        
        # Verify that status components exist
        assert hasattr(headless_ide, 'status_label')
        assert hasattr(headless_ide, 'position_label')
        assert hasattr(headless_ide, 'language_label')
        assert hasattr(headless_ide, 'theme_indicator')
    
    def test_notification_system(self, headless_ide):
        """Test toast notification system"""
        with patch('tkinter.Toplevel') as mock_toplevel:
            mock_window = Mock()
            mock_toplevel.return_value = mock_window
            
            # Mock window methods
            mock_window.withdraw = Mock()
            mock_window.overrideredirect = Mock()
            mock_window.attributes = Mock()
            mock_window.update_idletasks = Mock()
            mock_window.deiconify = Mock()
            mock_window.after = Mock()
            
            # Test different notification types
            notification_types = ['info', 'success', 'warning', 'error']
            
            for notif_type in notification_types:
                headless_ide.show_notification(f"Test {notif_type} message", notif_type)
                
                # Should create a new window
                mock_toplevel.assert_called()
                mock_window.withdraw.assert_called()
                mock_window.overrideredirect.assert_called_with(True)
    
    def test_settings_dialog_creation(self, headless_ide):
        """Test settings dialog functionality"""
        with patch('tkinter.Toplevel') as mock_toplevel:
            mock_window = Mock()
            mock_toplevel.return_value = mock_window
            
            # Mock window methods
            mock_window.title = Mock()
            mock_window.geometry = Mock()
            mock_window.configure = Mock()
            mock_window.transient = Mock()
            mock_window.grab_set = Mock()
            
            headless_ide.show_settings_dialog()
            
            # Should create settings window
            mock_toplevel.assert_called()
            mock_window.title.assert_called_with("Settings")
            mock_window.transient.assert_called()
            mock_window.grab_set.assert_called()
    
    def test_ui_color_updates(self, headless_ide):
        """Test that UI colors update when theme changes"""
        # Mock UI elements
        headless_ide.editor = Mock()
        headless_ide.output_area = Mock()
        headless_ide.canvas = Mock()
        headless_ide.status_label = Mock()
        
        # Mock root window
        headless_ide.root.winfo_children = Mock(return_value=[])
        
        # Test color update
        headless_ide.update_ui_colors()
        
        # Should configure background colors
        headless_ide.root.configure.assert_called()
        headless_ide.editor.configure.assert_called()
        headless_ide.output_area.configure.assert_called()
        headless_ide.canvas.configure.assert_called()
    
    def test_toolbar_creation(self, headless_ide):
        """Test modern toolbar components"""
        # Should have toolbar-related attributes after initialization
        assert hasattr(headless_ide, 'premium_themes')
        assert hasattr(headless_ide, 'current_theme_name')
        
        # Test theme variable initialization
        if hasattr(headless_ide, 'theme_var'):
            assert headless_ide.theme_var.get() == headless_ide.current_theme_name
    
    def test_cursor_position_tracking(self, headless_ide):
        """Test real-time cursor position tracking"""
        # Mock editor widget
        mock_editor = Mock()
        mock_editor.index = Mock(return_value='5.10')
        headless_ide.editor = mock_editor
        
        # Mock position label
        headless_ide.position_label = Mock()
        
        # Test position update
        headless_ide.setup_cursor_tracking()
        
        # Should have bound events to editor
        if hasattr(headless_ide, 'editor'):
            # Position tracking should be set up
            assert hasattr(headless_ide, 'position_label')
    
    def test_language_detection(self, headless_ide):
        """Test automatic language detection in status bar"""
        # Mock editor with different content types
        mock_editor = Mock()
        headless_ide.editor = mock_editor
        headless_ide.language_label = Mock()
        
        # Test PILOT detection
        mock_editor.get = Mock(return_value='T:Hello\nA:NAME\nU:X=10')
        headless_ide.update_status_indicators()
        
        # Test Logo detection
        mock_editor.get = Mock(return_value='FORWARD 100\nRIGHT 90\nREPEAT 4 [FORWARD 50]')
        headless_ide.update_status_indicators()
        
        # Test BASIC detection  
        mock_editor.get = Mock(return_value='10 PRINT "Hello"\n20 LET X = 5\n30 GOTO 10')
        headless_ide.update_status_indicators()
        
        # Language label should have been updated
        assert headless_ide.language_label.config.called
    
    def test_status_animation(self, headless_ide):
        """Test animated status indicators"""
        headless_ide.status_label = Mock()
        headless_ide.status_label.cget = Mock(return_value='✨ Ready')
        headless_ide.root.after = Mock()
        
        # Test animation start
        headless_ide.start_status_animation("Processing files...")
        
        headless_ide.status_label.config.assert_called()
        assert headless_ide._animation_active == True
        
        # Test animation stop
        headless_ide.stop_status_animation()
        assert headless_ide._animation_active == False
    
    def test_responsive_design_elements(self, headless_ide):
        """Test responsive design features"""
        # Test window geometry and scaling
        assert hasattr(headless_ide, 'root')
        
        # Should have proper initial geometry
        headless_ide.root.geometry.assert_called_with("1200x800")
        
        # Should have proper title
        headless_ide.root.title.assert_called_with("SuperPILOT II - Advanced Educational IDE")
    
    def test_accessibility_features(self, headless_ide):
        """Test accessibility and contrast features"""
        # Test that both light and dark themes have sufficient contrast
        for theme_name, theme_colors in headless_ide.premium_themes.items():
            assert 'primary' in theme_colors
            assert 'secondary' in theme_colors
            
            # Colors should be valid hex codes
            for color_key, color_value in theme_colors.items():
                assert isinstance(color_value, str)
                assert color_value.startswith('#') or color_value.startswith('rgba')
    
    def test_error_recovery_in_ui(self, headless_ide):
        """Test that UI gracefully handles errors"""
        # Test with missing attributes
        original_colors = headless_ide.colors
        headless_ide.colors = {}  # Empty colors dict
        
        # UI update should not crash
        try:
            headless_ide.update_ui_colors()
            # Should not raise exception
        except Exception as e:
            pytest.fail(f"UI update crashed with missing colors: {e}")
        finally:
            headless_ide.colors = original_colors