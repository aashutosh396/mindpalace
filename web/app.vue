<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import { useWorkspace } from './composables/useWorkspace'

const { state, init, checkHealth } = useWorkspace()
const tab = ref<'chat' | 'repos' | 'assets' | 'routines'>('chat')

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

onMounted(() => { init(); window.addEventListener('keydown', onKey) })
onUnmounted(() => window.removeEventListener('keydown', onKey))
</script>

<template>
  <div v-if="state.health && !state.health.provider_ok" class="setup-banner" role="alert">
    <strong>One step left:</strong> {{ state.health.provider_status }}.
    Install Claude Code, sign in to your Claude plan, then
    <button class="btn ghost" @click="checkHealth">Check again</button>
    <code>curl -fsSL https://claude.ai/install.sh | bash</code>
  </div>
  <div class="shell">
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
        </div>
        <ChatRail class="center" />
      </template>
    </main>

    <BoardRail />

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
