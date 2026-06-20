"""
WhatsApp gateway — same brain as Discord/terminal, reached over WhatsApp Cloud API (Meta).

Meta PUSHES messages to a webhook, so this runs an HTTP server (stdlib only — no extra deps):
  GET  /webhook   → verification handshake (hub.challenge)
  POST /webhook   → incoming messages; we 200 INSTANTLY (Meta retries on slow/:( responses),
                    then process in a background thread: run the brain, send the reply back.

Free for personal use: replies inside the 24-hour service window aren't billed by Meta.
Owner-locked: only allowed numbers are answered (first sender is adopted if none configured).

Run on a box with a public HTTPS URL (your VPS):  mindpalace whatsapp
Point Meta's webhook at  https://<your-host>/webhook  with the same verify token.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from .. import config
from ..core import brain
from ..memory import store as mem

GRAPH = "https://graph.facebook.com/v21.0"
KEEP = 24
_seen: set[str] = set()          # processed message ids — dedup Meta's retries
_seen_lock = threading.Lock()


# ---- per-sender history (mirrors the terminal/discord stores) ----
def _hist_path(num: str):
    return config.state_dir() / "whatsapp" / f"{num}.json"


def _load(num: str) -> list:
    try:
        return json.loads(_hist_path(num).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save(num: str, h: list) -> None:
    p = _hist_path(num)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(h[-KEEP:], indent=2))


# ---- WhatsApp Cloud API calls ----
def _api(payload: dict) -> None:
    """POST to the messages endpoint (send text / mark read). Best-effort; never raises."""
    pid, tok = config.whatsapp_phone_id(), config.whatsapp_token()
    if not (pid and tok):
        return
    req = urllib.request.Request(
        f"{GRAPH}/{pid}/messages",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"},
        method="POST")
    try:
        urllib.request.urlopen(req, timeout=30).read()
    except Exception as e:
        print(f"[whatsapp] send failed: {e}")


def _chunks(s: str, n: int = 3900):
    return [s[i:i + n] for i in range(0, len(s), n)] or ["(empty)"]


def send(to: str, text: str) -> None:
    for c in _chunks(text):
        _api({"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": c}})


def _mark_read(message_id: str) -> None:
    _api({"messaging_product": "whatsapp", "status": "read", "message_id": message_id})


# ---- signature check (X-Hub-Signature-256, HMAC-SHA256 of the raw body) ----
def _valid_sig(raw: bytes, header: str | None) -> bool:
    secret = config.whatsapp_app_secret()
    if not secret:                                # no app secret configured → skip the check
        return True
    if not header or not header.startswith("sha256="):
        return False
    digest = hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, header.split("=", 1)[1])


# ---- one incoming message → brain → reply (runs in a background thread) ----
def _process(frm: str, text: str, msg_id: str) -> None:
    try:
        _mark_read(msg_id)
        # owner-lock: adopt the first sender if no allow-list yet, else enforce it
        if not config.whatsapp_allowed():
            config.whatsapp_allow(frm)
            print(f"[whatsapp] adopted owner: {frm}")
        elif not config.whatsapp_is_allowed(frm):
            print(f"[whatsapp] ignoring non-owner {frm}")
            return
        history = _load(frm)
        reply = brain.ask_sync(text, history)
        send(frm, reply)
        history += [{"role": "Owner", "content": text}, {"role": "Assistant", "content": reply}]
        _save(frm, history)
        mem.save_exchange(text, reply)
    except Exception as e:
        print(f"[whatsapp] process error: {e}")
        try:
            send(frm, f"(hit an error: {str(e)[:160]})")
        except Exception:
            pass


def _handle_event(body: dict) -> None:
    for entry in body.get("entry", []):
        for change in entry.get("changes", []):
            for msg in change.get("value", {}).get("messages", []):
                if msg.get("type") != "text":
                    continue
                mid = msg.get("id", "")
                with _seen_lock:
                    if mid in _seen:
                        continue
                    _seen.add(mid)
                    if len(_seen) > 2000:        # bound the dedup set
                        _seen.clear(); _seen.add(mid)
                frm = msg.get("from", "")
                text = (msg.get("text", {}) or {}).get("body", "").strip()
                if frm and text:
                    threading.Thread(target=_process, args=(frm, text, mid), daemon=True).start()


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):                   # quiet — we print our own lines
        pass

    def _ok(self, code=200, body=b"OK"):
        self.send_response(code)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        mode = (q.get("hub.mode") or [""])[0]
        token = (q.get("hub.verify_token") or [""])[0]
        challenge = (q.get("hub.challenge") or [""])[0]
        if mode == "subscribe" and token == config.whatsapp_verify_token():
            self._ok(200, challenge.encode())    # echo the challenge → verified
        else:
            self._ok(403, b"forbidden")

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        if not _valid_sig(raw, self.headers.get("X-Hub-Signature-256")):
            self._ok(403, b"bad signature"); return
        self._ok(200, b"EVENT_RECEIVED")         # ACK FAST — then work (Meta retries on delay)
        try:
            _handle_event(json.loads(raw or b"{}"))
        except Exception as e:
            print(f"[whatsapp] event parse error: {e}")


def run():
    if not config.whatsapp_configured():
        raise SystemExit("WhatsApp not configured — run `mindpalace whatsapp setup` first.")
    config.ensure_dirs()
    port = config.whatsapp_port()
    srv = ThreadingHTTPServer(("0.0.0.0", port), _Handler)
    print(f"[whatsapp] webhook listening on :{port}  (point Meta at https://<host>/webhook)")
    print(f"[whatsapp] verify token: {config.whatsapp_verify_token()}  ·  "
          f"allowed: {config.whatsapp_allowed() or '(first sender adopts)'}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()
