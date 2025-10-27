"""
Runtime templecode animation system for SuperPILOT
Provides tweens, timers, and particle effects
"""

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
        val = self.start_val + (self.end_val - self.start_val) * k
        self.store[self.key] = val
        if self.elapsed >= self.duration:
            self.store[self.key] = self.end_val
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


# Runtime timing constants
MIN_DELTA_TIME_MS = 1
MAX_DELTA_TIME_MS = 100
