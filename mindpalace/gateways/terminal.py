"""
Terminal gateway — a polished, Claude-Code-style chat UI in your shell.

Same brain/memory/skills as Discord; a local REPL with a banner, colored prompt,
a thinking spinner, and markdown-rendered replies (via `rich`; degrades to plain text
if rich isn't installed).

Commands:  /exit  /quit  /status  /help   (Ctrl-D to leave)
"""
from __future__ import annotations

import json
import os
import sys
import time

from ..core import brain, updater
from .. import config
from ..memory import store as mem

KEEP = 24


def _check_for_update(force: bool = False) -> str | None:
    """Poll git for new commits, at most once per `update_check_minutes` (0 = off).
    If the remote is ahead, drop the pending marker and return a friendly notice to print;
    otherwise clear it and return None. Self-rate-limits via state on the function object,
    so it's cheap to call every REPL turn. `force` ignores the interval (used at startup)."""
    interval = updater.interval_minutes()
    if interval <= 0:
        return None
    now = time.time()
    last = getattr(_check_for_update, "_last", 0.0)
    if not force and now - last < interval * 60:
        return None
    _check_for_update._last = now
    try:
        info = updater.check()
    except Exception:                       # network/git hiccup — stay quiet, retry next interval
        return None
    if not info:
        updater.clear_pending()
        return None
    updater.write_pending({"remote_sha": info["remote_sha"], "behind": info["behind"]})
    return updater.notice_text(info)


def _apply_update(printer) -> None:
    """Owner said yes in the terminal: fast-forward pull, then re-exec this process so the
    new code loads. Leaves things untouched if local edits block the pull."""
    ok, out = updater.pull()
    updater.clear_pending()
    if not ok:
        printer("⚠️ Couldn't auto-update — looks like there are local changes in the way. "
                "Left things as they are; this one needs a hand.")
        return
    printer("✅ Update pulled. Reloading myself now — one sec… 🔄")
    os.execvp(sys.argv[0], sys.argv)        # replace the running process with fresh code


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


def _stream_reply(text, history, show):
    """Drive the SAME brain Discord uses, printing each live step via show(line).
    Keeps terminal and Discord behaviour identical — one base, one evolving intelligence."""
    import asyncio

    async def _go():
        async def on_progress(line):
            show(line)
        return await brain.ask_async_streaming(text, history, on_progress)

    return asyncio.run(_go())


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

    def _notice(msg):
        console.print(Panel(Markdown(msg), title="[bold yellow]update[/]",
                            title_align="left", border_style="yellow", padding=(0, 1)))

    startup = _check_for_update(force=True)         # surface a waiting update right away
    if startup:
        _notice(startup)
    while True:
        notice = _check_for_update()                # ~every interval: nag while behind
        if notice:
            _notice(notice)
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
        # pending update + owner says "yes" → pull + reload (never goes to the brain)
        if updater.read_pending() and updater.is_affirmative(text):
            _apply_update(lambda m: console.print(f"[yellow]{m}[/]"))
            continue
        console.print(f"[dim]{name} is on it…[/]")
        reply = _stream_reply(text, history, lambda l: console.print(f"[dim]  {l}[/]"))
        console.print(Panel(Markdown(reply), title=f"[bold green]{name}[/]",
                            title_align="left", border_style="green", padding=(0, 1)))
        history += [{"role": "Owner", "content": text},
                    {"role": "Assistant", "content": reply}]
        _save(history)
        mem.save_exchange(text, reply)


def _run_plain(name):
    print(f"\n{name} — terminal chat. /exit to leave.\n")
    history = _load()
    startup = _check_for_update(force=True)
    if startup:
        print(f"\n{startup}\n")
    while True:
        notice = _check_for_update()
        if notice:
            print(f"\n{notice}\n")
        try:
            text = input("you > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye."); break
        if not text:
            continue
        if text in ("/exit", "/quit"):
            print("bye."); break
        if updater.read_pending() and updater.is_affirmative(text):
            _apply_update(print)
            continue
        reply = _stream_reply(text, history, lambda l: print(f"  {l}"))
        print(f"\n{name} > {reply}\n")
        history += [{"role": "Owner", "content": text},
                    {"role": "Assistant", "content": reply}]
        _save(history)
        mem.save_exchange(text, reply)
