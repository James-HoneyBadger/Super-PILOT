"""
Audio playback system for SuperPILOT
Supports play/aplay for sound effects and music
"""


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
        import os

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
