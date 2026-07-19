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
  current: null as Project | null,
  tasks: [] as Task[],
  chat: [] as ChatMsg[],
  repos: { own: [] as any[], linked: [] as any[] },
  assets: [] as any[],
  arrived: new Set<number>(),      // task ids that just appeared (for the arrive animation)
  toast: '' as string,
  toastError: false,
  connected: false
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

function toast(msg: string, error = false) {
  state.toast = msg
  state.toastError = error
  setTimeout(() => { if (state.toast === msg) state.toast = '' }, 3200)
}

// ---- WS bus: server broadcasts every mutation; we fold them into state ----
let ws: WebSocket | null = null
function connect() {
  const proto = location.protocol === 'https:' ? 'wss' : 'ws'
  ws = new WebSocket(`${proto}://${location.host}/ws`)
  ws.onopen = () => { state.connected = true }
  ws.onclose = () => { state.connected = false; setTimeout(connect, 2000) }
  ws.onmessage = (e) => {
    const { event, data } = JSON.parse(e.data)
    if (event === 'project.created' && !state.projects.find(p => p.id === data.id)) {
      state.projects.unshift(data)
    } else if (event === 'project.deleted') {
      state.projects = state.projects.filter(p => p.id !== data.id)
      if (state.current?.id === data.id) state.current = null
    } else if (event === 'task.created' && data.project_id === state.current?.id) {
      if (!state.tasks.find(t => t.id === data.id)) {
        state.tasks.push(data)
        state.arrived.add(data.id)
        setTimeout(() => state.arrived.delete(data.id), 600)
      }
    } else if (event === 'task.updated') {
      const i = state.tasks.findIndex(t => t.id === data.id)
      if (i >= 0) state.tasks[i] = data
    } else if (event === 'chat.message' && data.project_id === state.current?.id) {
      if (!state.chat.find(m => m.id === data.id)) state.chat.push(data)
    }
  }
}

const actions = {
  async init() {
    connect()
    state.projects = await api('/projects')
    if (state.projects.length && !state.current) await actions.open(state.projects[0])
  },
  async open(p: Project) {
    state.current = p
    const [tasks, chat, repos, assets] = await Promise.all([
      api(`/projects/${p.id}/tasks`), api(`/projects/${p.id}/chat`),
      api(`/projects/${p.id}/repos`), api(`/projects/${p.id}/assets`)
    ])
    state.tasks = tasks; state.chat = chat; state.repos = repos; state.assets = assets
  },
  async createProject(name: string) {
    try {
      const p = await api('/projects', { method: 'POST', body: JSON.stringify({ name }) })
      if (!state.projects.find(x => x.id === p.id)) state.projects.unshift(p)
      await actions.open(p)
    } catch (e: any) { toast(e.message, true) }
  },
  async sendChat(text: string) {
    if (!state.current) return
    try {
      const r = await api(`/projects/${state.current.id}/chat`, {
        method: 'POST', body: JSON.stringify({ text })
      })
      if (!state.chat.find(m => m.id === r.message.id)) state.chat.push(r.message)
      toast(`Card #${r.task.id} added to the board`)
    } catch (e: any) { toast(e.message, true) }
  },
  async moveTask(id: number, status: Status) {
    const t = state.tasks.find(t => t.id === id)
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
      await api(`/projects/${state.current.id}/repos`, {
        method: 'POST', body: JSON.stringify({ path, is_primary: isPrimary })
      })
      state.repos = await api(`/projects/${state.current.id}/repos`)
      toast('Repo attached')
    } catch (e: any) { toast(e.message, true) }
  },
  toast
}

export function useWorkspace() {
  return { state, ...actions }
}
