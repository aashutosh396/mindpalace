<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, projectsApi, loadProjects } = useWorkspace()
const pick = ref<number | ''>('')
const open = reactive<Record<number, boolean>>({})

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
      <button class="proj-entry-head" :aria-expanded="!!open[p.id]"
        @click="open[p.id] = !open[p.id]">
        <svg class="caret" :class="{ open: open[p.id] }" width="14" height="14"
          viewBox="0 0 16 16" aria-hidden="true">
          <path d="M6 4l4 4-4 4" stroke="currentColor" stroke-width="2" fill="none"
            stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        <span class="proj-entry-name">{{ p.name }}</span>
        <span class="dim-inline">{{ p.repos.length }} folder{{ p.repos.length === 1 ? '' : 's' }}</span>
        <span class="row-x" role="button" tabindex="0" style="margin-left: auto; display: block"
          :title="`Disconnect ${p.name}`"
          @click.stop="disconnect(p)" @keydown.enter.stop="disconnect(p)">✕</span>
      </button>
      <div v-if="open[p.id]" class="proj-entry-body">
        <div v-for="r in p.repos" :key="r.id" class="panel-row">
          <span class="path">{{ r.path }}</span>
          <span v-if="r.is_git" class="tag git">git</span>
          <span v-if="r.is_primary" class="tag">primary</span>
        </div>
        <p v-if="!p.repos.length" class="side-empty">No folders tracked on this project yet.</p>
      </div>
    </div>

    <div v-if="!state.roomProjects.length" class="empty">
      <span class="glyph">—</span>
      <p>No projects connected. Connect one above — or just mention a project by
      name in the chat and it connects itself.</p>
    </div>
  </div>
</template>
