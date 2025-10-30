#!/usr/bin/env python3
# TempleCode v6 — Ultimate Edition (Consolidated)
# Includes: IDE with Debugger/Watch, Blocks preview, Classroom tab,
# Interpreter with Turtle graphics, Tween/Timers, Particles, Sprites/Tilemap/Image,
# Audio Mixer, SAVE/LOAD, and basic HUD.
#
# Arch deps: python, tk, (optional) sox (for 'play'), aplay
#
# Run IDE:
#   python3 templecode.py ide examples/ultimate_demo.pil

from __future__ import annotations
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
import argparse, re, math, sys, time, json, random, os, threading, queue, pathlib

# ---------------------- Parsing ----------------------
LABEL_RE = re.compile(r"^\s*\*(?P<label>[A-Za-z0-9_]+)\b")
CMD_RE = re.compile(r"\b(?P<token>[A-Za-z](?:[YN]|\([^)]*\))?)\s*:\s*(?P<rest>.*)$")
VAR_S_RE = re.compile(r"\$[A-Za-z_][A-Za-z0-9_]*")
VAR_N_RE = re.compile(r"\#[A-Za-z_][A-Za-z0-9_]*")


# ---------------------- Utilities ----------------------
def _has_exe(name: str) -> bool:
    for p in os.environ.get("PATH", "").split(os.pathsep):
        f = os.path.join(p, name)
        if os.path.isfile(f) and os.access(f, os.X_OK):
            return True
    return False


# ---------------------- Audio Mixer ----------------------
class Mixer:
    def __init__(self):
        self.registry = {}  # name -> path
        self.has_play = _has_exe("play")
        self.has_aplay = _has_exe("aplay")

    def snd(self, name, path, vol=0.8):
        self.registry[name] = path

    def play_snd(self, name):
        path = self.registry.get(name)
        if not path:
            return
        if self.has_play:
            os.system(f"play -q {path}")
            return
        if self.has_aplay and path.lower().endswith(".wav"):
            os.system(f"aplay -q {path}")
            return

        # Windows: use winsound for .wav files when available
        try:
            if os.name == "nt" and path.lower().endswith(".wav"):
                try:
                    import winsound

                    flags = winsound.SND_FILENAME | winsound.SND_ASYNC
                    winsound.PlaySound(path, flags)
                    return
                except Exception:
                    pass
        except Exception:
            pass

        # Fallback: system bell
        try:
            sys.stdout.write("\a")
            sys.stdout.flush()
        except Exception:
            pass


# ---------------------- Canvas / Turtle ----------------------
class TurtleCanvas:
    def __init__(self, canvas: tk.Canvas):
        self.cv = canvas
        self.w, self.h = 960, 600
        self.cx, self.cy = self.w / 2, self.h / 2
        self.x = 0.0
        self.y = 0.0
        self.hdg = 0.0
        self.color = "black"
        self.fill = "#cccccc"
        self.width = 2
        self.hud = False
        self._images_cache = {}
        self._sprites = {}
        self.cv.config(width=self.w, height=self.h, bg="white")
        self._axes()

    def _axes(self):
        self.cv.delete("axes")
        self.cv.create_line(0, self.cy, self.w, self.cy, fill="#eee", tags="axes")
        self.cv.create_line(self.cx, 0, self.cx, self.h, fill="#eee", tags="axes")

    def _to_screen(self, x, y):
        return (self.cx + x, self.cy - y)

    def _hud_draw(self):
        if not self.hud:
            return
        self.cv.delete("hud")
        self.cv.create_rectangle(
            6, 6, 240, 28, fill="#000", stipple="gray25", outline="", tags="hud"
        )
        self.cv.create_text(
            12,
            8,
            anchor="nw",
            text=f"HUD pos=({int(self.x)},{int(self.y)}) hdg={int(self.hdg)}",
            fill="#fff",
            tags="hud",
        )

    def op(self, name, *args):
        if name == "init":
            w, h = args
            self.w = int(w)
            self.h = int(h)
            self.cx, self.cy = self.w / 2, self.h / 2
            self.cv.config(width=self.w, height=self.h)
            self.cv.delete("all")
            self._axes()
        elif name == "state":
            self.x = 0
            self.y = 0
            self.hdg = 0
            self.color = "black"
            self.fill = "#ccc"
            self.width = 2
            self.cv.delete("all")
            self._axes()
        elif name == "clear":
            self.cv.delete("all")
            self._axes()
        elif name == "setpos":
            x, y = args
            self.x = float(x)
            self.y = float(y)
        elif name == "color":
            (c,) = args
            self.color = str(c)
        elif name == "fillcolor":
            (c,) = args
            self.fill = str(c)
        elif name == "width":
            (w,) = args
            self.width = max(1, int(float(w)))
        elif name == "speed":
            pass
        elif name == "left":
            (deg,) = args
            self.hdg = (self.hdg + float(deg)) % 360.0
        elif name == "right":
            (deg,) = args
            self.hdg = (self.hdg - float(deg)) % 360.0
        elif name == "forward":
            (dist,) = args
            nx = self.x + math.cos(math.radians(self.hdg)) * float(dist)
            ny = self.y + math.sin(math.radians(self.hdg)) * float(dist)
            x1, y1 = self._to_screen(self.x, self.y)
            x2, y2 = self._to_screen(nx, ny)
            self.cv.create_line(
                x1, y1, x2, y2, fill=self.color, width=self.width, capstyle=tk.ROUND
            )
            self.x, self.y = nx, ny
        elif name == "rect":
            w, h = args
            x1, y1 = self._to_screen(self.x, self.y)
            x2, y2 = self._to_screen(self.x + float(w), self.y + float(h))
            self.cv.create_rectangle(
                x1, y1, x2, y2, outline=self.color, width=self.width
            )
        elif name == "circle":
            r, extent = args if len(args) == 2 else (args[0], 360.0)
            steps = max(8, int(abs(extent) / 6))
            step = extent / steps
            for _ in range(steps):
                nx = self.x + math.cos(math.radians(self.hdg)) * (
                    2 * math.pi * r / 360.0 * step
                )
                ny = self.y + math.sin(math.radians(self.hdg)) * (
                    2 * math.pi * r / 360.0 * step
                )
                x1, y1 = self._to_screen(self.x, self.y)
                x2, y2 = self._to_screen(nx, ny)
                self.cv.create_line(
                    x1, y1, x2, y2, fill=self.color, width=self.width, capstyle=tk.ROUND
                )
                self.x, self.y = nx, ny
                self.hdg = (self.hdg + step) % 360.0
        elif name == "text":
            (s,) = args
            sx, sy = self._to_screen(self.x, self.y)
            self.cv.create_text(sx, sy, text=str(s), fill=self.color, anchor="nw")
        elif name == "dot":
            (r,) = args
            x1, y1 = self._to_screen(self.x - r, self.y + r)
            x2, y2 = self._to_screen(self.x + r, self.y - r)
            self.cv.create_oval(x1, y1, x2, y2, fill=self.color, outline="")
        elif name == "image":
            path = args[0]
            w = int(args[1]) if len(args) > 1 and args[1] else None
            h = int(args[2]) if len(args) > 2 and args[2] else None
            key = (path, w or 0, h or 0)
            try:
                img = self._images_cache.get(key)
                if img is None:
                    img = tk.PhotoImage(file=path)
                    if w and h:
                        sx = max(1, round(img.width() / w))
                        sy = max(1, round(img.height() / h))
                        img = img.subsample(sx, sy)
                    self._images_cache[key] = img
                sx, sy = self._to_screen(self.x, self.y)
                self.cv.create_image(sx, sy, image=img, anchor="nw")
                if not hasattr(self.cv, "_keep"):
                    self.cv._keep = []
                self.cv._keep.append(img)
            except Exception:
                self.cv.create_text(
                    *self._to_screen(self.x, self.y),
                    text=f"[missing {path}]",
                    fill="red",
                    anchor="nw",
                )
        elif name == "sprite_new":
            name, path = args
            self._sprites[str(name)] = {"path": path, "x": 0.0, "y": 0.0}
        elif name == "sprite_pos":
            name, x, y = args
            s = self._sprites.get(str(name))
            if s:
                s["x"] = float(x)
                s["y"] = float(y)
        elif name == "sprite_draw":
            name = args[0]
            s = self._sprites.get(str(name))
            if s:
                self.op("setpos", s["x"], s["y"])
                self.op("image", s["path"], None, None)
        elif name == "tilemap_txt":
            path, size = args
            size = int(size)
            try:
                rows = open(path, "r", encoding="utf-8").read().splitlines()
            except Exception:
                rows = []
            for r, row in enumerate(rows):
                for c, ch in enumerate(row):
                    if ch.strip() == "" or ch == ".":
                        continue
                    x = -self.w / 2 + c * size
                    y = self.h / 2 - (r + 1) * size
                    x1, y1 = self._to_screen(x, y)
                    x2, y2 = self._to_screen(x + size, y + size)
                    color = "#3a6" if ch == "@" else ("#444" if ch == "#" else "#aaa")
                    self.cv.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
        elif name == "hud":
            self.hud = not self.hud
        elif name == "snapshot":
            out = args[0]
            try:
                self.cv.postscript(file=out, colormode="color")
            except Exception:
                pass
        self._hud_draw()
        self.cv.update_idletasks()
        self.cv.update()


# ---------------------- Tween/Timers/Particles ----------------------
EASE = {
    "linear": lambda t: t,
    "quadOut": lambda t: 1 - (1 - t) * (1 - t),
    "quadIn": lambda t: t * t,
    "smooth": lambda t: t * t * (3 - 2 * t),
}


class Tween:
    def __init__(
        self,
        store: dict,
        key: str,
        a: float,
        b: float,
        dur_ms: int,
        ease: str = "linear",
    ):
        self.store = store
        self.key = key
        self.a = float(a)
        self.b = float(b)
        self.dur = max(1, int(dur_ms))
        self.t = 0
        self.ease = EASE.get(ease, EASE["linear"])
        self.done = False

    def step(self, dt):
        if self.done:
            return
        self.t += dt
        u = min(1.0, self.t / self.dur)
        k = self.ease(u)
        self.store[self.key] = self.a + (self.b - self.a) * k
        if self.t >= self.dur:
            self.store[self.key] = self.b
            self.done = True


class Timer:
    def __init__(self, delay_ms: int, label: str):
        self.delay = max(0, int(delay_ms))
        self.label = label


class Particle:
    def __init__(self, x, y, vx, vy, life_ms, color="#ffaa33", size=3):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life_ms
        self.color = color
        self.size = size

    def step(self, dt):
        self.x += self.vx * (dt / 1000.0)
        self.y += self.vy * (dt / 1000.0)
        self.vy -= 30 * (dt / 1000.0)
        self.life -= dt


# ---------------------- Interpreter Engine ----------------------
class Engine:
    def __init__(
        self,
        text: str,
        sink,
        mixer: Mixer,
        step_hook=None,
        var_hook=None,
        stop_event=None,
    ):
        self.lines = []
        self.labels = {}
        self.pc = 0
        self.sink = sink
        self.mixer = mixer
        self.step_hook = step_hook or (lambda idx, cmd, arg: None)
        self.var_hook = var_hook or (lambda s, n: None)
        self.stop_event = stop_event
        # variables
        self.vars_s = {}
        self.vars_n = {"#x": 0.0, "#y": 0.0, "#i": 0.0}
        # systems
        self.tweens: list[Tween] = []
        self.timers: list[Timer] = []
        self.particles: list[Particle] = []
        # parse
        for i, raw in enumerate(text.splitlines()):
            s = raw.rstrip("\n")
            label = None
            m = LABEL_RE.match(s)
            if m:
                label = m.group("label").upper()
                s = s[m.end() :].lstrip()
            token = cmd = None
            arg = ""
            mm = CMD_RE.search(s)
            if mm:
                token = mm.group("token")
                arg = mm.group("rest").strip()
                # flags/expr on token handled minimally: J(cond) only
                cmd = token[0].upper()
                cond_expr = None
                if "(" in token and token.endswith(")") and cmd == "J":
                    cond_expr = token[token.find("(") + 1 : -1].strip()
                self.lines.append((cmd, arg, i, cond_expr))
            else:
                self.lines.append((None, "", i, None))
            if label is not None:
                self.labels[label] = len(self.lines) - 1
        self.last_ms = None

    # ---- helpers
    def _eval_num(self, expr: str) -> float:
        def repl(m):
            return str(self.vars_n.get(m.group(0), 0.0))

        expr = VAR_N_RE.sub(repl, expr)
        try:
            return float(
                eval(
                    expr,
                    {"__builtins__": {}},
                    {"abs": abs, "min": min, "max": max, "round": round, "math": math},
                )
            )
        except Exception as e:
            raise RuntimeError(f"Bad numeric expression: {expr}\n{e}")

    def _eval_str(self, expr: str) -> str:
        def rep_s(m):
            return repr(self.vars_s.get(m.group(0)[1:], ""))

        def rep_n(m):
            v = self.vars_n.get(m.group(0), 0.0)
            return repr(str(int(v)) if float(v).is_integer() else str(v))

        expr = VAR_S_RE.sub(rep_s, expr)
        expr = VAR_N_RE.sub(rep_n, expr)
        try:
            v = eval(expr, {"__builtins__": {}}, {})
        except Exception as e:
            raise RuntimeError(f"Bad string expression: {expr}\n{e}")
        if not isinstance(v, str):
            raise RuntimeError("String expression must evaluate to text")
        return v

    def _jump(self, label_token: str):
        name = label_token[1:].upper()
        if name not in self.labels:
            raise RuntimeError(f"Unknown label {label_token}")
        self.pc = self.labels[name]

    # ---- systems
    def _update_systems(self, dt):
        for t in list(self.tweens):
            t.step(dt)
            if t.done:
                self.tweens.remove(t)
        for tm in list(self.timers):
            tm.delay -= dt
            if tm.delay <= 0:
                self._jump(tm.label)
                self.timers.remove(tm)
                break
        for p in list(self.particles):
            p.step(dt)
            if p.life <= 0:
                self.particles.remove(p)

    def _draw_particles(self):
        for p in list(self.particles):
            self.sink(("setpos", (p.x, p.y)))
            self.sink(("color", (p.color,)))
            self.sink(("dot", (p.size,)))

    # ---- main run
    def run(self):
        self.pc = 0
        self.last_ms = int(time.time() * 1000)
        steps = 0
        max_steps = 1_000_000
        while self.pc < len(self.lines):
            if self.stop_event and self.stop_event.is_set():
                raise RuntimeError("Stopped")
            now = int(time.time() * 1000)
            dt = max(1, now - self.last_ms)
            self.last_ms = now
            self._update_systems(dt)

            cmd, arg, ln, cond = self.lines[self.pc]
            self.step_hook(self.pc, cmd, arg)
            self.pc += 1
            steps += 1
            if steps > max_steps:
                raise RuntimeError("Step limit exceeded (infinite loop?)")
            if not cmd:
                continue

            # conditional J(cond): *LABEL
            if cmd == "J" and cond:
                try:
                    ok = self._eval_num(cond) != 0
                except Exception as e:
                    raise RuntimeError(f"Bad J(condition) at line {ln+1}: {e}")
                if not ok:
                    continue

            # Graphics
            if cmd == "G":
                parts = [p.strip() for p in (arg or "").split(",") if p.strip()]
                if len(parts) == 2:
                    self.sink(
                        (
                            "init",
                            (
                                int(self._eval_num(parts[0])),
                                int(self._eval_num(parts[1])),
                            ),
                        )
                    )
                else:
                    self.sink(("init", (960, 600)))
                self.sink(("state", ()))
                continue
            if cmd == "Z":
                self.sink(("clear", ()))
                continue
            if cmd == "V":
                time.sleep(max(0.0, float(self._eval_num(arg or "0")) / 1000.0))
                continue
            if cmd == "S":
                x, y = [self._eval_num(v.strip()) for v in arg.split(",")]
                self.vars_n["#x"] = x
                self.vars_n["#y"] = y
                self.sink(("setpos", (x, y)))
                continue
            if cmd == "K":
                c = arg.strip()
                if c and (c[0] in ('"', "'")):
                    c = self._eval_str(c)
                self.sink(("color", (c,)))
                continue
            if cmd == "Y":
                c = arg.strip()
                if c and (c[0] in ('"', "'")):
                    c = self._eval_str(c)
                self.sink(("fillcolor", (c,)))
                continue
            if cmd == "W":
                self.sink(("width", (self._eval_num(arg or "1"),)))
                continue
            if cmd == "F":
                self.sink(("forward", (self._eval_num(arg or "0"),)))
                continue
            if cmd == "L":
                self.sink(("left", (self._eval_num(arg or "0"),)))
                continue
            if cmd == "Q":
                self.sink(("right", (self._eval_num(arg or "0"),)))
                continue
            if cmd == "D":
                w, h = [self._eval_num(v.strip()) for v in arg.split(",")]
                self.sink(("rect", (w, h)))
                continue
            if cmd == "O":
                parts = [p.strip() for p in arg.split(",") if p.strip()]
                r = self._eval_num(parts[0]) if parts else 10.0
                ex = self._eval_num(parts[1]) if len(parts) > 1 else 360.0
                self.sink(("circle", (r, ex)))
                continue
            if cmd == "X":
                s = arg.strip()
                if not s:
                    s = '""'
                self.sink(("text", (self._eval_str(s),)))
                continue
            if cmd == "I":
                parts = [p.strip() for p in arg.split(",") if p.strip()]
                if not parts:
                    continue
                path = parts[0]
                if path[0] in ('"', "'"):
                    path = self._eval_str(path)
                w = self._eval_num(parts[1]) if len(parts) > 1 else None
                h = self._eval_num(parts[2]) if len(parts) > 2 else None
                self.sink(("image", (path, w, h)))
                continue

            # Core flow / vars
            if cmd == "C":
                # Assignments: $s = "text", #n = expr
                if "=" in arg:
                    lhs, rhs = arg.split("=", 1)
                    lhs = lhs.strip()
                    rhs = rhs.strip()
                    if lhs.startswith("$"):
                        self.vars_s[lhs[1:]] = self._eval_str(rhs)
                    else:
                        name = lhs if lhs.startswith("#") else "#" + lhs
                        self.vars_n[name] = self._eval_num(rhs)
                else:
                    # bare expression to #J
                    self.vars_n["#J"] = self._eval_num(arg)
                continue
            if cmd == "T":
                print(self._interpolate(arg))
                continue
            if cmd == "A":
                # A: $name ? prompt   or   A: #age ? prompt
                target = arg
                prompt = ""
                if " ? " in arg:
                    target, prompt = arg.split(" ? ", 1)
                    sys.stdout.write(prompt)
                    sys.stdout.flush()
                target = target.strip()
                try:
                    line = input()
                except EOFError:
                    line = ""
                if target.startswith("$"):
                    self.vars_s[target[1:]] = line
                elif target.startswith("#"):
                    try:
                        self.vars_n[target] = float(line)
                    except:
                        self.vars_n[target] = 0.0
                continue
            if cmd == "J":
                label = arg.strip()
                if label.startswith("*"):
                    self._jump(label)
                    continue
                else:
                    continue
            if cmd == "E":
                break

            # Runtime R:
            if cmd == "R":
                u = arg.strip().upper()
                if u.startswith("HUD"):
                    self.sink(("hud", ()))
                elif u.startswith("SNAP "):
                    path = arg[5:].strip()
                    if path and path[0] in ('"', "'"):
                        path = self._eval_str(path)
                    self.sink(("snapshot", (path,)))
                elif u.startswith("TWEEN"):
                    m = re.search(
                        r"(#[A-Za-z0-9_]+)\s*->\s*([\-0-9\.]+)\s*IN\s*([0-9]+)\s*ms(?:\s*EASE\s*\"?([A-Za-z0-9]+)\"?)?",
                        arg,
                        re.IGNORECASE,
                    )
                    if m:
                        key = m.group(1)
                        end = float(m.group(2))
                        dur = int(m.group(3))
                        ease = m.group(4) or "linear"
                        start = float(self.vars_n.get(key, 0.0))
                        self.vars_n[key] = start
                        self.tweens.append(
                            Tween(self.vars_n, key, start, end, dur, ease)
                        )
                elif u.startswith("AFTER"):
                    m = re.search(
                        r"AFTER\s*([0-9]+)\s*DO\s*(\*[A-Za-z0-9_]+)", arg, re.IGNORECASE
                    )
                    if m:
                        self.timers.append(
                            Timer(int(m.group(1)), m.group(2)[1:].upper())
                        )
                elif u.startswith("EMIT"):
                    parts = [p.strip() for p in arg.split(",")]
                    # R: EMIT "spark", x,y, n, life, spread
                    try:
                        kind = parts[0].strip('"')
                        x = float(self._eval_num(parts[1]))
                        y = float(self._eval_num(parts[2]))
                        n = int(self._eval_num(parts[3]))
                        life = int(self._eval_num(parts[4]))
                        spread = float(self._eval_num(parts[5]))
                    except Exception:
                        kind = "spark"
                        x = self.vars_n.get("#x", 0)
                        y = self.vars_n.get("#y", 0)
                        n = 20
                        life = 800
                        spread = 60
                    for _ in range(int(n)):
                        ang = random.uniform(0, 2 * math.pi)
                        spd = random.uniform(10, spread)
                        self.particles.append(
                            Particle(
                                x, y, math.cos(ang) * spd, math.sin(ang) * spd, life
                            )
                        )
                elif u.startswith("NEW "):
                    parts = [p.strip() for p in arg[4:].split(",")]
                    name = parts[0]
                    path = parts[1].strip('"')
                    self.sink(("sprite_new", (name, path)))
                elif u.startswith("POS "):
                    parts = [p.strip() for p in arg[4:].split(",")]
                    name = parts[0]
                    x = self._eval_num(parts[1])
                    y = self._eval_num(parts[2])
                    self.vars_n["#x"] = x
                    self.vars_n["#y"] = y
                    self.sink(("sprite_pos", (name, x, y)))
                elif u.startswith("DRAW "):
                    name = arg[5:].strip()
                    self.sink(("sprite_draw", (name,)))
                elif u.startswith("TILEMAPTXT "):
                    parts = [p.strip() for p in arg[10:].split(",")]
                    path = parts[0].strip('"')
                    size = int(self._eval_num(parts[1]))
                    self.sink(("tilemap_txt", (path, size)))
                elif u.startswith("SND "):
                    m = re.search(
                        r'name\s*=\s*"([^"]+)"\s*,\s*file\s*=\s*"([^"]+)"',
                        arg,
                        re.IGNORECASE,
                    )
                    if m:
                        self.mixer.snd(m.group(1), m.group(2))
                elif u.startswith("PLAY "):
                    m = re.search(r"\"([^\"]+)\"", arg)
                    nm = m.group(1) if m else arg.split()[-1].strip().strip('"')
                    self.mixer.play_snd(nm)
                elif u.startswith("SAVE "):
                    slot = arg[5:].strip().strip('"')
                    data = {"$": self.vars_s, "#": self.vars_n}
                    path = os.path.expanduser(f"~/.templecode_saves/{slot}.json")
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    open(path, "w", encoding="utf-8").write(json.dumps(data))
                elif u.startswith("LOAD "):
                    slot = arg[5:].strip().strip('"')
                    path = os.path.expanduser(f"~/.templecode_saves/{slot}.json")
                    if os.path.exists(path):
                        data = json.loads(open(path, "r", encoding="utf-8").read())
                        self.vars_s.update(data.get("$", {}))
                        self.vars_n.update(data.get("#", {}))
                continue

            # draw particles each frame end
            self._draw_particles()
            # publish watch
            self.var_hook(dict(self.vars_s), dict(self.vars_n))

    def _interpolate(self, textline: str) -> str:
        def rep_s(m):
            return self.vars_s.get(m.group(0)[1:], "")

        def rep_n(m):
            v = self.vars_n.get(m.group(0), 0.0)
            return str(int(v)) if float(v).is_integer() else str(v)

        s = VAR_S_RE.sub(lambda m: rep_s(m), textline)
        s = VAR_N_RE.sub(lambda m: rep_n(m), s)
        return s


# ---------------------- IDE (Debugger, Watch, Blocks, Classroom) ----------------------
class IDE(tk.Tk):
    def __init__(self, initial_path: str | None):
        super().__init__()
        self.title("TempleCode v6 — Ultimate Edition")
        self.geometry("1300x850")
        self.stop_event = threading.Event()
        self.mixer = Mixer()
        self._build_ui()
        if initial_path and os.path.exists(initial_path):
            try:
                self.editor.insert(
                    "1.0", open(initial_path, "r", encoding="utf-8").read()
                )
            except:
                pass
        self._refresh_gutter()
        self._update_blocks()

    def _build_ui(self):
        # Menus
        men = tk.Menu(self)
        self.config(menu=men)
        filem = tk.Menu(men, tearoff=0)
        filem.add_command(label="Open…", command=self.open_file)
        filem.add_command(label="Save As…", command=self.save_as)
        men.add_cascade(label="File", menu=filem)
        runm = tk.Menu(men, tearoff=0)
        runm.add_command(label="Run (F5)", command=self.run_prog)
        runm.add_command(label="Stop (Shift+F5)", command=self.stop_prog)
        runm.add_separator()
        runm.add_command(label="Toggle HUD (F9)", command=lambda: self.tc.op("hud"))
        men.add_cascade(label="Run", menu=runm)

        # Toolbar
        tb = tk.Frame(self)
        tb.pack(fill="x")
        self.btn_run = tk.Button(tb, text="▶ Run", command=self.run_prog)
        self.btn_run.pack(side="left")
        self.btn_pause = tk.Button(tb, text="⏸ Pause", command=self.toggle_pause)
        self.btn_pause.pack(side="left", padx=4)
        self.btn_step = tk.Button(tb, text="⤼ Step", command=self.step)
        self.btn_step.pack(side="left", padx=4)
        self.btn_cont = tk.Button(tb, text="⏵ Continue", command=self.cont)
        self.btn_cont.pack(side="left", padx=4)
        self.btn_stop = tk.Button(tb, text="■ Stop", command=self.stop_prog)
        self.btn_stop.pack(side="left", padx=4)

        # Main split
        main = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        main.pack(fill="both", expand=True)

        # Left: Editor + gutter + console
        left = tk.PanedWindow(main, orient=tk.VERTICAL)
        main.add(left, stretch="always")
        edwrap = tk.PanedWindow(left, orient=tk.HORIZONTAL)
        left.add(edwrap, stretch="always")
        self.gutter = tk.Text(
            edwrap, width=4, padx=4, state=tk.DISABLED, background="#f5f5f5"
        )
        self.editor = tk.Text(edwrap, undo=True, wrap=tk.NONE)
        edwrap.add(self.gutter)
        edwrap.add(self.editor, stretch="always")
        self.editor.bind(
            "<KeyRelease>", lambda e: (self._refresh_gutter(), self._update_blocks())
        )
        self.gutter.bind("<Button-1>", self._toggle_breakpoint)
        # Console (output only)
        self.console = tk.Text(left, height=8, state=tk.DISABLED)
        left.add(self.console, height=180)

        # Right: Tabs for Canvas, Watch/Breakpoints, Blocks, Classroom
        right = ttk.Notebook(main)
        main.add(right, width=520)

        # Canvas tab
        can_frame = ttk.Frame(right)
        right.add(can_frame, text="Canvas")
        self.canvas = tk.Canvas(can_frame, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.tc = TurtleCanvas(self.canvas)

        # Debug tab
        dbg = ttk.Frame(right)
        right.add(dbg, text="Debugger")
        self.watch_s = tk.Text(dbg, width=30, height=10)
        self.watch_s.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        self.watch_n = tk.Text(dbg, width=30, height=10)
        self.watch_n.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        self.breaks = set()
        self.paused = tk.BooleanVar(value=False)
        self.step_once = False

        # Blocks tab
        blk = ttk.Frame(right)
        right.add(blk, text="Blocks")
        self.blocks_canvas = tk.Canvas(blk, bg="#fdfdfd")
        self.blocks_canvas.pack(fill="both", expand=True)

        # Classroom tab
        cls = ttk.Frame(right)
        right.add(cls, text="Classroom")
        top = tk.Frame(cls)
        top.pack(fill="x")
        tk.Button(top, text="Load .tpack", command=self._load_tpack).pack(side="left")
        self.cls_title = tk.Label(top, text="No pack loaded")
        self.cls_title.pack(side="left", padx=8)
        mid = tk.PanedWindow(cls, orient=tk.HORIZONTAL)
        mid.pack(fill="both", expand=True)
        self.cls_list = tk.Listbox(mid, width=24)
        mid.add(self.cls_list)
        self.cls_desc = tk.Text(mid)
        mid.add(self.cls_desc, stretch="always")
        self.cls_list.bind("<<ListboxSelect>>", self._cls_show)

        # keys
        self.bind("<F5>", lambda e: self.run_prog())
        self.bind("<Shift-F5>", lambda e: self.stop_prog())
        self.bind("<F9>", lambda e: (self.tc.op("hud"), "break"))

    # --- File ops
    def open_file(self):
        p = filedialog.askopenfilename(
            filetypes=[("TempleCode", "*.pil"), ("All", "*.*")]
        )
        if not p:
            return
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", open(p, "r", encoding="utf-8").read())
        self._refresh_gutter()
        self._update_blocks()

    def save_as(self):
        p = filedialog.asksaveasfilename(
            defaultextension=".pil", filetypes=[("TempleCode", "*.pil")]
        )
        if not p:
            return
        open(p, "w", encoding="utf-8").write(self.editor.get("1.0", "end-1c"))

    # --- Gutter & Blocks
    def _refresh_gutter(self):
        self.gutter.config(state=tk.NORMAL)
        self.gutter.delete("1.0", "end")
        lines = int(self.editor.index("end-1c").split(".")[0])
        for i in range(1, lines + 1):
            mark = "●" if (i - 1) in self.breaks else " "
            self.gutter.insert("end", f"{mark}{i}\n")
        self.gutter.config(state=tk.DISABLED)

    def _toggle_breakpoint(self, event):
        index = self.gutter.index(f"@{event.x},{event.y}")
        line = int(index.split(".")[0]) - 1
        if line in self.breaks:
            self.breaks.remove(line)
        else:
            self.breaks.add(line)
        self._refresh_gutter()

    def _update_blocks(self):
        COLORS = {
            "G": "#6DCCFF",
            "S": "#B6FF6D",
            "F": "#FFD36D",
            "L": "#FF8B6D",
            "Q": "#FF6DB1",
            "D": "#B67DFF",
            "O": "#6DFFEA",
            "X": "#C7C7C7",
            "R": "#FFEA6D",
            "T": "#E6A5FF",
            "I": "#FFC6A5",
            "K": "#A5C9FF",
            "Y": "#FFD6E5",
            "W": "#D1FFD1",
        }
        c = self.blocks_canvas
        c.delete("all")
        y = 10
        for ln in self.editor.get("1.0", "end-1c").splitlines():
            m = CMD_RE.search(ln)
            if not m:
                continue
            t = m.group("token")[0].upper()
            arg = m.group("rest").strip()
            color = COLORS.get(t, "#ddd")
            c.create_rectangle(12, y, 12 + 360, y + 26, fill=color, width=0)
            c.create_text(
                20, y + 6, anchor="nw", text=f"{t}: {arg}", font=("TkDefaultFont", 10)
            )
            y += 32

    # --- Classroom
    def _load_tpack(self):
        p = filedialog.askopenfilename(
            filetypes=[("TemplePack", "*.tpack"), ("JSON", "*.json")]
        )
        if not p:
            return
        try:
            data = json.loads(open(p, "r", encoding="utf-8").read())
        except Exception as e:
            messagebox.showerror("TempleCode", f"Failed to load: {e}")
            return
        self.cls_data = data
        self.cls_list.delete(0, "end")
        for s in data.get("steps", []):
            self.cls_list.insert("end", s.get("title", "(untitled)"))
        self.cls_title.config(text=data.get("title", os.path.basename(p)))
        self.cls_desc.delete("1.0", "end")
        self.cls_desc.insert("1.0", "Select a step on the left.")

    def _cls_show(self, e):
        i = self.cls_list.curselection()
        if not i:
            return
        step = self.cls_data["steps"][i[0]]
        self.cls_desc.delete("1.0", "end")
        self.cls_desc.insert("1.0", step.get("description", ""))

    # --- Debug controls
    def toggle_pause(self):
        self.paused.set(not self.paused.get())

    def step(self):
        self.step_once = True
        self.paused.set(False)

    def cont(self):
        self.paused.set(False)
        self.step_once = False

    # --- Run/Stop
    def run_prog(self):
        if hasattr(self, "runner") and self.runner.is_alive():
            return
        self.console.config(state=tk.NORMAL)
        self.console.delete("1.0", "end")
        self.console.config(state=tk.DISABLED)
        self.canvas.delete("all")
        self.tc._axes()
        self.stop_event.clear()
        program = self.editor.get("1.0", "end-1c")

        def sink(op):
            name, args = op
            self.tc.op(name, *args)

        def step_hook(idx, cmd, arg):
            # Breakpoints & pause
            if idx in self.breaks or self.paused.get():
                self.paused.set(True)
                while self.paused.get() and not self.step_once:
                    if self.stop_event.is_set():
                        return
                    time.sleep(0.02)
                self.step_once = False

        def var_hook(svars, nvars):
            self.watch_s.delete("1.0", "end")
            [
                self.watch_s.insert("end", f"${k}: {v}\n")
                for k, v in sorted(svars.items())
            ]
            self.watch_n.delete("1.0", "end")
            [
                self.watch_n.insert("end", f"{k}: {v}\n")
                for k, v in sorted(nvars.items())
            ]

        eng = Engine(
            program,
            sink,
            self.mixer,
            step_hook=step_hook,
            var_hook=var_hook,
            stop_event=self.stop_event,
        )

        def worker():
            try:
                eng.run()
            except Exception as e:
                self._console(f"ERROR: {e}\n")

        self.runner = threading.Thread(target=worker, daemon=True)
        self.runner.start()

    def stop_prog(self):
        if hasattr(self, "runner") and self.runner.is_alive():
            self.stop_event.set()

    def _console(self, s: str):
        self.console.config(state=tk.NORMAL)
        self.console.insert("end", s)
        self.console.see("end")
        self.console.config(state=tk.DISABLED)


# ---------------------- CLI ----------------------
def run_file(path: str):
    text = open(path, "r", encoding="utf-8").read()
    root = tk.Tk()
    root.title("TempleCode v6 — Ultimate")
    cv = tk.Canvas(root, bg="white", width=960, height=600)
    cv.pack(fill="both", expand=True)
    tc = TurtleCanvas(cv)
    mix = Mixer()

    def sink(op):
        name, args = op
        tc.op(name, *args)

    Engine(text, sink, mix).run()
    root.mainloop()


def main():
    ap = argparse.ArgumentParser(
        description="TempleCode v6 — Ultimate Edition (single-file)"
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_run = sub.add_parser("run")
    p_run.add_argument("path")
    p_ide = sub.add_parser("ide")
    p_ide.add_argument("path", nargs="?")
    a = ap.parse_args()
    if a.cmd == "run":
        run_file(a.path)
    else:
        IDE(a.path).mainloop()


if __name__ == "__main__":
    main()
