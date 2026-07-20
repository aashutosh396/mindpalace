<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { Bell, PanelRightClose, PanelRightOpen, RefreshCw } from 'lucide-vue-next'
import { useWorkspace } from './composables/useWorkspace'

const { state, init, checkHealth, toggleRail, open, goHome, getUpdate, openTask } = useWorkspace()

const today = new Date().toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' })

function toggleNotifs() {
  state.notifOpen = !state.notifOpen
  if (state.notifOpen) state.notifs.forEach((n: any) => { n.read = true })
}

async function openNotif(n: any) {
  state.notifOpen = false
  if (n.kind === 'update') { await getUpdate(); return }
  if (n.task_id) await openTask(n.task_id)
}
const booted = ref(false)

// ---- hash routes: #/home · #/room/<slug>[/projects|assets|routines] ----
const TABS: Record<string, 'chat' | 'repos' | 'assets' | 'routines'> = { projects: 'repos', assets: 'assets', routines: 'routines' }
const SLUGS: Record<string, string> = { repos: 'projects', assets: 'assets', routines: 'routines' }

async function applyHash() {
  const parts = location.hash.replace(/^#\/?/, '').split('/')
  if (parts[0] === 'tools' && (parts[1] === 'reminders' || parts[1] === 'routines')) {
    state.tool = parts[1]
    state.current = null
    return
  }
  if (parts[0] === 'room' && parts[1]) {
    const r = state.rooms.find(x => x.slug === decodeURIComponent(parts[1]))
    if (r) {
      if (state.current?.id !== r.id) await open(r)
      state.tab = TABS[parts[2]] || 'chat'
      return
    }
  }
  if (state.current) await goHome()
}

watch([() => state.current?.slug, () => state.tab, () => state.tool], () => {
  const h = state.current
    ? `#/room/${state.current.slug}` + (state.tab !== 'chat' ? '/' + SLUGS[state.tab] : '')
    : state.tool ? `#/tools/${state.tool}` : '#/home'
  if (location.hash !== h) history.replaceState(null, '', h)
})

function onKey(e: KeyboardEvent) {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault()
    state.searchOpen = !state.searchOpen
    if (!state.searchOpen) state.searchResults = null
    return
  }
  if (e.key === 'Escape') {
    if (state.toolsOpen) state.toolsOpen = false
    else if (state.notifOpen) state.notifOpen = false
    else if (state.roomSettings) state.roomSettings = null
    else if (state.searchOpen) { state.searchOpen = false; state.searchResults = null }
    else if (state.modal) state.modal = null
    else if (state.projectsOpen) state.projectsOpen = false
    else state.boardOpen = false
  }
}

onMounted(async () => {
  window.addEventListener('keydown', onKey)
  window.addEventListener('hashchange', applyHash)
  await init()
  await applyHash()
  booted.value = true
})
onUnmounted(() => {
  window.removeEventListener('keydown', onKey)
  window.removeEventListener('hashchange', applyHash)
})
</script>

<template>
  <div v-if="state.health && !state.health.provider_ok" class="setup-banner" role="alert">
    <strong>One step left:</strong> {{ state.health.provider_status }}.
    Install Claude Code, sign in to your Claude plan, then
    <button class="btn ghost" @click="checkHealth">Check again</button>
    <code>curl -fsSL https://claude.ai/install.sh | bash</code>
  </div>
  <header v-if="booted" class="topbar">
    <span class="tb-mark">mind<em>palace</em></span>
    <span class="tb-date">{{ today }}</span>
    <span class="bl-spacer"></span>
    <button v-if="state.update?.behind" class="tb-update" :disabled="state.updating" @click="getUpdate">
      <RefreshCw :size="12" :stroke-width="1.75" /> {{ state.updating ? 'Updating…' : 'Update available' }}
    </button>
    <button class="tb-bell" :aria-label="`Notifications (${state.notifs.filter(n => !n.read).length} unread)`"
      @click="toggleNotifs">
      <Bell :size="15" :stroke-width="1.75" />
      <span v-if="state.notifs.filter(n => !n.read).length" class="tb-badge">
        {{ state.notifs.filter(n => !n.read).length }}
      </span>
    </button>
    <div v-if="state.notifOpen" class="notif-panel" role="dialog" aria-label="Notifications">
      <div v-if="!state.notifs.length" class="notif-empty">Quiet so far — alerts, reminders and updates land here.</div>
      <button v-for="n in state.notifs.slice(0, 20)" :key="n.id" class="notif-row" @click="openNotif(n)">
        <span class="notif-text">{{ n.text }}</span>
        <span class="notif-time">{{ new Date(n.ts * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}</span>
      </button>
    </div>
  </header>
  <div v-if="!booted" class="boot-splash"><span class="star">✳</span></div>
  <div v-else class="shell" :class="{ 'rail-closed': !state.railOpen, dragging: state.railDragging }"
    :style="{ gridTemplateColumns: `250px 1fr ${state.railOpen && !state.tool ? state.railW + 'px' : '0px'}` }">
    <ProjectSidebar />

    <main class="main">
      <template v-if="state.current">
        <div class="main-head">
          <h1 class="room-name">{{ state.current.name }}</h1>
          <nav class="tabs">
            <button class="tab" :class="{ active: state.tab === 'chat' }" @click="state.tab = 'chat'">Chat</button>
            <button class="tab" :class="{ active: state.tab === 'repos' }" @click="state.tab = 'repos'">Projects</button>
            <button class="tab" :class="{ active: state.tab === 'assets' }" @click="state.tab = 'assets'">Assets</button>
            <button class="tab" :class="{ active: state.tab === 'routines' }" @click="state.tab = 'routines'">Routines</button>
            <button class="tab" :title="state.railOpen ? 'Hide the board' : 'Show the board'"
              :aria-label="state.railOpen ? 'Hide the board' : 'Show the board'"
              @click="toggleRail"><PanelRightClose v-if="state.railOpen" :size="15" :stroke-width="1.75" /><PanelRightOpen v-else :size="15" :stroke-width="1.75" /></button>
          </nav>
        </div>
        <ChatRail v-if="state.tab === 'chat'" class="center" />
        <div v-else class="main-body">
          <RoomProjectsPanel v-if="state.tab === 'repos'" :key="'p' + state.current.id" />
          <AssetsPanel v-else-if="state.tab === 'assets'" />
          <RoutinesPanel v-else :key="state.current.id" />
        </div>
      </template>

      <template v-else-if="state.tool === 'reminders'">
        <div class="main-head">
          <h1 class="room-name">Reminders</h1>
        </div>
        <RemindersPage />
      </template>

      <template v-else-if="state.tool === 'routines'">
        <div class="main-head">
          <h1 class="room-name">Routines</h1>
        </div>
        <RoutinesTool />
      </template>

      <template v-else>
        <div class="main-head">
          <h1 class="room-name">Home</h1>
          <nav class="tabs">
            <button class="tab" :title="state.railOpen ? 'Hide the board' : 'Show the board'"
              :aria-label="state.railOpen ? 'Hide the board' : 'Show the board'"
              @click="toggleRail"><PanelRightClose v-if="state.railOpen" :size="15" :stroke-width="1.75" /><PanelRightOpen v-else :size="15" :stroke-width="1.75" /></button>
          </nav>
        </div>
        <ChatRail class="center" />
      </template>
    </main>

    <BoardRail v-show="state.railOpen && !state.tool" />

    <div class="foot foot-side"></div>
    <div class="foot foot-main"><Composer v-if="!state.tool" /></div>
    <div v-show="state.railOpen && !state.tool" class="foot foot-rail"></div>

    <div v-if="state.toast" class="toast" :class="{ error: state.toastError }" role="status">
      {{ state.toast }}
    </div>

    <TaskModal v-if="state.modal" />
    <SearchOverlay v-if="state.searchOpen" />
    <ProjectsSheet v-if="state.projectsOpen" />
    <RoomSettingsModal v-if="state.roomSettings" :key="state.roomSettings.id" />
    <ToolsModal v-if="state.toolsOpen" />
    <OnboardingOverlay v-if="state.showOnboarding" />

    <div v-if="state.boardOpen" class="sheet-backdrop" @click.self="state.boardOpen = false">
      <div class="sheet" role="dialog" aria-label="Project board">
        <div class="sheet-head">
          <span class="rail-title">{{ state.current ? `The board — ${state.current.name}` : 'The board — all rooms' }}</span>
          <button class="row-x" title="Close" aria-label="Close the board" @click="state.boardOpen = false">✕</button>
        </div>
        <KanbanBoard />
      </div>
    </div>
  </div>
</template>
