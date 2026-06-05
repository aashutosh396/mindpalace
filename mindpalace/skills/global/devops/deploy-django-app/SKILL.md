---
name: deploy-django-app
description: Deploy a Django app behind nginx using a gunicorn unix socket (wrapper-dir layout). Reference recipe — derive a per-host user skill from it.
tags: [deploy, django, nginx, gunicorn, systemd]
created: 2026-06-05
---

# Deploy a Django app (wrapper + unix socket)

> GLOBAL reference recipe. When you use this for a real host, draft a tailored
> user skill (`~/.mindpalace/skills/deploy-<project>.md`, `derived_from: deploy-django-app`)
> with the exact paths, Python version, and quirks you discover.

## Layout (one wrapper dir per project)
```
<project>/
├── run/            # gunicorn.sock (unix socket — not a TCP port)
├── .venv/          # virtualenv, SIBLING of the code (never inside the repo)
└── <repo>/         # manage.py + settings + .env
```

## Steps
1. Create wrapper + venv **at the final path** (never `mv` a venv — abs-path shebangs break):
   `python3 -m venv <project>/.venv && <project>/.venv/bin/pip install -r requirements.txt`
2. Place code in `<project>/<repo>/`, add `.env` (chmod 600).
3. `manage.py migrate && manage.py collectstatic --noinput`
4. systemd unit: `User=root Group=www-data`, gunicorn
   `--bind unix:<project>/run/gunicorn.sock --umask 007` → socket `0770 root:www-data`.
5. nginx: `proxy_pass http://unix:<project>/run/gunicorn.sock;` + static/media `location`s.
6. Restart + verify: `systemctl restart <svc>`; check `/` and `/admin/` return 200/302.

## Gotchas
- Old stacks pinning `grpcio==1.44`/`protobuf==3.19` have no cp311/cp312 wheels → use Python 3.10.
- 502 right after switching to a socket = graceful-reload drain window; re-test in ~1s.
- Block sensitive media (KYC/ID): nginx `location /media/<dir>/ { deny all; }`.
