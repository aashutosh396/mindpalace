"""Web gateway — the v3 GUI's backend. Third gateway beside Discord/WhatsApp.

Serves three things on one localhost port:
  • REST   /api/…   projects, tasks (kanban), chat, repos
  • WS     /ws      live event bus — every mutation broadcasts, so the board and
                    chat update in real time in every open window
  • static /        the pre-built Nuxt bundle (web_dist/, shipped as package data);
                    a plain status page until the first UI build lands

Run:  mindpalace serve [--port N]     (default 7777, localhost only)
The desktop app (Tauri) spawns this same gateway as its sidecar — the webview is
just another client of it. API-first: nothing here talks to the brain directly,
everything goes through the Provider interface.
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


# ---- WS event bus: every mutation → broadcast to all connected windows ----
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

    @asynccontextmanager
    async def lifespan(app):
        wtask = asyncio.create_task(worker.watch_loop(bus.broadcast))
        yield
        wtask.cancel()

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

    # ---- dev-channel updates (rolling build of the v3 branch) ----
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

    # ---- projects ----
    @app.get("/api/projects")
    def projects_list():
        return store.list_projects()

    @app.post("/api/projects")
    async def projects_create(body: dict):
        name = (body.get("name") or "").strip()
        if not name:
            return JSONResponse({"error": "name required"}, status_code=422)
        p = store.create_project(name)
        await bus.broadcast("project.created", p)
        return p

    @app.get("/api/projects/{pid}")
    def project_get(pid: int):
        p = store.get_project(pid)
        return p or _404("project")

    @app.patch("/api/projects/{pid}")
    async def project_rename(pid: int, body: dict):
        p = store.rename_project(pid, body.get("name", ""))
        if p:
            await bus.broadcast("project.updated", p)
        return p or _404("project")

    @app.delete("/api/projects/{pid}")
    async def project_delete(pid: int):
        if not store.delete_project(pid):
            return _404("project")
        await bus.broadcast("project.deleted", {"id": pid})
        return {"ok": True}

    # ---- repos ----
    @app.get("/api/repos")
    def repos_all():
        return store.all_repos()

    @app.get("/api/projects/{pid}/repos")
    def repos_list(pid: int):
        return store.repos_for(pid)

    @app.delete("/api/projects/{pid}/repos/{rid}")
    async def repos_remove(pid: int, rid: int):
        # own repo → remove it (links elsewhere die with it); linked → just unlink
        if not (store.remove_repo(pid, rid) or store.unlink_repo(pid, rid)):
            return _404("repo")
        await bus.broadcast("repos.changed", {"project_id": pid})
        return {"ok": True}

    @app.post("/api/projects/{pid}/repos")
    async def repos_add(pid: int, body: dict):
        if not store.get_project(pid):
            return _404("project")
        if body.get("link_repo_id"):              # reference another project's repo
            if not store.link_repo(pid, int(body["link_repo_id"])):
                return _404("repo")
            r = {"linked": True, "repo_id": int(body["link_repo_id"])}
        else:
            path = (body.get("path") or "").strip()
            if not path:
                return JSONResponse({"error": "path required"}, status_code=422)
            root = Path(path).expanduser().resolve()
            if not root.is_dir():
                return JSONResponse({"error": f"not a directory: {path}"}, status_code=422)
            # the FOLDER is the project root (agent's cwd); every git repo
            # nested inside is tracked with it
            from ..projects import scan
            existing = set(store.repo_paths_for(pid))
            added = []
            if str(root) not in existing:
                added.append(store.add_repo(pid, str(root), body.get("url"),
                                            bool(body.get("is_primary"))))
                existing.add(str(root))
            for rp in scan.discover_repos(str(root)):
                if rp not in existing:
                    added.append(store.add_repo(pid, rp))
                    existing.add(rp)
            r = {"added": added, "discovered": max(0, len(added) - 1)}
        await bus.broadcast("repos.changed", {"project_id": pid})
        return r

    # ---- tasks (kanban) ----
    @app.get("/api/tasks")
    def tasks_all():
        return store.all_tasks()

    @app.get("/api/projects/{pid}/tasks")
    def tasks_list(pid: int):
        return store.list_tasks(pid)

    @app.post("/api/projects/{pid}/tasks")
    async def tasks_create(pid: int, body: dict):
        if not store.get_project(pid):
            return _404("project")
        title = (body.get("title") or "").strip()
        if not title:
            return JSONResponse({"error": "title required"}, status_code=422)
        t = store.create_task(pid, title, body.get("body", ""))
        await bus.broadcast("task.created", t)
        return t

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

    # ---- home (the hall): one chat that routes to every room ----
    @app.get("/api/home/chat")
    def home_chat_list():
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

    # ---- chat: an instruction typed here becomes a ticket on the board ----
    @app.get("/api/projects/{pid}/chat")
    def chat_list(pid: int):
        return store.list_chat(pid)

    @app.post("/api/projects/{pid}/chat")
    async def chat_post(pid: int, body: dict):
        if not store.get_project(pid):
            return _404("project")
        text = (body.get("text") or "").strip()
        if not text:
            return JSONResponse({"error": "text required"}, status_code=422)

        # "close card 12" / "close task #12" → close it, don't open a new ticket
        m = re.match(r"(?i)^close\s+(?:card|task|ticket)?\s*#?(\d+)$", text)
        if m:
            tid = int(m.group(1))
            umsg = store.add_chat(pid, "user", text)
            await bus.broadcast("chat.message", umsg)
            t = store.get_task(tid)
            if t and t["project_id"] == pid:
                t = store.set_task_status(tid, "done")
                reply = f"Closed card #{tid} — {t['title']}"
                await bus.broadcast("task.updated", t)
            else:
                reply = f"No card #{tid} in this room."
            amsg = store.add_chat(pid, "agent", reply, task_id=tid if t else None)
            await bus.broadcast("chat.message", amsg)
            return {"message": umsg, "task": None}

        # triage: work → card; conversation → answer in the corridor, no card.
        # The UI can force a lane; default is auto (heuristics, then haiku).
        lane = body.get("lane") or "auto"
        if lane == "auto":
            lane = await triage.classify(text)

        if lane == "chat":
            msg = store.add_chat(pid, "user", text)
            await bus.broadcast("chat.message", msg)
            asyncio.get_running_loop().create_task(
                worker.run_chat(pid, text, bus.broadcast))
            return {"message": msg, "task": None, "lane": "chat"}

        task = store.create_task(pid, text.splitlines()[0][:120], text)
        msg = store.add_chat(pid, "user", text, task_id=task["id"])
        await bus.broadcast("chat.message", msg)
        await bus.broadcast("task.created", task)
        # the ticket worker (projects/worker.py) claims it from 'todo' within ~2s
        return {"message": msg, "task": task, "lane": "task"}

    # ---- assets ----
    @app.get("/api/projects/{pid}/assets")
    def assets_list(pid: int):
        return store.list_assets(pid)

    @app.post("/api/projects/{pid}/assets")
    async def assets_upload(pid: int, file: UploadFile):
        p = store.get_project(pid)
        if not p:
            return _404("project")
        adir = store.project_dir(p["slug"]) / "assets"
        adir.mkdir(parents=True, exist_ok=True)
        # sanitize to a plain basename; dedupe collisions with -2, -3, …
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
        a = store.add_asset(pid, dest.name, str(dest), size)
        await bus.broadcast("assets.changed", {"project_id": pid})
        return a

    @app.get("/api/assets/{aid}/download")
    def asset_download(aid: int):
        a = store.get_asset(aid)
        if not a or not Path(a["path"]).is_file():
            return _404("asset")
        return FileResponse(a["path"], filename=a["filename"])

    @app.delete("/api/projects/{pid}/assets/{aid}")
    async def asset_delete(pid: int, aid: int):
        a = store.delete_asset(pid, aid)
        if not a:
            return _404("asset")
        try:
            Path(a["path"]).unlink(missing_ok=True)
        except OSError:
            pass
        await bus.broadcast("assets.changed", {"project_id": pid})
        return {"ok": True}

    # ---- live event bus ----
    @app.websocket("/ws")
    async def ws(sock: WebSocket):
        await sock.accept()
        bus.clients.add(sock)
        try:
            while True:                            # inbound frames are just keepalives
                await sock.receive_text()
        except WebSocketDisconnect:
            pass
        finally:
            bus.clients.discard(sock)

    # ---- the UI: pre-built Nuxt bundle when present, status page until then ----
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
        # auto-restart on python edits; pair with `cd web && npm run dev` for UI HMR
        uvicorn.run("mindpalace.gateways.web:create_app", factory=True,
                    host="127.0.0.1", port=port, log_level="info",
                    reload=True, reload_dirs=[str(config.PKG_ROOT)])
    else:
        uvicorn.run(create_app(), host="127.0.0.1", port=port, log_level="warning")
