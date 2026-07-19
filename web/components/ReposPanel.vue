<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, addRepo, linkRepo, removeRepo, loadAllRepos } = useWorkspace()
const path = ref('')
const pick = ref<number | ''>('')

onMounted(loadAllRepos)

const folders = computed(() => state.repos.own.filter((r: any) => !r.is_git))
const gitRepos = computed(() => state.repos.own.filter((r: any) => r.is_git))

// repos from OTHER rooms not already attached or linked here
const linkable = computed(() => {
  const here = new Set([...state.repos.own, ...state.repos.linked].map((r: any) => r.id))
  return state.allRepos.filter((r: any) =>
    r.project_id !== state.current?.id && !here.has(r.id))
})

async function add() {
  const p = path.value.trim()
  if (!p) return
  await addRepo(p, !state.repos.own.length)   // first folder becomes primary
  path.value = ''
  await loadAllRepos()
}

async function link() {
  if (pick.value === '') return
  await linkRepo(Number(pick.value))
  pick.value = ''
}
</script>

<template>
  <div class="panel">
    <form @submit.prevent="add">
      <input v-model="path" placeholder="/absolute/path/to/the project folder" aria-label="Folder path" />
      <button class="btn" :disabled="!path.trim()">Track folder</button>
    </form>

    <form v-if="linkable.length" @submit.prevent="link">
      <select v-model="pick" aria-label="Repo from another room">
        <option value="" disabled>Link a repo from another room…</option>
        <option v-for="r in linkable" :key="r.id" :value="r.id">
          {{ r.owner_name }} — {{ r.path }}
        </option>
      </select>
      <button class="btn ghost" :disabled="pick === ''">Link</button>
    </form>

    <template v-if="folders.length">
      <div class="tm-section">Folders</div>
      <div v-for="r in folders" :key="r.id" class="panel-row">
        <span class="path">{{ r.path }}</span>
        <span v-if="r.is_primary" class="tag">primary</span>
        <button class="row-x" title="Untrack" @click="removeRepo(r.id)">✕</button>
      </div>
    </template>

    <template v-if="gitRepos.length">
      <div class="tm-section">Git repos detected in project folder</div>
      <div v-for="r in gitRepos" :key="r.id" class="panel-row">
        <span class="path">{{ r.path }}</span>
        <span class="tag git">git</span>
        <span v-if="r.is_primary" class="tag">primary</span>
        <button class="row-x" title="Untrack" @click="removeRepo(r.id)">✕</button>
      </div>
    </template>

    <template v-if="state.repos.linked.length">
      <div class="tm-section">Linked from other rooms</div>
      <div v-for="r in state.repos.linked" :key="'l' + r.id" class="panel-row">
        <span class="path">{{ r.path }}</span>
        <span v-if="r.is_git" class="tag git">git</span>
        <span class="tag">linked · {{ r.owner_slug }}</span>
        <button class="row-x" title="Unlink" @click="removeRepo(r.id)">✕</button>
      </div>
    </template>

    <div v-if="!state.repos.own.length && !state.repos.linked.length" class="empty">
      <span class="glyph">⌂</span>
      <p>Nothing tracked yet. Point me at the project's main folder — I'll track it
      and every git repo inside it. The first folder becomes the agent's working
      directory.</p>
    </div>
  </div>
</template>
