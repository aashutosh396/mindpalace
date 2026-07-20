<script setup lang="ts">
import { nextTick, ref } from 'vue'
import { Plus, LayoutGrid, RefreshCw, Landmark, Settings2, X } from 'lucide-vue-next'
import { useWorkspace } from '../composables/useWorkspace'
import { roomIcon } from '../composables/icons'

const { state, open, goHome, createRoom, deleteRoom, loadProjects, getUpdate } = useWorkspace()
const creating = ref(false)
const name = ref('')
const nameInput = ref<HTMLInputElement>()

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

    <button class="menu-item primary" @click="startCreate">
      <span class="mi-icon"><Plus :size="13" :stroke-width="2.25" /></span> New chatroom
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
        class="proj-item" :class="{ active: !state.current }"
        @click="goHome">
        <span class="room-ico" :class="{ on: !state.current }"><Landmark :size="15" :stroke-width="1.75" /></span>
        <span class="proj-name">Home</span>
      </button>
      <button
        v-for="r in state.rooms" :key="r.id"
        class="proj-item" :class="{ active: state.current?.id === r.id }"
        @click="open(r)">
        <span class="room-ico" :class="{ on: state.current?.id === r.id }">
          <component :is="roomIcon(r.icon)" :size="15" :stroke-width="1.75" />
        </span>
        <span class="proj-name">{{ r.name }}</span>
        <span v-if="r.open_tasks" class="count">{{ r.open_tasks }}</span>
        <span class="room-tools">
          <span
            class="room-x" role="button" tabindex="0"
            :title="`Settings for ${r.name}`" :aria-label="`Settings for ${r.name}`"
            @click.stop="state.roomSettings = r"
            @keydown.enter.stop="state.roomSettings = r"><Settings2 :size="13" :stroke-width="1.75" /></span>
          <span
            class="room-x" role="button" tabindex="0"
            :title="`Delete ${r.name}`" :aria-label="`Delete ${r.name}`"
            @click.stop="confirmDelete(r)"
            @keydown.enter.stop="confirmDelete(r)"><X :size="13" :stroke-width="1.75" /></span>
        </span>
      </button>
      <p v-if="!state.rooms.length" class="side-empty">
        No chatrooms yet — they are your channels; make one.
      </p>
    </nav>

    <button class="menu-item dim" @click="openProjects">
      <span class="mi-icon"><LayoutGrid :size="15" :stroke-width="1.75" /></span> Projects
    </button>
    <button class="menu-item dim" :disabled="state.updating" @click="getUpdate">
      <span class="mi-icon"><RefreshCw :size="15" :stroke-width="1.75" /></span>
      {{ state.updating ? 'Checking…' : state.update?.behind ? 'Get update' : 'Check for updates' }}
    </button>
    <ProfileFoot />
  </aside>
</template>
