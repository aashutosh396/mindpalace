<script setup lang="ts">
import { ref } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, projectsApi, loadProjects, toast } = useWorkspace()
const newName = ref('')
const newPath = ref('')
const expanded = ref<number | null>(null)

async function create() {
  const n = newName.value.trim()
  if (!n) return
  const body: any = { name: n }
  if (newPath.value.trim()) body.path = newPath.value.trim()
  else body.workspace = true
  try {
    await projectsApi.create(body)
    newName.value = ''; newPath.value = ''
    await loadProjects()
    toast('Project added to the inventory')
  } catch (e: any) { toast(e.message, true) }
}

async function remove(p: any) {
  if (!window.confirm(`Delete project "${p.name}" from the inventory? Folders on disk are untouched.`)) return
  try { await projectsApi.remove(p.id); await loadProjects() }
  catch (e: any) { toast(e.message, true) }
}

async function attach(p: any) {
  const path = window.prompt(`Track another folder on "${p.name}":`, '')
  if (!path?.trim()) return
  try { await projectsApi.attach(p.id, path.trim()); await loadProjects() }
  catch (e: any) { toast(e.message, true) }
}

async function detach(p: any, r: any) {
  try { await projectsApi.detach(p.id, r.id); await loadProjects() }
  catch (e: any) { toast(e.message, true) }
}
</script>

<template>
  <div class="sheet-backdrop" @click.self="state.projectsOpen = false">
    <div class="sheet projects-sheet" role="dialog" aria-label="Projects inventory">
      <div class="sheet-head">
        <span class="rail-title">Projects — the inventory</span>
        <button class="row-x" title="Close" aria-label="Close" @click="state.projectsOpen = false">✕</button>
      </div>
      <p class="dim-note">
        Projects are resources: a name + folders/repos on disk. The keeper scans them in;
        rooms connect to them. Deleting one never touches your files.
      </p>

      <form class="proj-new" @submit.prevent="create">
        <input v-model="newName" placeholder="New project name" aria-label="Project name" />
        <input v-model="newPath" placeholder="/existing/folder (empty = new workspace folder)" aria-label="Folder path" />
        <button class="btn" :disabled="!newName.trim()">Add</button>
      </form>

      <div class="proj-list">
        <div v-for="p in state.projects" :key="p.id" class="proj-entry">
          <button class="proj-entry-head" @click="expanded = expanded === p.id ? null : p.id">
            <span class="proj-entry-name">{{ p.name }}</span>
            <span class="dim-inline">{{ p.repos.length }} folder{{ p.repos.length === 1 ? '' : 's' }}</span>
            <span v-if="p.rooms.length" class="room-tag">
              in {{ p.rooms.map((r: any) => r.name).join(', ') }}
            </span>
            <span class="dim-inline" style="margin-left: auto">{{ expanded === p.id ? '▾' : '▸' }}</span>
          </button>
          <div v-if="expanded === p.id" class="proj-entry-body">
            <div v-for="r in p.repos" :key="r.id" class="panel-row">
              <span class="path">{{ r.path }}</span>
              <span v-if="r.is_git" class="tag git">git</span>
              <span v-if="r.is_primary" class="tag">primary</span>
              <button class="row-x" title="Untrack folder" @click="detach(p, r)">✕</button>
            </div>
            <div class="proj-entry-actions">
              <button class="btn ghost" @click="attach(p)">Track another folder</button>
              <button class="btn ghost" @click="remove(p)">Delete project</button>
            </div>
          </div>
        </div>
        <div v-if="!state.projects.length" class="empty">
          <span class="glyph">—</span>
          <p>The inventory is empty. Tell the concierge to scan your vault, or add one above.</p>
        </div>
      </div>
    </div>
  </div>
</template>
