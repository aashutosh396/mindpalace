<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { useWorkspace } from './composables/useWorkspace'

const { state, init, checkHealth, toggleRail, open, goHome } = useWorkspace()
const tab = ref<'chat' | 'repos' | 'assets' | 'routines'>('chat')

// ---- hash routes: #/home · #/room/<slug>[/projects|assets|routines] ----
const TABS: Record<string, typeof tab.value> = { projects: 'repos', assets: 'assets', routines: 'routines' }
const SLUGS: Record<string, string> = { repos: 'projects', assets: 'assets', routines: 'routines' }

async function applyHash() {
  const parts = location.hash.replace(/^#\/?/, '').split('/')
  if (parts[0] === 'room' && parts[1]) {
    const r = state.rooms.find(x => x.slug === decodeURIComponent(parts[1]))
    if (r) {
      if (state.current?.id !== r.id) await open(r)
      tab.value = TABS[parts[2]] || 'chat'
      return
    }
  }
  if (state.current) await goHome()
}

watch([() => state.current?.slug, tab], () => {
  const h = state.current
    ? `#/room/${state.current.slug}` + (tab.value !== 'chat' ? '/' + SLUGS[tab.value] : '')
    : '#/home'
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
    if (state.searchOpen) { state.searchOpen = false; state.searchResults = null }
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
  <div class="shell" :class="{ 'rail-closed': !state.railOpen, dragging: state.railDragging }"
    :style="{ gridTemplateColumns: `250px 1fr ${state.railOpen ? state.railW + 'px' : '0px'}` }">
    <ProjectSidebar />

    <main class="main">
      <template v-if="state.current">
        <div class="main-head">
          <h1 class="room-name">{{ state.current.name }}</h1>
          <span class="room-slug">{{ state.current.slug }}</span>
          <nav class="tabs">
            <button class="tab" :class="{ active: tab === 'chat' }" @click="tab = 'chat'">Chat</button>
            <button class="tab" :class="{ active: tab === 'repos' }" @click="tab = 'repos'">Projects</button>
            <button class="tab" :class="{ active: tab === 'assets' }" @click="tab = 'assets'">Assets</button>
            <button class="tab" :class="{ active: tab === 'routines' }" @click="tab = 'routines'">Routines</button>
            <button class="tab" :title="state.railOpen ? 'Hide the board' : 'Show the board'"
              @click="toggleRail">{{ state.railOpen ? '⟩' : '⟨' }}</button>
          </nav>
        </div>
        <ChatRail v-if="tab === 'chat'" class="center" />
        <div v-else class="main-body">
          <RoomProjectsPanel v-if="tab === 'repos'" :key="'p' + state.current.id" />
          <AssetsPanel v-else-if="tab === 'assets'" />
          <RoutinesPanel v-else :key="state.current.id" />
        </div>
      </template>

      <template v-else>
        <div class="main-head">
          <h1 class="room-name">Home</h1>
          <span class="room-slug">the hall — speak, I'll route it</span>
          <nav class="tabs">
            <button class="tab" :title="state.railOpen ? 'Hide the board' : 'Show the board'"
              @click="toggleRail">{{ state.railOpen ? '⟩' : '⟨' }}</button>
          </nav>
        </div>
        <ChatRail class="center" />
      </template>
    </main>

    <BoardRail v-show="state.railOpen" />

    <div class="foot foot-side"><ProfileFoot /></div>
    <div class="foot foot-main"><Composer /></div>
    <div v-show="state.railOpen" class="foot foot-rail"></div>

    <div v-if="state.toast" class="toast" :class="{ error: state.toastError }" role="status">
      {{ state.toast }}
    </div>

    <TaskModal v-if="state.modal" />
    <SearchOverlay v-if="state.searchOpen" />
    <ProjectsSheet v-if="state.projectsOpen" />
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
