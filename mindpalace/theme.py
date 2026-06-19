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
SPIN_FRAMES = "✻✢✶✷✸✹✺"


def fmt_dur(seconds) -> str:
    s = int(seconds)
    return f"{s // 60}m {s % 60}s" if s >= 60 else f"{s}s"


def cook_verb(elapsed, every: float = 9.0) -> str:
    """Whimsical verb that rotates every ~9s of elapsed time."""
    return COOK_VERBS[int(elapsed // every) % len(COOK_VERBS)]


def spin_frame(elapsed, fps: float = 4.0) -> str:
    """Rotating spinner glyph (for gateways that animate by re-rendering, e.g. Discord edits)."""
    return SPIN_FRAMES[int(elapsed * fps) % len(SPIN_FRAMES)]


def cook_status(elapsed, hint: str = "thinking") -> str:
    """Rich-markup status text (verb + timer) — pair with a rich spinner glyph for the terminal.
    Renders e.g. 'Fermenting… (11s · thinking)' in coral + dim."""
    return f"[bold {Palette.CORAL}]{cook_verb(elapsed)}…[/] [{Palette.DIM}]({fmt_dur(elapsed)} · {hint})[/]"


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
