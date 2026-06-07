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


async def _run_one(path, report):
    name = path.stem
    run_path = running_dir() / path.name
    try:
        path.rename(run_path)
    except OSError:
        return
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
    # [SILENT]: a job that finished cleanly with nothing worth saying suppresses its report
    # (kills scheduled-job notification spam). Errors always report.
    if rc == 0 and "[SILENT]" in text:
        return
    tail = "\n".join(text.strip().splitlines()[-8:])[:600]
    mark = "✅" if rc == 0 else "❌"
    await report(f"{mark} job **{name}** finished (exit {rc}, {dur}s)\n```\n{tail}\n```")


async def watch_loop(report, interval: int = 5):
    """Run queued jobs one at a time; `report(msg)` posts each result to the home channel."""
    print("job watcher started")
    while True:
        try:
            for path in sorted(queue_dir().glob("*.sh")):
                await _run_one(path, report)
        except Exception as e:
            print(f"job watcher error: {e}")
        await asyncio.sleep(interval)
