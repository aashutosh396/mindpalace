"""Web gateway — the v3 GUI's backend. Third gateway beside Discord/WhatsApp.

Two-layer model:
  /api/projects…  the INVENTORY (folders/repos on disk; keeper-managed)
  /api/rooms…     the owner's CHANNELS (chat + kanban + assets + routines),
                  each connected to any number of projects for grounding.

Serves three things on one localhost port: REST under /api, the live WS event
bus at /ws, and the pre-built Nuxt bundle at /. Run: mindpalace serve [--port N]
[--dev]. The desktop app spawns this same gateway as its sidecar.
"""
from __future__ import annotations

import asyncio
import json
import re
from contextlib import asynccontextmanager
from pathlib import Path

from .. import config
from ..projects import home, store, triage, worker

DEFAULT_PORT = 7777

# Module-level import, guarded: the WebSocket annotation must live in module
# globals for FastAPI to resolve it (PEP 563 strings + py3.9), and the module
# must still import cleanly when the [web] extra isn't installed.
try:
    from fastapi import FastAPI, UploadFile, WebSocket, WebSocketDisconnect
    from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    _HAVE_WEB = True
except ImportError:
    _HAVE_WEB = False


def _require_fastapi():
    if not _HAVE_WEB:
        raise SystemExit(
            'web gateway needs FastAPI — install with:  pip install "mindpalace[web]"\n'
            "(or from the repo:  ./install.sh web)")


class Bus:
    def __init__(self):
        self.clients: set = set()

    async def broadcast(self, kind: str, data: dict):
        msg = json.dumps({"event": kind, "data": data})
        dead = []
        for ws in self.clients:
            try:
                await ws.send_text(msg)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.clients.discard(ws)


def create_app():
    _require_fastapi()
    bus = Bus()

    async def _recover_hall():
        """A restart mid-decision kills the concierge task — the owner's last
        message would sit unanswered forever. Re-handle it on startup."""
        last = store.list_home_chat(1)
        if last and last[-1]["role"] == "user":
            await home.handle(last[-1]["text"], bus.broadcast)

    @asynccontextmanager
    async def lifespan(app):
        wtask = asyncio.create_task(worker.watch_loop(bus.broadcast))
        stask = asyncio.create_task(worker.routine_loop(bus.broadcast))
        rtask = asyncio.create_task(_recover_hall())
        yield
        for t in (wtask, stask, rtask):
            t.cancel()

    app = FastAPI(title="mindpalace", docs_url=None, redoc_url=None, lifespan=lifespan)
    app.state.bus = bus

    def _404(what: str):
        return JSONResponse({"error": f"{what} not found"}, status_code=404)

    # ---- health / status ----
    @app.get("/api/health")
    def health():
        from ..providers import get_provider
        from ..projects import updates
        from .. import __version__
        p = get_provider()
        ok, why = p.available()
        return {"version": __version__, "commit": updates.local_commit()[:12],
                "provider": p.name, "provider_ok": ok, "provider_status": why}

    # ---- first-run onboarding ----
    @app.get("/api/onboarding")
    def onboarding_get():
        cfg = config.load_config()
        web = cfg.get("web", {})
        try:                                          # vault users skip the seed question
            vault_present = any((config.vault_dir() / "projects").glob("*.md"))
        except Exception:
            vault_present = False
        return {"onboarded": bool(web.get("onboarded")),
                "name": web.get("owner_name", ""),
                "vault_present": vault_present,
                "workspace": str(config.workspace_dir())}

    @app.post("/api/onboarding")
    def onboarding_set(body: dict):
        cfg = config.load_config()
        web = cfg.setdefault("web", {})
        if "name" in body:
            web["owner_name"] = str(body["name"]).strip()[:60]
        if (body.get("workspace") or "").strip():
            config.set_workspace(body["workspace"].strip())
            cfg = config.load_config()                # set_workspace saved; re-read + re-merge
            web = cfg.setdefault("web", {})
            if "name" in body:
                web["owner_name"] = str(body["name"]).strip()[:60]
        if body.get("onboarded"):
            web["onboarded"] = True
        config.save_config(cfg)
        return {"ok": True}

    @app.post("/api/onboarding/seed")
    async def onboarding_seed(body: dict):
        """Seed the inventory: a deterministic general card for the keeper."""
        mode = body.get("mode")
        if mode == "folder":
            path = (body.get("path") or "").strip()
            root = Path(path).expanduser()
            if not root.is_dir():
                return JSONResponse({"error": f"not a folder: {path}"}, status_code=422)
            task_body = (
                f"Scan {root} for the owner's projects (each subfolder that looks like a "
                "real project — has code, a git repo, or a README). For each one, create a "
                "PROJECT in the inventory and attach its main folder. Do NOT create rooms. "
                "Report how many projects you loaded.")
            title = f"Load projects from {root.name}"
        elif mode == "vault":
            task_body = (
                "Read the mindpalace vault's project pointer files and load every tracked "
                "project into the inventory: create a PROJECT per pointer and attach its "
                "folder(s) from the pointer's paths. Do NOT create rooms. Report the count.")
            title = "Load projects from the mindpalace vault"
        else:
            return JSONResponse({"error": "mode must be folder or vault"}, status_code=422)
        room = store.ensure_home_room()
        task = store.create_task(room["id"], title, task_body)
        await bus.broadcast("task.created", task)
        return {"task": task}

    # ---- dev-channel updates ----
    @app.get("/api/update/check")
    async def update_check():
        from ..projects import updates
        try:
            return await asyncio.get_running_loop().run_in_executor(None, updates.check)
        except Exception as e:
            return JSONResponse({"error": f"update check failed: {str(e)[:160]}"}, status_code=502)

    @app.post("/api/update/apply")
    async def update_apply():
        from ..projects import updates
        try:
            return await asyncio.get_running_loop().run_in_executor(None, updates.apply)
        except Exception as e:
            return JSONResponse({"error": f"update failed: {str(e)[:160]}"}, status_code=502)

    # =================================================================
    # PROJECTS — the inventory
    # =================================================================
    @app.get("/api/projects")
    def projects_list():
        out = store.list_projects()
        for p in out:                                # folders vs git repos
            for row in p["repos"]:
                g = Path(row["path"]) / ".git"
                row["is_git"] = g.is_dir() or g.is_file()
        return out

    @app.post("/api/projects")
    async def projects_create(body: dict):
        name = (body.get("name") or "").strip()
        if not name:
            return JSONResponse({"error": "name required"}, status_code=422)
        p = store.create_project(name)
        path = (body.get("path") or "").strip()
        if body.get("workspace"):                    # scaffold a fresh home in the nursery
            import subprocess
            folder = config.workspace_dir() / p["slug"]
            folder.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "init", "-q", str(folder)], timeout=10, capture_output=True)
            store.add_repo(p["id"], str(folder), is_primary=True)
        elif path:                                   # attach an existing folder in the same call
            await _attach_folder(p["id"], path)
        await bus.broadcast("projects.changed", {})
        return next((x for x in store.list_projects() if x["id"] == p["id"]), p)

    @app.patch("/api/projects/{pid}")
    async def project_rename(pid: int, body: dict):
        p = store.rename_project(pid, body.get("name", ""))
        if p:
            await bus.broadcast("projects.changed", {})
        return p or _404("project")

    @app.delete("/api/projects/{pid}")
    async def project_delete(pid: int):
        if not store.delete_project(pid):
            return _404("project")
        await bus.broadcast("projects.changed", {})
        return {"ok": True}

    async def _attach_folder(pid: int, path: str):
        """Track a folder on a project: the folder itself + every git repo inside."""
        root = Path(path).expanduser().resolve()
        if not root.is_dir():
            return JSONResponse({"error": f"not a directory: {path}"}, status_code=422)
        from ..projects import scan
        existing = set(store.project_repo_paths(pid))
        added = []
        if str(root) not in existing:
            added.append(store.add_repo(pid, str(root),
                                        is_primary=not existing))
            existing.add(str(root))
        for rp in scan.discover_repos(str(root)):
            if rp not in existing:
                added.append(store.add_repo(pid, rp))
                existing.add(rp)
        return {"added": added, "discovered": max(0, len(added) - 1)}

    @app.post("/api/projects/{pid}/repos")
    async def repos_add(pid: int, body: dict):
        if not store.get_project(pid):
            return _404("project")
        path = (body.get("path") or "").strip()
        if not path:
            return JSONResponse({"error": "path required"}, status_code=422)
        r = await _attach_folder(pid, path)
        await bus.broadcast("projects.changed", {})
        return r

    @app.delete("/api/projects/{pid}/repos/{rid}")
    async def repos_remove(pid: int, rid: int):
        if not store.remove_repo(pid, rid):
            return _404("repo")
        await bus.broadcast("projects.changed", {})
        return {"ok": True}

    # =================================================================
    # ROOMS — the owner's channels
    # =================================================================
    @app.get("/api/rooms")
    def rooms_list():
        return store.list_rooms()

    @app.post("/api/rooms")
    async def rooms_create(body: dict):
        name = (body.get("name") or "").strip()
        if not name:
            return JSONResponse({"error": "name required"}, status_code=422)
        r = store.create_room(name)
        # a room named like an inventory project connects to it automatically
        import difflib
        projs = store.list_projects()
        by_name = {p["name"].lower(): p for p in projs}
        by_slug = {p["slug"]: p for p in projs}
        cand = by_slug.get(store.slugify(name)) or by_name.get(name.lower())
        if not cand:
            close = difflib.get_close_matches(name.lower(), list(by_name), n=1, cutoff=0.75)
            cand = by_name[close[0]] if close else None
        connected = []
        if cand:
            store.connect_project(r["id"], cand["id"])
            connected.append(cand["name"])
            await bus.broadcast("room.projects", {"room_id": r["id"]})
        await bus.broadcast("room.created", r)
        return {**r, "connected": connected}

    @app.patch("/api/rooms/{rid}")
    async def room_rename(rid: int, body: dict):
        r = store.rename_room(rid, body.get("name", ""))
        if r:
            await bus.broadcast("room.updated", r)
        return r or _404("room")

    @app.delete("/api/rooms/{rid}")
    async def room_delete(rid: int):
        r = store.get_room(rid)
        if r and r["slug"] == store.HOME_SLUG:
            return JSONResponse({"error": "the Home workroom can't be deleted"}, status_code=422)
        if not store.delete_room(rid):
            return _404("room")
        await bus.broadcast("room.deleted", {"id": rid})
        return {"ok": True}

    # ---- room ↔ project connections ----
    @app.get("/api/rooms/{rid}/projects")
    def room_projects(rid: int):
        out = store.projects_for_room(rid)
        for p in out:
            for row in p["repos"]:
                g = Path(row["path"]) / ".git"
                row["is_git"] = g.is_dir() or g.is_file()
        return out

    @app.post("/api/rooms/{rid}/projects")
    async def room_connect(rid: int, body: dict):
        if not store.get_room(rid):
            return _404("room")
        if not store.connect_project(rid, int(body.get("project_id") or 0)):
            return _404("project")
        await bus.broadcast("room.projects", {"room_id": rid})
        return {"ok": True}

    @app.delete("/api/rooms/{rid}/projects/{pid}")
    async def room_disconnect(rid: int, pid: int):
        if not store.disconnect_project(rid, pid):
            return _404("connection")
        await bus.broadcast("room.projects", {"room_id": rid})
        return {"ok": True}

    # ---- tasks (kanban — lives in rooms) ----
    @app.get("/api/tasks")
    def tasks_all():
        return store.all_tasks()

    @app.get("/api/rooms/{rid}/tasks")
    def tasks_list(rid: int):
        return store.list_tasks(rid)

    @app.post("/api/rooms/{rid}/tasks")
    async def tasks_create(rid: int, body: dict):
        if not store.get_room(rid):
            return _404("room")
        title = (body.get("title") or "").strip()
        if not title:
            return JSONResponse({"error": "title required"}, status_code=422)
        t = store.create_task(rid, title, body.get("body", ""))
        await bus.broadcast("task.created", t)
        return t

    @app.get("/api/tasks/{tid}/log")
    def task_log(tid: int):
        t = store.get_task(tid)
        if not t:
            return _404("task")
        r = store.get_room(t["room_id"])
        return {"task": t, "room": {"name": r["name"], "slug": r["slug"]} if r else None,
                "log": store.list_task_log(tid), "thread": store.list_thread(tid)}

    @app.post("/api/tasks/{tid}/reply")
    async def task_reply(tid: int, body: dict):
        t = store.get_task(tid)
        if not t:
            return _404("task")
        text = (body.get("text") or "").strip()
        if not text:
            return JSONResponse({"error": "text required"}, status_code=422)
        if t["status"] == "in_progress":
            return JSONResponse({"error": "still working — wait for it to finish"},
                                status_code=409)
        msg = store.add_thread(tid, "user", text)
        await bus.broadcast("task.thread", msg)
        t2 = store.set_task_status(tid, "in_progress")
        if t2:
            await bus.broadcast("task.updated", t2)
        worker.spawn_followup(t, text, bus.broadcast)
        return {"ok": True, "message": msg}

    @app.post("/api/tasks/{tid}/stop")
    async def task_stop(tid: int):
        t = store.get_task(tid)
        if not t:
            return _404("task")
        if not worker.cancel_task(tid) and t["status"] == "in_progress":
            # not in this process's registry (orphan from a restart) — just park it
            t2 = store.set_task_status(tid, "review", result="(stopped)")
            if t2:
                await bus.broadcast("task.updated", t2)
        return {"ok": True}

    @app.patch("/api/tasks/{tid}")
    async def task_update(tid: int, body: dict):
        status = body.get("status")
        if status not in store.STATUSES:
            return JSONResponse({"error": f"status must be one of {store.STATUSES}"},
                                status_code=422)
        t = store.set_task_status(tid, status, body.get("result"))
        if not t:
            return _404("task")
        await bus.broadcast("task.updated", t)
        return t

    # ---- routines (rooms) ----
    @app.get("/api/rooms/{rid}/routines")
    def routines_list(rid: int):
        return store.list_routines(rid)

    @app.post("/api/rooms/{rid}/routines")
    async def routines_add(rid: int, body: dict):
        if not store.get_room(rid):
            return _404("room")
        title = (body.get("title") or "").strip()
        schedule = (body.get("schedule") or "").strip()
        if not title or not re.match(r"^(daily@\d{1,2}:\d{2}|every@\d+[mh])$", schedule):
            return JSONResponse(
                {"error": "need title + schedule like daily@09:00 or every@4h"}, status_code=422)
        return store.add_routine(rid, title, body.get("body", ""), schedule)

    @app.patch("/api/routines/{rtid}")
    def routines_toggle(rtid: int, body: dict):
        r = store.toggle_routine(rtid, bool(body.get("enabled")))
        return r or _404("routine")

    @app.delete("/api/routines/{rtid}")
    def routines_delete(rtid: int):
        return {"ok": True} if store.delete_routine(rtid) else _404("routine")

    # ---- palace search ----
    @app.get("/api/search")
    def palace_search(q: str = ""):
        q = q.strip()
        if len(q) < 2:
            return {"rooms": [], "projects": [], "tasks": [], "chats": []}
        return store.search(q)

    # ---- home (the hall) ----
    @app.get("/api/home/chat")
    async def home_chat_list():
        from ..projects import brief
        row = brief.ensure_daily_brief()
        if row:
            await bus.broadcast("home.message", row)
        return store.list_home_chat()

    @app.post("/api/home/chat")
    async def home_chat_post(body: dict):
        text = (body.get("text") or "").strip()
        if not text:
            return JSONResponse({"error": "text required"}, status_code=422)
        msg = store.add_home_chat("user", text)
        await bus.broadcast("home.message", msg)
        asyncio.get_running_loop().create_task(home.handle(text, bus.broadcast))
        return {"message": msg}

    # ---- room chat: triage → card / conversation ----
    @app.get("/api/rooms/{rid}/chat")
    def chat_list(rid: int):
        return store.list_chat(rid)

    @app.post("/api/rooms/{rid}/chat")
    async def chat_post(rid: int, body: dict):
        if not store.get_room(rid):
            return _404("room")
        text = (body.get("text") or "").strip()
        if not text:
            return JSONResponse({"error": "text required"}, status_code=422)

        m = re.match(r"(?i)^close\s+(?:card|task|ticket)?\s*#?(\d+)$", text)
        if m:
            tid = int(m.group(1))
            umsg = store.add_chat(rid, "user", text)
            await bus.broadcast("chat.message", umsg)
            t = store.get_task(tid)
            if t and t["room_id"] == rid:
                t = store.set_task_status(tid, "done")
                reply = f"Closed card #{tid} — {t['title']}"
                await bus.broadcast("task.updated", t)
            else:
                reply = f"No card #{tid} in this room."
            amsg = store.add_chat(rid, "agent", reply, task_id=tid if t else None)
            await bus.broadcast("chat.message", amsg)
            return {"message": umsg, "task": None}

        # projects mentioned in the message connect themselves to the room
        r = store.get_room(rid)
        if r and r["slug"] != store.HOME_SLUG:
            hits = store.match_projects_in_text(text, exclude_room=rid)[:3]
            if hits:
                for p in hits:
                    store.connect_project(rid, p["id"])
                await bus.broadcast("room.projects", {"room_id": rid})
                note = store.add_chat(
                    rid, "agent",
                    "🔗 Connected project" + ("s" if len(hits) > 1 else "")
                    + " to this room: " + ", ".join(p["name"] for p in hits))
                await bus.broadcast("chat.message", note)

        lane = body.get("lane") or "auto"
        if lane == "auto":
            lane = await triage.classify(text)

        if lane == "chat":
            msg = store.add_chat(rid, "user", text)
            await bus.broadcast("chat.message", msg)
            asyncio.get_running_loop().create_task(
                worker.run_chat(rid, text, bus.broadcast))
            return {"message": msg, "task": None, "lane": "chat"}

        kind = "goal" if lane == "goal" else "task"
        task = store.create_task(rid, text.splitlines()[0][:120], text, kind=kind,
                                 promise=worker.DEFAULT_PROMISE if kind == "goal" else None)
        msg = store.add_chat(rid, "user", text, task_id=task["id"])
        await bus.broadcast("chat.message", msg)
        await bus.broadcast("task.created", task)
        return {"message": msg, "task": task, "lane": kind}

    # ---- assets (rooms) ----
    @app.get("/api/rooms/{rid}/assets")
    def assets_list(rid: int):
        return store.list_assets(rid)

    @app.post("/api/home/upload")
    async def home_upload(file: UploadFile):
        """Attachments sent from the hall land in the Home workroom's shelf."""
        room = store.ensure_home_room()
        return await assets_upload(room["id"], file)

    @app.post("/api/rooms/{rid}/assets")
    async def assets_upload(rid: int, file: UploadFile):
        r = store.get_room(rid)
        if not r:
            return _404("room")
        adir = store.room_dir(r["slug"]) / "assets"
        adir.mkdir(parents=True, exist_ok=True)
        base = Path(file.filename or "upload").name.replace("/", "_") or "upload"
        dest, n = adir / base, 2
        while dest.exists():
            dest = adir / f"{Path(base).stem}-{n}{Path(base).suffix}"
            n += 1
        size = 0
        with dest.open("wb") as out:
            while chunk := await file.read(1 << 20):
                out.write(chunk)
                size += len(chunk)
        a = store.add_asset(rid, dest.name, str(dest), size)
        await bus.broadcast("assets.changed", {"room_id": rid})
        return a

    @app.get("/api/assets/{aid}/download")
    def asset_download(aid: int):
        a = store.get_asset(aid)
        if not a or not Path(a["path"]).is_file():
            return _404("asset")
        return FileResponse(a["path"], filename=a["filename"])

    @app.delete("/api/rooms/{rid}/assets/{aid}")
    async def asset_delete(rid: int, aid: int):
        a = store.delete_asset(rid, aid)
        if not a:
            return _404("asset")
        try:
            Path(a["path"]).unlink(missing_ok=True)
        except OSError:
            pass
        await bus.broadcast("assets.changed", {"room_id": rid})
        return {"ok": True}

    # ---- live event bus ----
    @app.websocket("/ws")
    async def ws(sock: WebSocket):
        await sock.accept()
        bus.clients.add(sock)
        try:
            while True:
                await sock.receive_text()
        except WebSocketDisconnect:
            pass
        finally:
            bus.clients.discard(sock)

    # ---- the UI ----
    dist = Path(__file__).resolve().parent.parent / "web_dist"
    if (dist / "index.html").exists():
        app.mount("/", StaticFiles(directory=dist, html=True), name="ui")
    else:
        @app.get("/", response_class=HTMLResponse)
        def placeholder():
            return ("<html><body style='font-family:system-ui;padding:3em'>"
                    "<h2>🧠 mindpalace</h2><p>web gateway is up. The GUI ships in P2 — "
                    "meanwhile the API lives at <code>/api/…</code> and the event bus at "
                    "<code>/ws</code>.</p></body></html>")

    return app


def run(port: int | None = None, open_browser: bool = True, dev: bool = False):
    _require_fastapi()
    import uvicorn
    config.ensure_dirs()
    port = port or int(config.load_config().get("web", {}).get("port", DEFAULT_PORT))
    url = f"http://127.0.0.1:{port}"
    print(f"[web] mindpalace GUI at {url}  (Ctrl-C to stop)")
    if open_browser:
        import threading
        import webbrowser
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    # localhost only — never expose the daemon to the network unauthenticated
    if dev:
        uvicorn.run("mindpalace.gateways.web:create_app", factory=True,
                    host="127.0.0.1", port=port, log_level="info",
                    reload=True, reload_dirs=[str(config.PKG_ROOT)])
    else:
        uvicorn.run(create_app(), host="127.0.0.1", port=port, log_level="warning")
