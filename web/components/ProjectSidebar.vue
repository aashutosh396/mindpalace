<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, open, goHome, createRoom, deleteRoom, loadProjects, getUpdate } = useWorkspace()
const creating = ref(false)
const name = ref('')
const nameInput = ref<HTMLInputElement>()
const dark = ref(false)

onMounted(() => {
  dark.value = localStorage.getItem('theme') === 'dark'
  apply()
})

function apply() {
  document.documentElement.dataset.theme = dark.value ? 'dark' : 'light'
}

function toggleTheme() {
  dark.value = !dark.value
  localStorage.setItem('theme', dark.value ? 'dark' : 'light')
  apply()
}

async function startCreate() {
  creating.value = true
  await nextTick()
  nameInput.value?.focus()
}

async function create() {
  const n = name.value.trim()
  if (!n) { creating.value = false; return }
  name.value = ''
  creating.value = false
  await createRoom(n)
}

function confirmDelete(r: any) {
  if (window.confirm(`Delete room "${r.name}"? Its cards and chat go with it (projects and asset files stay).`)) {
    deleteRoom(r)
  }
}

async function openProjects() {
  await loadProjects()
  state.projectsOpen = true
}
</script>

<template>
  <aside class="sidebar">
    <div class="wordmark">mind<em>palace</em></div>

    <button class="menu-item" :class="{ here: !state.current }" @click="goHome">
      <span class="mi-icon plain">🏛</span> Home
    </button>
    <button class="menu-item primary" @click="startCreate">
      <span class="mi-icon">+</span> New chatroom
    </button>
    <form v-if="creating" class="new-proj" @submit.prevent="create">
      <input
        ref="nameInput" v-model="name" placeholder="Chatroom name…"
        aria-label="New chatroom name"
        @blur="!name.trim() && (creating = false)"
        @keydown.esc="creating = false; name = ''" />
    </form>

    <div class="side-label">Chatrooms</div>
    <nav class="rooms">
      <button
        v-for="r in state.rooms" :key="r.id"
        class="proj-item" :class="{ active: state.current?.id === r.id }"
        @click="open(r)">
        <span class="room-lead" :class="{ on: state.current?.id === r.id }">●</span>
        <span class="proj-name">{{ r.name }}</span>
        <span v-if="r.open_tasks" class="count">{{ r.open_tasks }}</span>
        <span
          class="room-x" role="button" tabindex="0"
          :title="`Delete ${r.name}`" :aria-label="`Delete ${r.name}`"
          @click.stop="confirmDelete(r)"
          @keydown.enter.stop="confirmDelete(r)">✕</span>
      </button>
      <p v-if="!state.rooms.length" class="side-empty">
        No chatrooms yet — they are your channels; make one.
      </p>
    </nav>

    <button class="menu-item dim" @click="openProjects">
      <span class="mi-icon">▦</span> Projects
    </button>
    <button class="menu-item dim" :disabled="state.updating" @click="getUpdate">
      <span class="mi-icon">⟳</span>
      {{ state.updating ? 'Checking…' : state.update?.behind ? 'Get update' : 'Check for updates' }}
    </button>

    <div class="side-user">
      <div class="avatar">m</div>
      <div class="side-user-meta">
        <div class="name">mindpalace</div>
        <div class="plan">
          <span :style="{ color: state.connected ? 'var(--sage)' : 'var(--danger)' }">●</span>
          {{ state.connected ? 'live' : 'reconnecting…' }}
          <template v-if="state.health"> · {{ state.health.commit.slice(0, 7) }}</template>
        </div>
      </div>
      <button class="theme-toggle" :title="dark ? 'Switch to light' : 'Switch to dark'"
        @click="toggleTheme">{{ dark ? '☀' : '☾' }}</button>
    </div>
  </aside>
</template>
