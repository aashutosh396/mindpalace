<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, open, createProject, getUpdate } = useWorkspace()
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
  await createProject(n)
}
</script>

<template>
  <aside class="sidebar">
    <div class="wordmark">mind<em>palace</em></div>

    <button class="menu-item" @click="startCreate">
      <span class="mi-icon">+</span> New project
    </button>
    <form v-if="creating" class="new-proj" @submit.prevent="create">
      <input
        ref="nameInput" v-model="name" placeholder="Project name…"
        aria-label="New project name"
        @blur="!name.trim() && (creating = false)"
        @keydown.esc="creating = false; name = ''" />
    </form>

    <div class="side-label">Rooms</div>
    <nav class="rooms">
      <button
        v-for="p in state.projects" :key="p.id"
        class="proj-item" :class="{ active: state.current?.id === p.id }"
        @click="open(p)">
        <span class="proj-name">{{ p.name }}</span>
        <span v-if="p.open_tasks" class="count">{{ p.open_tasks }}</span>
      </button>
      <p v-if="!state.projects.length" class="side-empty">No rooms yet.</p>
    </nav>

    <div style="flex: 1"></div>

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
