# mindpalace desktop

The customer-facing app: a Tauri (Rust) shell + the Nuxt GUI + the Python daemon
compiled into a standalone sidecar binary. Download, double-click, done — no
Python, no pip, no terminal. The only external requirement is the Claude CLI,
which the first-run banner walks the user through.

## How it fits together

```
mindpalace.app
 ├─ Tauri shell (Rust)     native window; spawns/kills the sidecar
 ├─ webview                loads http://127.0.0.1:7777 (the GUI)
 └─ mindpalaced sidecar    PyInstaller build of the daemon web gateway
                           (UI bundle + skills library packed inside)
```

If port 7777 is already served (a dev `mindpalace serve`), the shell reuses it
instead of spawning the sidecar.

## Build locally

```bash
# 1. sidecar (needs python + `pip install .[web] pyinstaller`)
cd desktop/sidecar && ./build.sh python3
mkdir -p ../src-tauri/binaries && cp dist/mindpalaced-* ../src-tauri/binaries/

# 2. app (needs rust + node)
cd .. && npm install && npx tauri build
# → src-tauri/target/release/bundle/{dmg,macos,deb,appimage,msi,nsis}
```

The web UI is NOT built here — `mindpalace/web_dist` is committed. To refresh it:
`cd web && npm run build:dist`.

## CI

`.github/workflows/desktop.yml` builds all four targets (mac arm/intel, linux,
windows) on `v3*` tags and attaches installers to a draft GitHub release.

## Signing

Unsigned for now (Gatekeeper: right-click → Open; Windows: SmartScreen "run
anyway"). Buy Apple Developer + a Windows cert when there are outside users.
