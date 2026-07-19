// One shared reactive workspace: projects, the open project's board/chat/repos/
// assets, and the live WS bus that keeps every open window in sync.
import { reactive, readonly } from 'vue'

export const STATUSES = ['todo', 'in_progress', 'review', 'done'] as const
export type Status = typeof STATUSES[number]

export interface Project { id: number; slug: string; name: string; open_tasks?: number }
export interface Task {
  id: number; project_id: number; title: string; body: string
  status: Status; created_by: string; result: string; created_at: number
}
export interface ChatMsg { id: number; project_id: number; role: string; text: string; task_id: number | null }

const state = reactive({
  projects: [] as Project[],
  current: null as Project | null,   // null = the Home hall
  tasks: [] as Task[],
  allTasks: [] as any[],             // cross-room cards for the Home board
  chat: [] as ChatMsg[],
  homeChat: [] as any[],
  repos: { own: [] as any[], linked: [] as any[] },
  allRepos: [] as any[],           // every repo in the palace, for the link picker
  assets: [] as any[],
  arrived: new Set<number>(),      // task ids that just appeared (for the arrive animation)
  progress: {} as Record<number, string>,   // live step line per working card
  awaitingReply: false,            // chat-lane message sent, agent still writing
  toast: '' as string,
  toastError: false,
  connected: false,
  boardOpen: false,                // the board sheet (⛶) is expanded
  health: null as null | { version: string; commit: string; provider: string; provider_ok: boolean; provider_status: string },
  update: null as null | { behind: boolean; local: string; remote: string; installer: string | null },
  updating: false
})

async function api(path: string, opts: RequestInit = {}) {
  const res = await fetch(`/api${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...opts
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.error || `${res.status} on ${path}`)
  return data
}

function syncCount() {
  // keep the sidebar badge honest for the open room
  const row = state.projects.find(p => p.id === state.current?.id)
  if (row) row.open_tasks = state.tasks.filter(t => t.status !== 'done').length
}

function toast(msg: string, error = false) {
  state.toast = msg
  state.toastError = error
  setTimeout(() => { if (state.toast === msg) state.toast = '' }, 3200)
}

// ---- WS bus: server broadcasts every mutation; we fold them into state ----
let ws: WebSocket | null = null
function connect() {
  const proto = location.protocol === 'https:' ? 'wss' : 'ws'
  // dev: the nitro proxy doesn't upgrade websockets — talk to the daemon directly
  const host = import.meta.dev ? '127.0.0.1:7777' : location.host
  ws = new WebSocket(`${proto}://${host}/ws`)
  ws.onopen = async () => {
    state.connected = true
    // resync — anything broadcast while the socket was down is gone forever
    // (backend restarts in dev drop the connection constantly)
    try {
      state.projects = await api('/projects')
      if (state.current) {
        const p = state.projects.find(x => x.id === state.current!.id)
        if (p) await actions.open(p)
        else { state.current = null; state.tasks = []; state.chat = [] }
      }
    } catch { /* backend still coming up — next reconnect will sync */ }
  }
  ws.onclose = () => { state.connected = false; setTimeout(connect, 2000) }
  ws.onmessage = (e) => {
    const { event, data } = JSON.parse(e.data)
    if (event === 'project.created' && !state.projects.find(p => p.id === data.id)) {
      state.projects.unshift(data)
    } else if (event === 'project.deleted') {
      state.projects = state.projects.filter(p => p.id !== data.id)
      if (state.current?.id === data.id) state.current = null
    } else if (event === 'task.created') {
      if (!state.allTasks.find((t: any) => t.id === data.id)) {
        const room = state.projects.find(p => p.id === data.project_id)
        state.allTasks.push({ ...data, room_slug: room?.slug, room_name: room?.name })
      }
      if (data.project_id === state.current?.id) {
        if (!state.tasks.find(t => t.id === data.id)) {
          state.tasks.push(data)
          state.arrived.add(data.id)
          setTimeout(() => state.arrived.delete(data.id), 600)
        }
        syncCount()
      } else {
        const row = state.projects.find(p => p.id === data.project_id)
        if (row) row.open_tasks = (row.open_tasks || 0) + 1
      }
    } else if (event === 'task.updated') {
      const i = state.tasks.findIndex(t => t.id === data.id)
      if (i >= 0) state.tasks[i] = data
      const j = state.allTasks.findIndex((t: any) => t.id === data.id)
      if (j >= 0) state.allTasks[j] = { ...state.allTasks[j], ...data }
      if (data.status !== 'in_progress') delete state.progress[data.id]
      if (data.project_id === state.current?.id) syncCount()
      else api('/projects').then(ps => { state.projects = ps }).catch(() => {})
    } else if (event === 'task.progress') {
      state.progress[data.task_id] = data.text
    } else if (event === 'repos.changed' && data.project_id === state.current?.id) {
      api(`/projects/${data.project_id}/repos`).then(r => { state.repos = r })
    } else if (event === 'assets.changed' && data.project_id === state.current?.id) {
      api(`/projects/${data.project_id}/assets`).then(a => { state.assets = a })
    } else if (event === 'chat.message' && data.project_id === state.current?.id) {
      if (!state.chat.find(m => m.id === data.id)) state.chat.push(data)
      if (data.role === 'agent') state.awaitingReply = false
    } else if (event === 'home.message') {
      if (!state.homeChat.find((m: any) => m.id === data.id)) state.homeChat.push(data)
      if (data.role === 'agent' && !state.current) state.awaitingReply = false
    }
  }
}

const actions = {
  async init() {
    connect()
    actions.checkHealth()
    state.projects = await api('/projects')
    state.homeChat = await api('/home/chat')   // land in the hall
    state.allTasks = await api('/tasks')
  },
  async goHome() {
    state.current = null
    state.awaitingReply = false
    ;[state.homeChat, state.allTasks] = await Promise.all([api('/home/chat'), api('/tasks')])
  },
  async sendHomeChat(text: string) {
    try {
      const r = await api('/home/chat', { method: 'POST', body: JSON.stringify({ text }) })
      if (!state.homeChat.find((m: any) => m.id === r.message.id)) state.homeChat.push(r.message)
      state.awaitingReply = true
    } catch (e: any) { toast(e.message, true) }
  },
  async checkHealth() {
    try { state.health = await api('/health') } catch { /* banner just stays hidden */ }
    try { state.update = await api('/update/check') } catch { /* offline — button stays hidden */ }
  },
  async getUpdate() {
    state.updating = true
    try {
      state.update = await api('/update/check')     // always re-check on press
      if (!state.update.behind) {
        toast(`You're up to date (${state.update.local})`)
      } else {
        const r = await api('/update/apply', { method: 'POST' })
        if (r.ok) toast('Update downloaded — drag mindpalace to Applications, then relaunch')
        else toast(r.error || 'update failed', true)
      }
    } catch (e: any) { toast(e.message, true) }
    state.updating = false
  },
  async open(p: Project) {
    state.current = p
    const [tasks, chat, repos, assets] = await Promise.all([
      api(`/projects/${p.id}/tasks`), api(`/projects/${p.id}/chat`),
      api(`/projects/${p.id}/repos`), api(`/projects/${p.id}/assets`)
    ])
    state.tasks = tasks; state.chat = chat; state.repos = repos; state.assets = assets
  },
  async deleteProject(p: Project) {
    try {
      await api(`/projects/${p.id}`, { method: 'DELETE' })
      state.projects = state.projects.filter(x => x.id !== p.id)
      if (state.current?.id === p.id) {
        state.current = null
        state.tasks = []; state.chat = []; state.assets = []
        state.repos = { own: [], linked: [] }
        if (state.projects.length) await actions.open(state.projects[0])
      }
      toast(`Deleted "${p.name}"`)
    } catch (e: any) { toast(e.message, true) }
  },
  async createProject(name: string) {
    try {
      const p = await api('/projects', { method: 'POST', body: JSON.stringify({ name }) })
      if (!state.projects.find(x => x.id === p.id)) state.projects.unshift(p)
      await actions.open(p)
    } catch (e: any) { toast(e.message, true) }
  },
  async sendChat(text: string, lane: 'auto' | 'chat' | 'task' = 'auto') {
    if (!state.current) return
    try {
      const r = await api(`/projects/${state.current.id}/chat`, {
        method: 'POST', body: JSON.stringify({ text, lane })
      })
      if (!state.chat.find(m => m.id === r.message.id)) state.chat.push(r.message)
      if (r.task) toast(`Card #${r.task.id} added to the board`)
      else if (r.lane === 'chat') state.awaitingReply = true
    } catch (e: any) { toast(e.message, true) }
  },
  async moveTask(id: number, status: Status) {
    const t = state.tasks.find(t => t.id === id) || state.allTasks.find((t: any) => t.id === id)
    if (!t || t.status === status) return
    const prev = t.status
    t.status = status                              // optimistic; WS confirms
    try {
      await api(`/tasks/${id}`, { method: 'PATCH', body: JSON.stringify({ status }) })
    } catch (e: any) { t.status = prev; toast(e.message, true) }
  },
  async addRepo(path: string, isPrimary: boolean) {
    if (!state.current) return
    try {
      const r = await api(`/projects/${state.current.id}/repos`, {
        method: 'POST', body: JSON.stringify({ path, is_primary: isPrimary })
      })
      state.repos = await api(`/projects/${state.current.id}/repos`)
      toast(r.discovered > 0
        ? `Folder attached — found ${r.discovered} git repo${r.discovered > 1 ? 's' : ''} inside`
        : 'Folder attached')
    } catch (e: any) { toast(e.message, true) }
  },
  async linkRepo(repoId: number) {
    if (!state.current) return
    try {
      await api(`/projects/${state.current.id}/repos`, {
        method: 'POST', body: JSON.stringify({ link_repo_id: repoId })
      })
      state.repos = await api(`/projects/${state.current.id}/repos`)
      toast('Repo linked')
    } catch (e: any) { toast(e.message, true) }
  },
  async removeRepo(repoId: number) {
    if (!state.current) return
    try {
      await api(`/projects/${state.current.id}/repos/${repoId}`, { method: 'DELETE' })
      state.repos = await api(`/projects/${state.current.id}/repos`)
    } catch (e: any) { toast(e.message, true) }
  },
  async loadAllRepos() {
    try { state.allRepos = await api('/repos') } catch { /* picker just stays empty */ }
  },
  async uploadAssets(files: FileList | File[]) {
    if (!state.current) return
    for (const f of Array.from(files)) {
      const form = new FormData()
      form.append('file', f)
      try {
        const res = await fetch(`/api/projects/${state.current.id}/assets`, {
          method: 'POST', body: form
        })
        if (!res.ok) throw new Error((await res.json()).error || `upload failed (${res.status})`)
      } catch (e: any) { toast(e.message, true); return }
    }
    state.assets = await api(`/projects/${state.current.id}/assets`)
    toast(files.length > 1 ? `${files.length} files uploaded` : 'Uploaded')
  },
  async deleteAsset(aid: number) {
    if (!state.current) return
    try {
      await api(`/projects/${state.current.id}/assets/${aid}`, { method: 'DELETE' })
      state.assets = await api(`/projects/${state.current.id}/assets`)
    } catch (e: any) { toast(e.message, true) }
  },
  toast
}

export function useWorkspace() {
  return { state, ...actions }
}
