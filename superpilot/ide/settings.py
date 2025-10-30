"""
Settings management for TempleCode IDE
Provides JSON-based persistence of user preferences
"""

import json
import os
from pathlib import Path


class Settings:
    """Manages IDE settings with JSON persistence"""
    
    DEFAULT_SETTINGS = {
        "theme": "light",  # light or dark
        "font_family": "Consolas",
        "font_size": 13,
        "auto_save": False,
        "show_line_numbers": True,
        "syntax_highlighting": True,
        "tab_width": 4,
        "word_wrap": False,
        "recent_files": [],
        "max_recent_files": 10,
        "window_geometry": "1000x700",
    }
    
    def __init__(self, config_path=None):
        """Initialize settings manager
        
        Args:
            config_path: Path to settings file. 
                        Defaults to ~/.templecode/settings.json
        """
        if config_path is None:
            config_dir = Path.home() / ".templecode"
            config_dir.mkdir(exist_ok=True)
            config_path = config_dir / "settings.json"
        
        self.config_path = Path(config_path)
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.load()
    
    def load(self):
        """Load settings from JSON file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults (preserve new default keys)
                    self.settings.update(loaded)
        except Exception as e:
            print(f"Warning: Could not load settings: {e}")
    
    def save(self):
        """Save settings to JSON file"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save settings: {e}")
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value"""
        self.settings[key] = value
    
    def add_recent_file(self, filepath):
        """Add a file to recent files list"""
        recent = self.settings.get("recent_files", [])
        
        # Remove if already in list
        if filepath in recent:
            recent.remove(filepath)
        
        # Add to front
        recent.insert(0, filepath)
        
        # Limit size
        max_recent = self.settings.get("max_recent_files", 10)
        recent = recent[:max_recent]
        
        self.settings["recent_files"] = recent
        self.save()
    
    def get_recent_files(self):
        """Get list of recent files"""
        return self.settings.get("recent_files", [])
    
    def clear_recent_files(self):
        """Clear recent files list"""
        self.settings["recent_files"] = []
        self.save()
