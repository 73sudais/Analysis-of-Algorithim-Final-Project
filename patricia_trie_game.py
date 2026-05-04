import tkinter as tk
from tkinter import font as tkfont
import random
import os
import math
import time

# =============================
# PATRICIA TRIE IMPLEMENTATION
# =============================

class Node:
    def __init__(self):
        self.children = {}
        self.is_end = False


class PatriciaTrie:
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        node = self.root
        node.children[word] = Node()
        node.children[word].is_end = True

    def search(self, word):
        node = self.root
        return word in node.children


# =============================
# LOAD WORDS
# =============================

file_path = os.path.join(os.path.dirname(__file__), "words.txt")

try:
    with open(file_path, "r", encoding="utf-8") as f:
        raw_words = [w.strip().lower() for w in f if w.strip()]
    words = [w for w in raw_words if 3 <= len(w) <= 5 and w.isalpha()]
except FileNotFoundError:
    # Fallback word list if words.txt not found
    words = ["cat", "car", "can", "cap", "dog", "dot", "ant", "art", "arm",
             "bat", "ban", "bad", "cup", "cut", "cub", "fan", "fat", "far",
             "hat", "ham", "has", "jar", "jam", "job", "kit", "kid", "lap",
             "log", "lot", "map", "mat", "man", "net", "nod", "not", "oak",
             "oar", "odd", "pan", "pat", "pad", "rat", "run", "rub", "sad",
             "sat", "sit", "sun", "tap", "tan", "tip", "top", "van", "vat",
             "war", "was", "web", "win", "zip", "zoo", "ace", "age", "ago",
             "aid", "aim", "air", "ale", "ape", "apt", "arc", "ash", "ask"]

trie = PatriciaTrie()
for w in words:
    trie.insert(w)

# =============================
# THEMES
# =============================

THEMES = {
    "Cosmic": {
        "bg":        "#06142e",
        "bg2":       "#0d2050",
        "accent":    "#00e5ff",
        "accent2":   "#7c4dff",
        "text":      "#e0f7fa",
        "correct":   "#00e676",
        "wrong":     "#ff1744",
        "btn_bg":    "#00e5ff",
        "btn_fg":    "#06142e",
        "btn2_bg":   "#7c4dff",
        "btn2_fg":   "#ffffff",
        "particles": "stars",
        "entry_bg":  "#112240",
        "entry_fg":  "#00e5ff",
        "score_col": "#ffd740",
        "bar_col":   "#00e5ff",
    },
    "Neon Forest": {
        "bg":        "#0a1a0a",
        "bg2":       "#0f2d0f",
        "accent":    "#39ff14",
        "accent2":   "#ff6b35",
        "text":      "#e8f5e9",
        "correct":   "#69ff47",
        "wrong":     "#ff4444",
        "btn_bg":    "#39ff14",
        "btn_fg":    "#0a1a0a",
        "btn2_bg":   "#ff6b35",
        "btn2_fg":   "#ffffff",
        "particles": "fireflies",
        "entry_bg":  "#0d2a0d",
        "entry_fg":  "#39ff14",
        "score_col": "#ffd740",
        "bar_col":   "#39ff14",
    },
    "Lava": {
        "bg":        "#1a0500",
        "bg2":       "#2d0a00",
        "accent":    "#ff6d00",
        "accent2":   "#ff1744",
        "text":      "#fff8e1",
        "correct":   "#ffeb3b",
        "wrong":     "#ff1744",
        "btn_bg":    "#ff6d00",
        "btn_fg":    "#1a0500",
        "btn2_bg":   "#ff1744",
        "btn2_fg":   "#ffffff",
        "particles": "embers",
        "entry_bg":  "#2d1200",
        "entry_fg":  "#ff6d00",
        "score_col": "#ffeb3b",
        "bar_col":   "#ff6d00",
    },
    "Arctic": {
        "bg":        "#0d1b2a",
        "bg2":       "#1b2d45",
        "accent":    "#90caf9",
        "accent2":   "#e1f5fe",
        "text":      "#e3f2fd",
        "correct":   "#80deea",
        "wrong":     "#ef9a9a",
        "btn_bg":    "#90caf9",
        "btn_fg":    "#0d1b2a",
        "btn2_bg":   "#1565c0",
        "btn2_fg":   "#ffffff",
        "particles": "snow",
        "entry_bg":  "#152536",
        "entry_fg":  "#90caf9",
        "score_col": "#ffe082",
        "bar_col":   "#90caf9",
    },
}

THEME_NAMES = list(THEMES.keys())

# =============================
# GAME VARIABLES
# =============================

score = 0
q_no = 0
MAX_Q = 5
current_word = ""
current_theme_idx = 0
particles = []
anim_time = 0
answered = False
combo = 0
high_score = 0

# =============================
# WINDOW SETUP
# =============================

window = tk.Tk()
window.title("Patricia Trie — Word Quest")
window.geometry("560x620")
window.resizable(False, False)

W, H = 560, 620

canvas = tk.Canvas(window, width=W, height=H, highlightthickness=0)
canvas.place(x=0, y=0)

# =============================
# FONT SETUP
# =============================

try:
    title_font   = tkfont.Font(family="Courier New", size=20, weight="bold")
    label_font   = tkfont.Font(family="Courier New", size=13)
    entry_font   = tkfont.Font(family="Courier New", size=15)
    btn_font     = tkfont.Font(family="Courier New", size=12, weight="bold")
    small_font   = tkfont.Font(family="Courier New", size=10)
    score_font   = tkfont.Font(family="Courier New", size=11, weight="bold")
    combo_font   = tkfont.Font(family="Courier New", size=14, weight="bold")
    hint_font    = tkfont.Font(family="Courier New", size=28, weight="bold")
except:
    title_font   = label_font = entry_font = btn_font = small_font = score_font = combo_font = hint_font = None

# =============================
# PARTICLE SYSTEM
# =============================

def init_particles(theme):
    global particles
    particles = []
    ptype = theme["particles"]

    if ptype == "stars":
        for _ in range(70):
            particles.append({
                "x": random.uniform(0, W),
                "y": random.uniform(0, H),
                "vy": random.uniform(0.3, 1.2),
                "size": random.uniform(1, 3),
                "brightness": random.uniform(0.4, 1.0),
                "twinkle": random.uniform(0, math.pi * 2),
            })
    elif ptype == "fireflies":
        for _ in range(40):
            particles.append({
                "x": random.uniform(0, W),
                "y": random.uniform(0, H),
                "vx": random.uniform(-0.5, 0.5),
                "vy": random.uniform(-0.5, 0.5),
                "size": random.uniform(2, 5),
                "phase": random.uniform(0, math.pi * 2),
                "life": random.uniform(0, 1),
            })
    elif ptype == "embers":
        for _ in range(55):
            particles.append({
                "x": random.uniform(0, W),
                "y": random.uniform(H * 0.5, H),
                "vx": random.uniform(-1, 1),
                "vy": random.uniform(-2, -0.5),
                "size": random.uniform(1, 4),
                "life": random.uniform(0, 1),
                "decay": random.uniform(0.003, 0.008),
            })
    elif ptype == "snow":
        for _ in range(60):
            particles.append({
                "x": random.uniform(0, W),
                "y": random.uniform(0, H),
                "vy": random.uniform(0.4, 1.5),
                "vx": random.uniform(-0.3, 0.3),
                "size": random.uniform(2, 5),
                "wobble": random.uniform(0, math.pi * 2),
                "wobble_speed": random.uniform(0.02, 0.05),
            })


def draw_particles(theme):
    global anim_time
    t = anim_time * 0.04
    ptype = theme["particles"]
    acc = theme["accent"]

    for p in particles:
        if ptype == "stars":
            p["y"] += p["vy"]
            p["twinkle"] += 0.05
            if p["y"] > H:
                p["y"] = 0
                p["x"] = random.uniform(0, W)
            bright = p["brightness"] * (0.6 + 0.4 * math.sin(p["twinkle"]))
            v = int(bright * 255)
            col = f"#{v:02x}{v:02x}{v:02x}"
            s = p["size"]
            canvas.create_oval(p["x"]-s, p["y"]-s, p["x"]+s, p["y"]+s,
                                fill=col, outline="")

        elif ptype == "fireflies":
            p["phase"] += 0.03
            p["life"] = (math.sin(p["phase"]) + 1) / 2
            p["x"] += p["vx"] + math.sin(p["phase"] * 0.7) * 0.4
            p["y"] += p["vy"] + math.cos(p["phase"] * 0.5) * 0.3
            if p["x"] < 0: p["x"] = W
            if p["x"] > W: p["x"] = 0
            if p["y"] < 0: p["y"] = H
            if p["y"] > H: p["y"] = 0
            alpha = int(p["life"] * 200)
            v = int(alpha)
            col = f"#39ff14" if v > 100 else f"#1a7a0a"
            s = p["size"] * p["life"]
            if s > 0.5:
                canvas.create_oval(p["x"]-s, p["y"]-s, p["x"]+s, p["y"]+s,
                                    fill=col, outline="")

        elif ptype == "embers":
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= p["decay"]
            p["vy"] -= 0.01
            if p["life"] <= 0 or p["y"] < 0:
                p["x"] = random.uniform(0, W)
                p["y"] = random.uniform(H * 0.7, H + 20)
                p["vx"] = random.uniform(-1, 1)
                p["vy"] = random.uniform(-2, -0.5)
                p["life"] = 1.0
            r = int(255)
            g = int(p["life"] * 120)
            b = 0
            col = f"#{r:02x}{g:02x}{b:02x}"
            s = p["size"] * p["life"]
            if s > 0.3:
                canvas.create_oval(p["x"]-s, p["y"]-s, p["x"]+s, p["y"]+s,
                                    fill=col, outline="")

        elif ptype == "snow":
            p["wobble"] += p["wobble_speed"]
            p["y"] += p["vy"]
            p["x"] += math.sin(p["wobble"]) * 0.5
            if p["y"] > H:
                p["y"] = -5
                p["x"] = random.uniform(0, W)
            v = random.randint(200, 255)
            col = f"#{v:02x}{v:02x}{v:02x}"
            s = p["size"]
            canvas.create_oval(p["x"]-s, p["y"]-s, p["x"]+s, p["y"]+s,
                                fill=col, outline="")


# =============================
# BACKGROUND RENDERER
# =============================

bg_items = []

def draw_bg():
    global anim_time, bg_items
    theme = THEMES[THEME_NAMES[current_theme_idx]]
    canvas.delete("bg")
    anim_time += 1
    t = anim_time

    # Gradient BG via layered rectangles
    bg = theme["bg"]
    bg2 = theme["bg2"]
    canvas.create_rectangle(0, 0, W, H, fill=bg, outline="", tags="bg")

    # Animated gradient orbs
    for i, (fx, fy, fr) in enumerate([
        (0.2, 0.3, 120), (0.8, 0.6, 100), (0.5, 0.85, 80)
    ]):
        ox = fx * W + math.sin(t * 0.008 + i * 2) * 30
        oy = fy * H + math.cos(t * 0.006 + i * 1.5) * 25
        acc2 = theme["accent2"]
        # Glow orb — layered
        for r in range(int(fr), 0, -10):
            alpha_ratio = 1 - (r / fr)
            col = _blend(bg, acc2, alpha_ratio * 0.18)
            canvas.create_oval(ox-r, oy-r, ox+r, oy+r,
                                fill=col, outline="", tags="bg")

    # Particles
    draw_particles(theme)

    # Scanline subtle overlay (stipple instead of alpha — Tkinter doesn't support 8-digit hex)
    canvas.create_rectangle(0, 0, W, H, fill="#000000",
                             stipple="gray12", outline="", tags="bg")


def _blend(hex1, hex2, t):
    """Blend two hex colors by factor t (0=hex1, 1=hex2)."""
    try:
        r1,g1,b1 = int(hex1[1:3],16), int(hex1[3:5],16), int(hex1[5:7],16)
        r2,g2,b2 = int(hex2[1:3],16), int(hex2[3:5],16), int(hex2[5:7],16)
        r = int(r1 + (r2-r1)*t)
        g = int(g1 + (g2-g1)*t)
        b = int(b1 + (b2-b1)*t)
        return f"#{r:02x}{g:02x}{b:02x}"
    except:
        return hex1


# =============================
# UI WIDGETS (canvas-based)
# =============================

# We'll use canvas text + real tkinter widgets layered on top.

frames = {}
active_frame = None

def show_frame(name):
    global active_frame
    if active_frame:
        for widget in frames.get(active_frame, []):
            widget.place_forget()
    active_frame = name
    for widget in frames.get(name, []):
        widget.place(**widget._place_kwargs)


def register(name, widget, **kwargs):
    widget._place_kwargs = kwargs
    if name not in frames:
        frames[name] = []
    frames[name].append(widget)


# =============================
# THEME SWITCHER (always visible)
# =============================

theme_label_var = tk.StringVar(value=f"Theme: {THEME_NAMES[0]}")

def cycle_theme():
    global current_theme_idx
    current_theme_idx = (current_theme_idx + 1) % len(THEME_NAMES)
    theme = THEMES[THEME_NAMES[current_theme_idx]]
    theme_label_var.set(f"Theme: {THEME_NAMES[current_theme_idx]}")
    theme_btn.config(bg=theme["accent2"], fg=theme["bg"])
    apply_theme()
    init_particles(theme)

theme_btn = tk.Button(
    window, textvariable=theme_label_var,
    font=small_font, cursor="hand2",
    relief="flat", bd=0,
    command=cycle_theme
)
theme_btn.place(x=W-140, y=8, width=132, height=26)


def apply_theme():
    theme = THEMES[THEME_NAMES[current_theme_idx]]
    theme_btn.config(bg=theme["accent2"], fg=theme["bg"])
    # Update all visible widgets
    for name, wlist in frames.items():
        for w in wlist:
            try:
                if hasattr(w, '_theme_role'):
                    role = w._theme_role
                    if role == "entry":
                        w.config(bg=theme["entry_bg"], fg=theme["entry_fg"],
                                 insertbackground=theme["accent"],
                                 highlightcolor=theme["accent"],
                                 highlightbackground=theme["accent2"])
                    elif role == "btn_main":
                        w.config(bg=theme["btn_bg"], fg=theme["btn_fg"])
                    elif role == "btn_alt":
                        w.config(bg=theme["btn2_bg"], fg=theme["btn2_fg"])
                    elif role == "label":
                        w.config(bg=theme["bg"], fg=theme["text"])
                    elif role == "accent_label":
                        w.config(bg=theme["bg"], fg=theme["accent"])
            except:
                pass


# =============================
# WELCOME SCREEN
# =============================

def make_welcome():
    theme = THEMES[THEME_NAMES[current_theme_idx]]

    lbl_title = tk.Label(window, text="◈ WORD QUEST ◈",
                         font=title_font, bg=theme["bg"], fg=theme["accent"])
    lbl_title._theme_role = "accent_label"
    register("welcome", lbl_title, x=0, y=160, width=W)

    lbl_sub = tk.Label(window, text="A Patricia Trie Adventure",
                       font=small_font, bg=theme["bg"], fg=theme["text"])
    lbl_sub._theme_role = "label"
    register("welcome", lbl_sub, x=0, y=198, width=W)

    lbl_desc = tk.Label(window,
        text="Guess the word from its first 2 letters!\n5 rounds  •  10 pts each  •  streak bonus",
        font=small_font, bg=theme["bg"], fg=theme["text"], justify="center")
    lbl_desc._theme_role = "label"
    register("welcome", lbl_desc, x=60, y=240, width=W-120)

    btn_start = tk.Button(window, text="▶  START GAME",
                          font=btn_font, relief="flat", bd=0,
                          cursor="hand2",
                          bg=theme["btn_bg"], fg=theme["btn_fg"],
                          command=start_game,
                          activebackground=theme["accent2"],
                          activeforeground=theme["bg"])
    btn_start._theme_role = "btn_main"
    register("welcome", btn_start, x=W//2-100, y=330, width=200, height=44)

    lbl_hs = tk.Label(window, text="High Score: 0",
                      font=small_font, bg=theme["bg"], fg=theme["score_col"])
    lbl_hs._theme_role = "label"
    lbl_hs._hs_label = True
    register("welcome", lbl_hs, x=0, y=400, width=W)

    # animated trie node diagram hint
    lbl_hint = tk.Label(window, text="[root] ─ c─a─t\n         └─ d─o─g\n         └─ a─n─t",
                        font=tkfont.Font(family="Courier New", size=9),
                        bg=theme["bg"], fg=theme["accent2"], justify="left")
    lbl_hint._theme_role = "label"
    register("welcome", lbl_hint, x=W//2-70, y=460, width=160)


# =============================
# GAME SCREEN
# =============================

result_label_var  = tk.StringVar(value="")
question_text_var = tk.StringVar(value="")
score_var         = tk.StringVar(value="Score: 0 / 50")
q_var             = tk.StringVar(value="Q 1 / 5")
combo_var         = tk.StringVar(value="")
progress_var      = tk.IntVar(value=0)

progress_bar_id   = None  # canvas item for progress bar

def make_game():
    theme = THEMES[THEME_NAMES[current_theme_idx]]

    # Score + Q counter row
    lbl_score = tk.Label(window, textvariable=score_var,
                         font=score_font, bg=theme["bg"], fg=theme["score_col"])
    lbl_score._theme_role = "label"
    register("game", lbl_score, x=10, y=45, width=180)

    lbl_q = tk.Label(window, textvariable=q_var,
                     font=score_font, bg=theme["bg"], fg=theme["text"])
    lbl_q._theme_role = "label"
    register("game", lbl_q, x=W-140, y=45, width=130)

    # Combo label
    lbl_combo = tk.Label(window, textvariable=combo_var,
                         font=combo_font, bg=theme["bg"], fg=theme["accent"])
    lbl_combo._theme_role = "accent_label"
    register("game", lbl_combo, x=0, y=68, width=W)

    # "The word starts with..." label
    lbl_prompt = tk.Label(window, text="THE WORD STARTS WITH:",
                          font=small_font, bg=theme["bg"], fg=theme["text"])
    lbl_prompt._theme_role = "label"
    register("game", lbl_prompt, x=0, y=120, width=W)

    # Big PREFIX display
    lbl_prefix = tk.Label(window, textvariable=question_text_var,
                          font=hint_font, bg=theme["bg"], fg=theme["accent"])
    lbl_prefix._theme_role = "accent_label"
    register("game", lbl_prefix, x=0, y=150, width=W)

    # Entry box
    global game_entry
    game_entry = tk.Entry(window, font=entry_font, justify="center",
                          relief="flat", bd=0,
                          bg=theme["entry_bg"], fg=theme["entry_fg"],
                          insertbackground=theme["accent"],
                          highlightthickness=2,
                          highlightcolor=theme["accent"],
                          highlightbackground=theme["accent2"])
    game_entry._theme_role = "entry"
    game_entry.bind("<Return>", lambda e: check_answer())
    game_entry.bind("<KeyRelease>", on_key_type)
    register("game", game_entry, x=W//2-130, y=250, width=260, height=44)

    # Typing hint (live preview)
    global lbl_preview
    lbl_preview = tk.Label(window, text="",
                           font=small_font, bg=theme["bg"], fg=theme["accent2"])
    lbl_preview._theme_role = "label"
    register("game", lbl_preview, x=0, y=300, width=W)

    # Result feedback
    lbl_result = tk.Label(window, textvariable=result_label_var,
                          font=btn_font, bg=theme["bg"], fg=theme["correct"])
    lbl_result._theme_role = "label"
    register("game", lbl_result, x=0, y=330, width=W)

    # Buttons
    btn_check = tk.Button(window, text="✔  CHECK",
                          font=btn_font, relief="flat", bd=0, cursor="hand2",
                          bg=theme["btn_bg"], fg=theme["btn_fg"],
                          command=check_answer,
                          activebackground=theme["accent2"])
    btn_check._theme_role = "btn_main"
    register("game", btn_check, x=W//2-115, y=390, width=110, height=40)

    btn_skip = tk.Button(window, text="▶  SKIP",
                         font=btn_font, relief="flat", bd=0, cursor="hand2",
                         bg=theme["btn2_bg"], fg=theme["btn2_fg"],
                         command=skip_question,
                         activebackground=theme["accent"])
    btn_skip._theme_role = "btn_alt"
    register("game", btn_skip, x=W//2+5, y=390, width=110, height=40)

    # Progress bar base
    lbl_prog_label = tk.Label(window, text="PROGRESS",
                              font=small_font, bg=theme["bg"], fg=theme["text"])
    lbl_prog_label._theme_role = "label"
    register("game", lbl_prog_label, x=10, y=450, width=80)


def on_key_type(event):
    theme = THEMES[THEME_NAMES[current_theme_idx]]
    typed = game_entry.get().strip().lower()
    prefix = current_word[:2] if current_word else ""
    if len(typed) >= 2:
        if typed.startswith(prefix):
            lbl_preview.config(text=f"✓ Prefix matches!", fg=theme["correct"])
        else:
            lbl_preview.config(text=f"✗ Should start with '{prefix}'", fg=theme["wrong"])
    else:
        lbl_preview.config(text="Type your word then press Check or Enter")


def draw_progress_bar():
    theme = THEMES[THEME_NAMES[current_theme_idx]]
    canvas.delete("progress")
    bx, by, bw, bh = 10, 468, W-20, 12
    # Track
    canvas.create_rectangle(bx, by, bx+bw, by+bh,
                              fill=theme["bg2"], outline=theme["accent2"],
                              width=1, tags="progress")
    # Fill
    fill_w = int(bw * (q_no / MAX_Q))
    if fill_w > 0:
        canvas.create_rectangle(bx+1, by+1, bx+fill_w, by+bh-1,
                                  fill=theme["bar_col"], outline="", tags="progress")
    # Dots
    for i in range(1, MAX_Q):
        dx = bx + int(bw * i / MAX_Q)
        canvas.create_line(dx, by, dx, by+bh, fill=theme["bg2"], width=2, tags="progress")

    # Stars/icons for completed
    for i in range(min(q_no, MAX_Q)):
        dx = bx + int(bw * (i + 0.5) / MAX_Q)
        canvas.create_text(dx, by+6, text="★", fill=theme["btn_fg"],
                            font=("Courier New", 7, "bold"), tags="progress")


# =============================
# RESULT SCREEN
# =============================

final_text_var  = tk.StringVar(value="")
final_score_var = tk.StringVar(value="")
grade_var       = tk.StringVar(value="")

def make_result():
    theme = THEMES[THEME_NAMES[current_theme_idx]]

    lbl_over = tk.Label(window, text="◈ GAME OVER ◈",
                        font=title_font, bg=theme["bg"], fg=theme["accent"])
    lbl_over._theme_role = "accent_label"
    register("result", lbl_over, x=0, y=140, width=W)

    lbl_fscore = tk.Label(window, textvariable=final_score_var,
                          font=tkfont.Font(family="Courier New", size=22, weight="bold"),
                          bg=theme["bg"], fg=theme["score_col"])
    lbl_fscore._theme_role = "label"
    register("result", lbl_fscore, x=0, y=190, width=W)

    lbl_grade = tk.Label(window, textvariable=grade_var,
                         font=combo_font, bg=theme["bg"], fg=theme["correct"])
    lbl_grade._theme_role = "label"
    register("result", lbl_grade, x=0, y=240, width=W)

    lbl_hs_res = tk.Label(window, textvariable=final_text_var,
                          font=small_font, bg=theme["bg"], fg=theme["text"])
    lbl_hs_res._theme_role = "label"
    register("result", lbl_hs_res, x=0, y=280, width=W)

    btn_play_again = tk.Button(window, text="▶  PLAY AGAIN",
                               font=btn_font, relief="flat", bd=0, cursor="hand2",
                               bg=theme["btn_bg"], fg=theme["btn_fg"],
                               command=restart_game)
    btn_play_again._theme_role = "btn_main"
    register("result", btn_play_again, x=W//2-110, y=340, width=220, height=44)

    btn_quit = tk.Button(window, text="✕  QUIT",
                         font=btn_font, relief="flat", bd=0, cursor="hand2",
                         bg=theme["btn2_bg"], fg=theme["btn2_fg"],
                         command=window.destroy)
    btn_quit._theme_role = "btn_alt"
    register("result", btn_quit, x=W//2-70, y=400, width=140, height=36)


# =============================
# GAME LOGIC
# =============================

def start_game():
    global score, q_no, combo, answered
    score = 0
    q_no = 0
    combo = 0
    answered = False
    score_var.set("Score: 0 / 50")
    combo_var.set("")
    show_frame("game")
    load_question()


def restart_game():
    start_game()


def load_question():
    global current_word, answered
    answered = False
    current_word = random.choice(words)
    prefix = current_word[:2]
    question_text_var.set(f"« {prefix.upper()} »")
    result_label_var.set("")
    game_entry.delete(0, tk.END)
    lbl_preview.config(text="Type your word then press Check or Enter")
    q_var.set(f"Q {q_no + 1} / {MAX_Q}")
    score_var.set(f"Score: {score} / 50")
    update_combo_display()
    draw_progress_bar()
    game_entry.focus()


def update_combo_display():
    theme = THEMES[THEME_NAMES[current_theme_idx]]
    if combo >= 3:
        combo_var.set(f"🔥 {combo}x COMBO!")
    elif combo == 2:
        combo_var.set(f"⚡ 2x COMBO!")
    elif combo == 1:
        combo_var.set(f"✓ Keep going!")
    else:
        combo_var.set("")


def check_answer():
    global score, q_no, combo, answered, high_score
    if answered:
        return
    answered = True
    theme = THEMES[THEME_NAMES[current_theme_idx]]
    ans = game_entry.get().strip().lower()

    if trie.search(ans):
        bonus = 5 if combo >= 2 else 0
        pts = 10 + bonus
        score += pts
        combo += 1
        msg = f"✔ CORRECT! +{pts} pts"
        if bonus:
            msg += f" (combo bonus!)"
        result_label_var.set(msg)
        # Flash green
        flash_feedback("#00e676")
    else:
        combo = 0
        result_label_var.set(f"✖ Wrong!  Answer: {current_word.upper()}")
        flash_feedback(theme["wrong"])

    score_var.set(f"Score: {score} / 50")
    update_combo_display()

    q_no += 1
    draw_progress_bar()

    if q_no >= MAX_Q:
        window.after(1600, show_result)
    else:
        window.after(1600, load_question)


def skip_question():
    global q_no, combo, answered
    if answered:
        return
    answered = True
    combo = 0
    result_label_var.set(f"Skipped. Answer was: {current_word.upper()}")
    update_combo_display()
    q_no += 1
    draw_progress_bar()
    if q_no >= MAX_Q:
        window.after(1400, show_result)
    else:
        window.after(1400, load_question)


def flash_feedback(color):
    canvas.delete("flash")
    canvas.create_rectangle(0, 0, W, H, fill=color, outline="",
                              stipple="gray12", tags="flash")
    window.after(200, lambda: canvas.delete("flash"))


def show_result():
    global high_score
    if score > high_score:
        high_score = score
        final_text_var.set(f"🏆 NEW HIGH SCORE!")
        # Update welcome screen high score label
        for w in frames.get("welcome", []):
            if getattr(w, '_hs_label', False):
                w.config(text=f"High Score: {high_score}")
    else:
        final_text_var.set(f"High Score: {high_score}")

    final_score_var.set(f"{score} / 50")

    if score == 50:
        grade_var.set("⭐ PERFECT — GENIUS!")
    elif score >= 40:
        grade_var.set("🔥 EXCELLENT!")
    elif score >= 30:
        grade_var.set("👍 GOOD JOB!")
    elif score >= 20:
        grade_var.set("😐 KEEP PRACTICING")
    else:
        grade_var.set("💪 TRY AGAIN!")

    show_frame("result")


# =============================
# MAIN LOOP
# =============================

def animate():
    theme = THEMES[THEME_NAMES[current_theme_idx]]
    draw_bg()
    if active_frame == "game":
        draw_progress_bar()
    window.after(40, animate)


# =============================
# INIT
# =============================

init_particles(THEMES[THEME_NAMES[0]])
make_welcome()
make_game()
make_result()

show_frame("welcome")
animate()
window.mainloop()