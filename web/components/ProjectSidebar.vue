<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, open, createProject, getUpdate } = useWorkspace()
const name = ref('')
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

async function create() {
  const n = name.value.trim()
  if (!n) return
  name.value = ''
  await createProject(n)
}
</script>

<template>
  <aside class="sidebar">
    <div class="wordmark">mind<em>palace</em></div>

    <div class="side-label">Rooms</div>
    <button
      v-for="p in state.projects" :key="p.id"
      class="proj-item" :class="{ active: state.current?.id === p.id }"
      @click="open(p)">
      <span>{{ p.name }}</span>
      <span v-if="p.open_tasks" class="count">{{ p.open_tasks }}</span>
    </button>

    <p v-if="!state.projects.length" class="side-label" style="text-transform: none; letter-spacing: 0">
      No rooms yet.
    </p>

    <form class="new-proj" @submit.prevent="create">
      <input v-model="name" placeholder="New project…" aria-label="New project name" />
      <button class="btn" :disabled="!name.trim()">Add</button>
    </form>

    <div style="flex: 1"></div>
    <button
      class="btn ghost update-btn"
      :disabled="state.updating"
      :title="state.update ? `installed ${state.update.local} · latest ${state.update.remote}` : 'Check GitHub for a newer build'"
      @click="getUpdate">
      {{ state.updating ? 'Checking…' : state.update?.behind ? '⟳ Get update' : '⟳ Check for updates' }}
    </button>
    <div class="side-foot">
      <span class="side-label" :style="{ color: state.connected ? 'var(--sage)' : 'var(--danger)' }">
        {{ state.connected ? '● live' : '○ reconnecting…' }}
      </span>
      <button class="theme-toggle" :title="dark ? 'Switch to light' : 'Switch to dark'"
        @click="toggleTheme">{{ dark ? '☀' : '☾' }}</button>
    </div>
  </aside>
</template>
