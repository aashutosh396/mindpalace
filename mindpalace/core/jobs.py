"""
Background job dispatch — what makes the agent feel ALIVE.

For anything slow (backups, deploys, big scrapes), the brain doesn't block the chat.
It drops a shell script into the job queue and replies instantly ("queued it"). A
watcher running inside the gateway executes queued jobs in the background and REPORTS
THE RESULT back to the home channel when each finishes — so you keep chatting meanwhile.

  user-data/jobs/queue/    *.sh waiting to run   (the brain writes here)
  user-data/jobs/running/  currently executing
  user-data/jobs/done/     <name>.log  (output + exit code), kept for inspection

The brain is told (in its system prompt) how to queue a job. No triage call needed —
the brain decides what's worth backgrounding.
"""
from __future__ import annotations

import asyncio
import json
import time

from .. import config


def _d(sub):
    p = config.home() / "jobs" / sub
    p.mkdir(parents=True, exist_ok=True)
    return p


def queue_dir():   return _d("queue")
def running_dir(): return _d("running")
def done_dir():    return _d("done")


def submit(name: str, script: str) -> str:
    """Programmatic submit (the brain usually just writes the file itself)."""
    safe = "".join(c for c in name if c.isalnum() or c in "-_") or "job"
    fn = f"{safe}-{int(time.time())}.sh"
    (queue_dir() / fn).write_text(script)
    return fn


def _meta_for(path) -> dict:
    """Origin sidecar (`<file>.meta`) written when a turn queues a job: which channel asked
    (the report routes back there) and, for agent tasks, which persona/session to fork.
    Read at pickup — NOT consumed; it travels with the job into running/ so a crash/restart
    can restore both. {} for jobs with no origin (cron, hand-written)."""
    try:
        return json.loads(path.with_name(path.name + ".meta").read_text())
    except Exception:
        return {}


def _move_meta(src, dst) -> None:
    """Move a job's sidecar along with it (queue → running)."""
    m = src.with_name(src.name + ".meta")
    try:
        if m.exists():
            m.rename(dst.with_name(dst.name + ".meta"))
    except OSError:
        pass


def _drop_meta(path) -> None:
    try:
        path.with_name(path.name + ".meta").unlink()
    except OSError:
        pass


def _recover(run_dir, q_dir) -> int:
    """Daemon restarted mid-job: anything still in running/ was ORPHANED by the crash — it
    would otherwise sit there dead forever ('I'll ping you when done' that never comes).
    Move each job (and its origin sidecar) back to the queue so it runs again. Called once
    per watcher start; returns how many were requeued."""
    n = 0
    try:
        for p in sorted(run_dir.glob("*")):
            if p.name.endswith(".meta"):
                continue                          # moved together with its job below
            try:
                m = p.with_name(p.name + ".meta")
                p.rename(q_dir / p.name)
                if m.exists():
                    m.rename(q_dir / m.name)
                n += 1
            except OSError:
                pass
    except OSError:
        pass
    return n


def _too_fresh(path, grace: float = 20.0) -> bool:
    """A queued file with no meta yet, younger than `grace` seconds — the gateway may still be
    stamping its origin (it stamps on the next stream event after the brain writes the file).
    Skip this cycle; the next pass picks it up."""
    if path.with_name(path.name + ".meta").exists():
        return False
    try:
        return time.time() - path.stat().st_mtime < grace
    except OSError:
        return False


async def _run_one(path, report):
    if _too_fresh(path):
        return
    name = path.stem
    meta = _meta_for(path)
    run_path = running_dir() / path.name
    try:
        path.rename(run_path)
    except OSError:
        return
    _move_meta(path, run_path)
    started = time.time()
    try:
        proc = await asyncio.create_subprocess_exec(
            "bash", str(run_path), cwd=str(config.home()),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
        out, _ = await asyncio.wait_for(proc.communicate(), timeout=3600)
        rc, text = proc.returncode, out.decode(errors="replace")
    except asyncio.TimeoutError:
        rc, text = 124, "(job timed out after 1h)"
    except Exception as e:
        rc, text = 1, f"(job error: {e})"
    dur = int(time.time() - started)
    (done_dir() / f"{name}.log").write_text(f"exit={rc} dur={dur}s\n\n{text}")
    try:
        run_path.unlink()
    except OSError:
        pass
    _drop_meta(run_path)
    # [SILENT]: a job that finished cleanly with nothing worth saying suppresses its report
    # (kills scheduled-job notification spam). Errors always report.
    if rc == 0 and "[SILENT]" in text:
        return
    tail = "\n".join(text.strip().splitlines()[-8:])[:600]
    mark = "✅" if rc == 0 else "❌"
    await report(f"{mark} job **{name}** finished (exit {rc}, {dur}s)\n```\n{tail}\n```",
                 meta.get("channel"))


async def watch_loop(report, interval: int = 5):
    """Run queued jobs one at a time; `report(msg, channel_id)` posts each result back to the
    job's ORIGIN channel (home when it has none). Requeues jobs orphaned by a restart first."""
    n = _recover(running_dir(), queue_dir())
    if n:
        print(f"[jobs] requeued {n} job(s) orphaned by a restart")
    print("job watcher started")
    while True:
        try:
            for path in sorted(queue_dir().glob("*.sh")):
                await _run_one(path, report)
        except Exception as e:
            print(f"job watcher error: {e}")
        await asyncio.sleep(interval)


# ======================================================================
# Background AGENT jobs (Tier 2/3): hand off a long AGENTIC task — not a
# shell script, but real reasoning + tool use — to run async. The brain drops
# the task here, replies instantly, and a watcher runs it on a FORK of the live
# session (full context, lock-free → doesn't block live chat) and reports back.
#
#   jobs/agent_queue/   <name>.task  (plain text = the task)  OR  <name>.json
#   jobs/agent_running/ currently executing
#   jobs/agent_done/    <name>.log   (task + result), kept for inspection
# ======================================================================

def agent_queue_dir():   return _d("agent_queue")
def agent_running_dir(): return _d("agent_running")
def agent_done_dir():    return _d("agent_done")


def submit_agent(task: str, name: str = "task", system: str | None = None) -> str:
    """Programmatic submit of a background agent task (the brain may also just write a .task file)."""
    safe = "".join(c for c in name if c.isalnum() or c in "-_") or "task"
    fn = f"{safe}-{int(time.time())}.json"
    (agent_queue_dir() / fn).write_text(json.dumps({"task": task, "system": system, "ts": time.time()}))
    return fn


# Tier 3: wrap a handed-off task so the background worker decomposes + summarizes — a big task
# self-chunks into ordered steps instead of one monolithic, easy-to-stall blob.
_AGENT_WRAP = (
    "You are running as a BACKGROUND worker — the owner is NOT waiting live, so work autonomously "
    "and DON'T ask questions; make sensible decisions and proceed. Do this end to end:\n\n"
    "{task}\n\n"
    "First break it into clear ordered steps, then carry them out one by one. When finished, reply "
    "with a SHORT summary: what you created/changed (files + key decisions) and anything the owner "
    "should review or run."
)


def _load_agent_task(path) -> tuple[str, str | None]:
    """Return (task_text, system) from a .task (plain text) or .json file. ('' , None) if unreadable."""
    try:
        if path.suffix == ".json":
            spec = json.loads(path.read_text())
            return (spec.get("task", "") or "").strip(), spec.get("system")
        return path.read_text().strip(), None
    except Exception:
        return "", None


async def _run_agent_one(path, report):
    from . import brain
    if _too_fresh(path):
        return
    task, system = _load_agent_task(path)
    meta = _meta_for(path)
    chan = meta.get("channel")
    if meta.get("system"):                       # origin persona: fork the ROOM's session, not main's
        system = meta["system"]
    name = path.stem
    if not task:
        try: path.unlink()
        except OSError: pass
        return
    run_path = agent_running_dir() / path.name
    try:
        path.rename(run_path)
    except OSError:
        return
    _move_meta(path, run_path)
    await report(f"🛠️ started background task **{name}** — working on it, I'll report back "
                 "when it's done.", chan)
    started = time.time()
    prompt = _AGENT_WRAP.format(task=task)
    try:
        sid = brain.current_session_id(system)            # fork the live session if one exists today
        if sid:
            reply = await brain.ask_resumed(prompt, sid, timeout=config.agent_job_timeout())
            if reply.startswith("(empty;") and "No conversation found" in reply:
                # fork raced the session's own creation (the create turn was still streaming
                # when we tried to fork it) → run fresh instead of dying with '(empty…)'
                reply = await brain.ask_async(prompt, [], system=system)
        else:                                             # no live session → fresh, self-contained turn
            reply = await brain.ask_async(prompt, [], system=system)
    except Exception as e:
        reply = f"(background task error: {e})"
    dur = int(time.time() - started)
    (agent_done_dir() / f"{name}.log").write_text(f"dur={dur}s\n\nTASK:\n{task}\n\nRESULT:\n{reply}")
    try: run_path.unlink()
    except OSError: pass
    _drop_meta(run_path)
    mins = f"{dur // 60}m{dur % 60}s" if dur >= 60 else f"{dur}s"
    bad = reply.startswith("(") and reply.endswith(")")   # our error/timeout markers
    mark = "⚠️" if bad else "✅"
    await report(f"{mark} background task **{name}** done ({mins})\n\n{reply[:1500]}", chan)


async def agent_watch_loop(report, interval: int = 5):
    """Run queued background AGENT tasks one at a time; start + result report back to the
    task's ORIGIN channel (home when it has none). Runs on forked sessions, so it executes
    ALONGSIDE live chat without taking the session lock."""
    n = _recover(agent_running_dir(), agent_queue_dir())
    if n:
        print(f"[jobs] requeued {n} agent task(s) orphaned by a restart")
        try:
            await report(f"🔁 requeued **{n}** background task(s) that were orphaned by a "
                         "restart — running them now.")
        except Exception:
            pass
    print("agent-job watcher started")
    while True:
        try:
            for path in sorted([*agent_queue_dir().glob("*.task"), *agent_queue_dir().glob("*.json")]):
                await _run_agent_one(path, report)
        except Exception as e:
            print(f"agent-job watcher error: {e}")
        await asyncio.sleep(interval)
