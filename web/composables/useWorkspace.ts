// One shared reactive workspace, two layers:
//   ROOMS    the owner's channels — chat, board, assets, routines (state.current)
//   PROJECTS the inventory — folders/repos, inspected via the Projects sheet
// The live WS bus keeps every open window in sync.
import { reactive } from 'vue'

export const STATUSES = ['todo', 'in_progress', 'review', 'done'] as const
export type Status = typeof STATUSES[number]

export interface Room { id: number; slug: string; name: string; open_tasks?: number }
export interface Task {
  id: number; room_id: number; title: string; body: string
  status: Status; created_by: string; kind?: string; iterations?: number; result: string; created_at: number
}

const state = reactive({
  rooms: [] as Room[],
  current: null as Room | null,      // null = the Home hall
  projects: [] as any[],             // the inventory
  roomProjects: [] as any[],         // projects connected to the open room
  tasks: [] as Task[],
  allTasks: [] as any[],
  chat: [] as any[],
  homeChat: [] as any[],
  assets: [] as any[],
  arrived: new Set<number>(),
  progress: {} as Record<number, string>,
  awaitingReply: false,
  toast: '' as string,
  toastError: false,
  connected: false,
  boardOpen: false,
  projectsOpen: false,               // the Projects sheet
  modal: null as null | { task: any; room: any; log: any[]; thread: any[] },
  searchOpen: false,
  searchResults: null as null | { rooms: any[]; projects: any[]; tasks: any[]; chats: any[] },
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

function updateTitleBadge() {
  const n = state.allTasks.filter((t: any) => t.status === 'review').length
  document.title = (n ? `(${n}) ` : '') + 'mindpalace'
}

function syncCount() {
  const row = state.rooms.find(r => r.id === state.current?.id)
  if (row) row.open_tasks = state.tasks.filter(t => t.status !== 'done').length
}

function toast(msg: string, error = false) {
  state.toast = msg
  state.toastError = error
  setTimeout(() => { if (state.toast === msg) state.toast = '' }, 3200)
}

let ws: WebSocket | null = null
function connect() {
  const proto = location.protocol === 'https:' ? 'wss' : 'ws'
  const host = import.meta.dev ? '127.0.0.1:7777' : location.host
  ws = new WebSocket(`${proto}://${host}/ws`)
  ws.onopen = async () => {
    state.connected = true
    try {
      state.rooms = await api('/rooms')
      state.homeChat = await api('/home/chat')
      state.allTasks = await api('/tasks')
      updateTitleBadge()
      if (state.current) {
        const r = state.rooms.find(x => x.id === state.current!.id)
        if (r) await actions.open(r)
        else { state.current = null; state.tasks = []; state.chat = [] }
      } else {
        const last = state.homeChat[state.homeChat.length - 1]
        state.awaitingReply = !!last && last.role === 'user'
      }
    } catch { /* backend still coming up — next reconnect will sync */ }
  }
  ws.onclose = () => { state.connected = false; setTimeout(connect, 2000) }
  ws.onmessage = (e) => {
    const { event, data } = JSON.parse(e.data)
    if (event === 'room.created' && !state.rooms.find(r => r.id === data.id)) {
      state.rooms.unshift(data)
    } else if (event === 'room.deleted') {
      state.rooms = state.rooms.filter(r => r.id !== data.id)
      if (state.current?.id === data.id) state.current = null
    } else if (event === 'room.updated') {
      const i = state.rooms.findIndex(r => r.id === data.id)
      if (i >= 0) state.rooms[i] = { ...state.rooms[i], ...data }
    } else if (event === 'projects.changed') {
      api('/projects').then(ps => { state.projects = ps }).catch(() => {})
      if (state.current) {
        api(`/rooms/${state.current.id}/projects`).then(ps => { state.roomProjects = ps }).catch(() => {})
      }
    } else if (event === 'room.projects' && data.room_id === state.current?.id) {
      api(`/rooms/${data.room_id}/projects`).then(ps => { state.roomProjects = ps }).catch(() => {})
    } else if (event === 'task.created') {
      if (!state.allTasks.find((t: any) => t.id === data.id)) {
        const room = state.rooms.find(r => r.id === data.room_id)
        state.allTasks.push({ ...data, room_slug: room?.slug, room_name: room?.name || 'Home' })
      }
      if (data.room_id === state.current?.id) {
        if (!state.tasks.find(t => t.id === data.id)) {
          state.tasks.push(data)
          state.arrived.add(data.id)
          setTimeout(() => state.arrived.delete(data.id), 600)
        }
        syncCount()
      } else {
        const row = state.rooms.find(r => r.id === data.room_id)
        if (row) row.open_tasks = (row.open_tasks || 0) + 1
      }
    } else if (event === 'task.updated') {
      const j = state.allTasks.findIndex((t: any) => t.id === data.id)
      if (j >= 0 && state.allTasks[j].status !== 'review' && data.status === 'review') {
        const room = state.rooms.find(r => r.id === data.room_id)
        toast(`Card #${data.id} ready for review${room ? ' — ' + room.name : ''}`)
      }
      const i = state.tasks.findIndex(t => t.id === data.id)
      if (i >= 0) state.tasks[i] = data
      if (j >= 0) state.allTasks[j] = { ...state.allTasks[j], ...data }
      if (data.status !== 'in_progress') delete state.progress[data.id]
      if (data.room_id === state.current?.id) syncCount()
      else api('/rooms').then(rs => { state.rooms = rs }).catch(() => {})
      updateTitleBadge()
      if (state.modal?.task.id === data.id) state.modal.task = { ...state.modal.task, ...data }
    } else if (event === 'task.progress') {
      state.progress[data.task_id] = data.text
      if (state.modal?.task.id === data.task_id) {
        state.modal.log.push({ id: Date.now(), text: data.text, created_at: Date.now() / 1000 })
      }
    } else if (event === 'task.thread') {
      if (state.modal?.task.id === data.task_id
          && !state.modal.thread.find((m: any) => m.id === data.id)) {
        state.modal.thread.push(data)
      }
    } else if (event === 'assets.changed' && data.room_id === state.current?.id) {
      api(`/rooms/${data.room_id}/assets`).then(a => { state.assets = a }).catch(() => {})
    } else if (event === 'chat.message' && data.room_id === state.current?.id) {
      if (!state.chat.find((m: any) => m.id === data.id)) state.chat.push(data)
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
    state.rooms = await api('/rooms')
    state.homeChat = await api('/home/chat')
    state.allTasks = await api('/tasks')
    updateTitleBadge()
    const last = state.homeChat[state.homeChat.length - 1]
    state.awaitingReply = !!last && (last as any).role === 'user'
  },
  async checkHealth() {
    try { state.health = await api('/health') } catch { /* banner stays hidden */ }
    try { state.update = await api('/update/check') } catch { /* button stays plain */ }
  },
  async getUpdate() {
    state.updating = true
    try {
      state.update = await api('/update/check')
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
  async goHome() {
    state.current = null
    state.awaitingReply = false
    ;[state.homeChat, state.allTasks] = await Promise.all([api('/home/chat'), api('/tasks')])
    const last = state.homeChat[state.homeChat.length - 1]
    state.awaitingReply = !!last && (last as any).role === 'user'
  },
  async open(r: Room) {
    state.current = r
    state.awaitingReply = false
    const [tasks, chat, projects, assets] = await Promise.all([
      api(`/rooms/${r.id}/tasks`), api(`/rooms/${r.id}/chat`),
      api(`/rooms/${r.id}/projects`), api(`/rooms/${r.id}/assets`)
    ])
    state.tasks = tasks; state.chat = chat; state.roomProjects = projects; state.assets = assets
  },
  async createRoom(name: string) {
    try {
      const r = await api('/rooms', { method: 'POST', body: JSON.stringify({ name }) })
      if (!state.rooms.find(x => x.id === r.id)) state.rooms.unshift(r)
      await actions.open(r)
    } catch (e: any) { toast(e.message, true) }
  },
  async deleteRoom(r: Room) {
    try {
      await api(`/rooms/${r.id}`, { method: 'DELETE' })
      state.rooms = state.rooms.filter(x => x.id !== r.id)
      if (state.current?.id === r.id) await actions.goHome()
      toast(`Deleted "${r.name}"`)
    } catch (e: any) { toast(e.message, true) }
  },
  async loadProjects() {
    try { state.projects = await api('/projects') } catch (e: any) { toast(e.message, true) }
  },
  async sendHomeChat(text: string) {
    try {
      const r = await api('/home/chat', { method: 'POST', body: JSON.stringify({ text }) })
      if (!state.homeChat.find((m: any) => m.id === r.message.id)) state.homeChat.push(r.message)
      state.awaitingReply = true
    } catch (e: any) { toast(e.message, true) }
  },
  async sendChat(text: string, lane: 'auto' | 'chat' | 'task' | 'goal' = 'auto') {
    if (!state.current) return
    try {
      const r = await api(`/rooms/${state.current.id}/chat`, {
        method: 'POST', body: JSON.stringify({ text, lane })
      })
      if (!state.chat.find((m: any) => m.id === r.message.id)) state.chat.push(r.message)
      if (r.task) toast(`Card #${r.task.id} added to the board`)
      else if (r.lane === 'chat') state.awaitingReply = true
    } catch (e: any) { toast(e.message, true) }
  },
  async openTask(id: number) {
    try { state.modal = await api(`/tasks/${id}/log`) }
    catch (e: any) { toast(e.message, true) }
  },
  async replyTask(id: number, text: string) {
    try {
      await api(`/tasks/${id}/reply`, { method: 'POST', body: JSON.stringify({ text }) })
    } catch (e: any) { toast(e.message, true) }
  },
  async moveTask(id: number, status: Status) {
    const t = state.tasks.find(t => t.id === id) || state.allTasks.find((t: any) => t.id === id)
    if (!t || t.status === status) return
    const prev = t.status
    t.status = status
    try {
      await api(`/tasks/${id}`, { method: 'PATCH', body: JSON.stringify({ status }) })
    } catch (e: any) { t.status = prev; toast(e.message, true) }
  },
  async doSearch(q: string) {
    try { state.searchResults = await api(`/search?q=${encodeURIComponent(q)}`) }
    catch { state.searchResults = null }
  },
  async uploadAssets(files: FileList | File[]) {
    if (!state.current) return
    for (const f of Array.from(files)) {
      const form = new FormData()
      form.append('file', f)
      try {
        const res = await fetch(`/api/rooms/${state.current.id}/assets`, {
          method: 'POST', body: form
        })
        if (!res.ok) throw new Error((await res.json()).error || `upload failed (${res.status})`)
      } catch (e: any) { toast(e.message, true); return }
    }
    state.assets = await api(`/rooms/${state.current.id}/assets`)
    toast(files.length > 1 ? `${files.length} files uploaded` : 'Uploaded')
  },
  async deleteAsset(aid: number) {
    if (!state.current) return
    try {
      await api(`/rooms/${state.current.id}/assets/${aid}`, { method: 'DELETE' })
      state.assets = await api(`/rooms/${state.current.id}/assets`)
    } catch (e: any) { toast(e.message, true) }
  },
  projectsApi: {
    create: (body: any) => api('/projects', { method: 'POST', body: JSON.stringify(body) }),
    rename: (pid: number, name: string) => api(`/projects/${pid}`, { method: 'PATCH', body: JSON.stringify({ name }) }),
    remove: (pid: number) => api(`/projects/${pid}`, { method: 'DELETE' }),
    attach: (pid: number, path: string) => api(`/projects/${pid}/repos`, { method: 'POST', body: JSON.stringify({ path }) }),
    detach: (pid: number, rid: number) => api(`/projects/${pid}/repos/${rid}`, { method: 'DELETE' }),
    connect: (roomId: number, pid: number) => api(`/rooms/${roomId}/projects`, { method: 'POST', body: JSON.stringify({ project_id: pid }) }),
    disconnect: (roomId: number, pid: number) => api(`/rooms/${roomId}/projects/${pid}`, { method: 'DELETE' })
  },
  routinesApi: {
    list: (rid: number) => api(`/rooms/${rid}/routines`),
    add: (rid: number, r: any) => api(`/rooms/${rid}/routines`, { method: 'POST', body: JSON.stringify(r) }),
    toggle: (rtid: number, enabled: boolean) => api(`/routines/${rtid}`, { method: 'PATCH', body: JSON.stringify({ enabled }) }),
    remove: (rtid: number) => api(`/routines/${rtid}`, { method: 'DELETE' })
  },
  toast
}

export function useWorkspace() {
  return { state, ...actions }
}
