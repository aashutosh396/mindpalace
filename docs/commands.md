# Commands

## CLI
| Command | Description |
|---|---|
| `mindpalace` | Start (first run = setup; then terminal + bg daemon) |
| `mindpalace setup` | Re-run onboarding |
| `mindpalace gateway terminal\|discord` | Configure / switch interface |
| `mindpalace daemon` | Run the background daemon in the foreground (systemd/launchd) |
| `mindpalace start` / `stop` | Detached background daemon control |
| `mindpalace service install\|uninstall\|status` | Reboot-persistent OS service |
| `mindpalace add-bot` / `bots` | Scoped bots |
| `mindpalace admins` / `add-admin <id>` / `remove-admin <id>` | Admin management |
| `mindpalace add-webhook <name> <url>` | Save a channel webhook |
| `mindpalace notify "msg" [--channel name]` | Post to a channel |
| `mindpalace heartbeat <minutes>` | Autonomous self-tick interval (0 = off) |
| `mindpalace status` / `version` | Info |

## Discord (home channel, admins)
`!help` · `!admins` · `!add-admin @user` · `!remove-admin @user` · `!bots` · `!add-webhook <name> <url>`

## Terminal chat
`/help` · `/status` · `/exit`
