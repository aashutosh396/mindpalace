"""
mindpalace visual theme — coral primary, Hermes-grade terminal polish.

Why coral? Warm reds/oranges around the coral band (#FF6B5C) read as *energising
but not alarming*. For ADHD brains a warm focal accent holds attention and gives
clear "this is the thing" anchoring without the cold, easy-to-tune-out feel of the
old cyan. One primary colour, used consistently, = less visual noise to filter.

Everything here is pure data + tiny helpers. No state, no I/O. Degrades cleanly:
if `rich` / `prompt_toolkit` aren't present the caller falls back to plain text.
"""
from __future__ import annotations


class Palette:
    """The coral system. Hex values are true-color; terminals that lack 24-bit
    color round to the nearest 256-color cell — still warm, still coral-ish."""
    CORAL        = "#FF6B5C"   # PRIMARY — prompts, borders, the agent's name
    CORAL_BRIGHT = "#FF8A6B"   # hover / emphasis
    CORAL_SOFT   = "#FFA07A"   # light salmon — secondary accents
    PEACH        = "#FFB39A"   # softest tint — logo top, gentle highlights
    CORAL_DEEP   = "#E8543F"   # pressed / strong
    EMBER        = "#D94436"   # deepest — logo bottom, warnings that aren't errors
    TEXT         = "#FFE9E2"   # warm cream — body text on dark
    DIM          = "#C58A7C"   # muted coral-taupe — labels, hints, metadata
    OK           = "#7BD88F"   # success green (kept — universally "done")
    WARN         = "#FFC861"   # amber — updates / attention
    ERR          = "#FF5370"   # error red


# ── ASCII wordmark (ANSI Shadow). 80 cols wide; gate display on terminal width. ──
LOGO_LINES = [
    "███╗   ███╗██╗███╗   ██╗██████╗ ██████╗  █████╗ ██╗      █████╗  ██████╗███████╗",
    "████╗ ████║██║████╗  ██║██╔══██╗██╔══██╗██╔══██╗██║     ██╔══██╗██╔════╝██╔════╝",
    "██╔████╔██║██║██╔██╗ ██║██║  ██║██████╔╝███████║██║     ███████║██║     █████╗  ",
    "██║╚██╔╝██║██║██║╚██╗██║██║  ██║██╔═══╝ ██╔══██║██║     ██╔══██║██║     ██╔══╝  ",
    "██║ ╚═╝ ██║██║██║ ╚████║██████╔╝██║     ██║  ██║███████╗██║  ██║╚██████╗███████╗",
    "╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝",
]
LOGO_WIDTH = 80

# top→bottom warm gradient across the six logo rows
_LOGO_GRADIENT = [
    Palette.PEACH, Palette.CORAL_SOFT, Palette.CORAL_BRIGHT,
    Palette.CORAL, Palette.CORAL_DEEP, Palette.EMBER,
]


def logo_markup() -> str:
    """Rich-markup version of the wordmark, one gradient color per line."""
    return "\n".join(
        f"[bold {c}]{line}[/]" for c, line in zip(_LOGO_GRADIENT, LOGO_LINES)
    )


def logo_fits(term_width: int) -> bool:
    return term_width >= LOGO_WIDTH + 4


# ── "cooking" thinking spinner — Claude-Code-style: rotating glyph + whimsical verb + live timer.
#    On-brand for Ginji ("let's start cooking"). Shared by both gateways so terminal + Discord match. ──
COOK_VERBS = [
    "Simmering", "Fermenting", "Marinating", "Whisking", "Kneading", "Reducing",
    "Proofing", "Basting", "Caramelizing", "Plating", "Seasoning", "Sautéing",
    "Folding", "Searing", "Glazing", "Braising", "Tasting", "Stirring",
]
# One emoji PER verb (paired 1:1 with COOK_VERBS above). The emoji changes only when the word
# changes (~9s) — no fast spin; each new "dish" is a fresh sight.
COOK_EMOJI = ["🍲", "🫙", "🥩", "🥚", "🥖", "🔥", "🍞", "🍗", "🍮", "🍽️",
              "🧂", "🍳", "🥟", "🍖", "🍯", "🥘", "😋", "🥄"]


def blank_spinner_name() -> str:
    """A no-op rich spinner (single blank frame) so console.status shows ONLY our paired
    emoji+verb text, with no separately-animating glyph. Falls back to 'dots' if rich is absent."""
    try:
        from rich.spinner import SPINNERS
        if "blank" not in SPINNERS:
            SPINNERS["blank"] = {"interval": 100000, "frames": [" "]}
        return "blank"
    except Exception:
        return "dots"


def fmt_dur(seconds) -> str:
    s = int(seconds)
    return f"{s // 60}m {s % 60}s" if s >= 60 else f"{s}s"


def random_verb_offset() -> int:
    """Pick once per turn so each turn STARTS on a different verb (not always 'Simmering')."""
    import random
    return random.randrange(len(COOK_VERBS))


def cook_verb(elapsed, every: float = 30.0, offset: int = 0) -> str:
    """Whimsical verb that rotates only every ~30s — calm (1-2 changes in a typical turn), not a
    distracting every-few-seconds churn. `offset` (per-turn random start) varies the opening verb."""
    return COOK_VERBS[(int(elapsed // every) + offset) % len(COOK_VERBS)]


def cook_emoji(elapsed, every: float = 30.0, offset: int = 0) -> str:
    """The emoji PAIRED to the current verb — changes only when the verb changes (~30s)."""
    return COOK_EMOJI[(int(elapsed // every) + offset) % len(COOK_EMOJI)]


# Escalating worded hint (Claude-Code-style) — grows as the turn drags on. More stages = more
# variety over a long turn.
_HINTS = [
    (0, "thinking"), (10, "thinking some more"), (22, "still simmering"),
    (38, "letting it reduce"), (58, "almost done thinking"), (85, "thinking real hard"),
    (120, "deep in the sauce"), (170, "this one's a slow cook"), (240, "still on it, hang tight"),
]


def cook_hint(elapsed) -> str:
    e = int(elapsed)
    hint = _HINTS[0][1]
    for thresh, label in _HINTS:
        if e >= thresh:
            hint = label
    return hint


_PULSE = "⣿⣶⣦⣄⣀"            # braille comet: head → fading tail


def trail(elapsed=0, width: int = 8, step: float = 0.35) -> str:
    """A braille MOVING PULSE — a bright comet that scans back and forth with a fading tail,
    e.g. '[⣿⣶⣦⣄⣀⣀⣀⣀]'. Position advances with `elapsed`, so it visibly moves each redraw
    (smooth in the terminal at 0.5s, stepping in Discord per edit)."""
    n = int(elapsed / step)
    period = 2 * (width - 1) if width > 1 else 1
    p = n % period
    head = p if p < width else period - p           # ping-pong across the track
    cells = [_PULSE[d] if (d := abs(i - head)) < len(_PULSE) else "⣀" for i in range(width)]
    return "[" + "".join(cells) + "]"


def cook_status(elapsed, offset: int = 0) -> str:
    """Rich-markup status: '<emoji> <verb> (<timer> · <hint>) <shimmer trail>' — no '…' dots.
    e.g. '🍮 Caramelizing (1m 7s · almost done thinking) =_=_=_='."""
    return (f"{cook_emoji(elapsed, offset=offset)} "
            f"[bold {Palette.CORAL}]{cook_verb(elapsed, offset=offset)}[/] "
            f"[{Palette.DIM}]({fmt_dur(elapsed)} · {cook_hint(elapsed)})[/] "
            f"[{Palette.CORAL}]{trail(elapsed)}[/]")


def baked_line(elapsed) -> str:
    """Rich-markup done-line, e.g. '✻ Baked for 2m 23s'."""
    return f"[{Palette.DIM}]✻ Baked for {fmt_dur(elapsed)}[/]"


# ── prompt_toolkit style (the bordered input box) ──
def pt_style():
    """Coral input frame + prompt caret. None if prompt_toolkit is absent."""
    try:
        from prompt_toolkit.styles import Style
    except ImportError:
        return None
    return Style.from_dict({
        "frame.border": Palette.CORAL,
        "prompt":       f"{Palette.CORAL} bold",
        "":             Palette.TEXT,          # typed text
    })


# ── rich theme (named styles so markup can say [accent]…[/] etc.) ──
def rich_theme():
    """A rich Theme mapping semantic names → coral palette. None if rich absent."""
    try:
        from rich.theme import Theme
    except ImportError:
        return None
    return Theme({
        "accent":  f"bold {Palette.CORAL}",
        "accent2": Palette.CORAL_SOFT,
        "body":    Palette.TEXT,
        "muted":   Palette.DIM,
        "ok":      Palette.OK,
        "warn":    Palette.WARN,
        "err":     Palette.ERR,
        "agent":   f"bold {Palette.CORAL}",
        "switch":  f"bold {Palette.CORAL_BRIGHT}",   # model-switch notice
    })
