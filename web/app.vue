<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useWorkspace } from './composables/useWorkspace'

const { state, init, checkHealth } = useWorkspace()
const tab = ref<'board' | 'assets' | 'repos'>('board')

onMounted(init)
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
            <button class="tab" :class="{ active: tab === 'board' }" @click="tab = 'board'">Board</button>
            <button class="tab" :class="{ active: tab === 'repos' }" @click="tab = 'repos'">Repos</button>
            <button class="tab" :class="{ active: tab === 'assets' }" @click="tab = 'assets'">Assets</button>
          </nav>
        </div>
        <div class="main-body">
          <KanbanBoard v-if="tab === 'board'" />
          <ReposPanel v-else-if="tab === 'repos'" />
          <AssetsPanel v-else />
        </div>
      </template>

      <div v-else class="empty" style="margin-top: 18vh">
        <span class="glyph">🏛️</span>
        <p>Every project is a room in your palace.</p>
        <p>Create one in the sidebar to begin.</p>
      </div>
    </main>

    <ChatRail />

    <div v-if="state.toast" class="toast" :class="{ error: state.toastError }" role="status">
      {{ state.toast }}
    </div>
  </div>
</template>
