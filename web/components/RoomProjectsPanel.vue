<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, projectsApi, loadProjects } = useWorkspace()
const pick = ref<number | ''>('')

onMounted(loadProjects)

const connectable = computed(() => {
  const here = new Set(state.roomProjects.map((p: any) => p.id))
  return state.projects.filter((p: any) => !here.has(p.id))
})

async function connect() {
  if (pick.value === '' || !state.current) return
  await projectsApi.connect(state.current.id, Number(pick.value))
  pick.value = ''
}

async function disconnect(p: any) {
  if (!state.current) return
  await projectsApi.disconnect(state.current.id, p.id)
}
</script>

<template>
  <div class="panel">
    <form v-if="connectable.length" @submit.prevent="connect">
      <select v-model="pick" aria-label="Connect a project">
        <option value="" disabled>Connect a project to this room…</option>
        <option v-for="p in connectable" :key="p.id" :value="p.id">
          {{ p.name }} ({{ p.repos.length }} folder{{ p.repos.length === 1 ? '' : 's' }})
        </option>
      </select>
      <button class="btn" :disabled="pick === ''">Connect</button>
    </form>

    <div v-for="p in state.roomProjects" :key="p.id" class="proj-entry">
      <div class="proj-entry-head" style="cursor: default">
        <span class="proj-entry-name">{{ p.name }}</span>
        <button class="row-x" style="margin-left: auto" :title="`Disconnect ${p.name}`"
          @click="disconnect(p)">✕</button>
      </div>
      <div class="proj-entry-body">
        <div v-for="r in p.repos" :key="r.id" class="panel-row">
          <span class="path">{{ r.path }}</span>
          <span v-if="r.is_git" class="tag git">git</span>
          <span v-if="r.is_primary" class="tag">primary</span>
        </div>
        <p v-if="!p.repos.length" class="side-empty">No folders tracked on this project yet.</p>
      </div>
    </div>

    <div v-if="!state.roomProjects.length" class="empty">
      <span class="glyph">⌂</span>
      <p>No projects connected. Connect one above — the room's agent works inside
      the folders of its connected projects. Manage the inventory itself from the
      sidebar's Projects button.</p>
    </div>
  </div>
</template>
