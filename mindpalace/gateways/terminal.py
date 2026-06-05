"""
Terminal gateway — a polished, Claude-Code-style chat UI in your shell.

Same brain/memory/skills as Discord; a local REPL with a banner, colored prompt,
a thinking spinner, and markdown-rendered replies (via `rich`; degrades to plain text
if rich isn't installed).

Commands:  /exit  /quit  /status  /help   (Ctrl-D to leave)
"""
from __future__ import annotations

import json

from ..core import brain
from .. import config
from ..memory import store as mem

KEEP = 24


def _hist():
    return config.state_dir() / "history.json"


def _load():
    try:
        return json.loads(_hist().read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save(h):
    config.state_dir().mkdir(parents=True, exist_ok=True)
    _hist().write_text(json.dumps(h[-KEEP:], indent=2))


def _agent_name() -> str:
    n = config.load_config().get("agent_name")
    if n:
        return n
    try:
        first = config.AGENT_FILE().read_text().lstrip("# ").splitlines()[0].strip()
        # ignore a literal "AGENT.md"/"AGENT" heading
        if first and first.lower() not in ("agent.md", "agent"):
            return first
    except OSError:
        pass
    return "mindpalace"


def _make_boxed_input():
    """Claude-style 2-line bordered input with a `>` prompt. None if prompt_toolkit absent."""
    try:
        from prompt_toolkit import Application
        from prompt_toolkit.layout import Layout
        from prompt_toolkit.widgets import Frame, TextArea
        from prompt_toolkit.key_binding import KeyBindings
        from prompt_toolkit.styles import Style
    except ImportError:
        return None

    style = Style.from_dict({"frame.border": "#5fafff", "prompt": "#5fafff bold"})

    def ask() -> str | None:
        ta = TextArea(multiline=True, height=2, wrap_lines=True,
                      prompt=[("class:prompt", "> ")])
        kb = KeyBindings()

        @kb.add("enter")
        def _(e): e.app.exit(result=ta.text)

        @kb.add("escape", "enter")          # alt/opt+Enter = newline
        def _(e): ta.buffer.insert_text("\n")

        @kb.add("c-c")
        @kb.add("c-d")
        def _(e): e.app.exit(result=None)

        return Application(layout=Layout(Frame(ta)), key_bindings=kb,
                           style=style, full_screen=False, mouse_support=False).run()
    return ask


def run():
    name = _agent_name()
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.markdown import Markdown
    except ImportError:
        return _run_plain(name)
    boxed = _make_boxed_input()

    console = Console()
    console.print(Panel(
        f"[bold]{name}[/]  [dim]· self-learning agent[/]\n"
        f"[dim]data:[/] {config.home()}\n"
        f"[dim]type your message · /help · /exit[/]",
        title="[bold cyan]◈ mindpalace[/]", title_align="left",
        border_style="cyan", padding=(1, 2)))
    history = _load()
    while True:
        if boxed:
            text = boxed()
            if text is None:
                console.print("[dim]bye.[/]"); break
            text = text.strip()
        else:
            try:
                text = console.input("\n[bold cyan]you[/] [dim]›[/] ").strip()
            except (EOFError, KeyboardInterrupt):
                console.print("\n[dim]bye.[/]"); break
        if not text:
            continue
        if text in ("/exit", "/quit"):
            console.print("[dim]bye.[/]")
            break
        if text == "/help":
            console.print("[dim]/status  /exit  · everything else goes to the agent[/]")
            continue
        if text == "/status":
            cfg = config.load_config()
            console.print(f"[dim]data {config.home()} · gateway {cfg.get('gateway')}[/]")
            continue
        with console.status(f"[dim]{name} is thinking…[/]", spinner="dots"):
            reply = brain.ask_sync(text, history)
        console.print(Panel(Markdown(reply), title=f"[bold green]{name}[/]",
                            title_align="left", border_style="green", padding=(0, 1)))
        history += [{"role": "Owner", "content": text},
                    {"role": "Assistant", "content": reply}]
        _save(history)
        mem.save_exchange(text, reply)


def _run_plain(name):
    print(f"\n{name} — terminal chat. /exit to leave.\n")
    history = _load()
    while True:
        try:
            text = input("you > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye."); break
        if not text:
            continue
        if text in ("/exit", "/quit"):
            print("bye."); break
        print("…thinking", end="\r")
        reply = brain.ask_sync(text, history)
        print(" " * 12, end="\r")
        print(f"\n{name} > {reply}\n")
        history += [{"role": "Owner", "content": text},
                    {"role": "Assistant", "content": reply}]
        _save(history)
        mem.save_exchange(text, reply)
