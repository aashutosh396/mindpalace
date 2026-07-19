<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, addRepo, linkRepo, removeRepo, loadAllRepos } = useWorkspace()
const path = ref('')
const pick = ref<number | ''>('')

onMounted(loadAllRepos)

// repos from OTHER rooms not already attached or linked here
const linkable = computed(() => {
  const here = new Set([...state.repos.own, ...state.repos.linked].map((r: any) => r.id))
  return state.allRepos.filter((r: any) =>
    r.project_id !== state.current?.id && !here.has(r.id))
})

async function add() {
  const p = path.value.trim()
  if (!p) return
  await addRepo(p, !state.repos.own.length)   // first repo becomes primary
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
      <input v-model="path" placeholder="/absolute/path/to/repo" aria-label="Repo path" />
      <button class="btn" :disabled="!path.trim()">Attach repo</button>
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

    <div v-for="r in state.repos.own" :key="r.id" class="panel-row">
      <span class="path">{{ r.path }}</span>
      <span v-if="r.is_primary" class="tag">primary</span>
      <button class="row-x" title="Remove repo" @click="removeRepo(r.id)">✕</button>
    </div>
    <div v-for="r in state.repos.linked" :key="'l' + r.id" class="panel-row">
      <span class="path">{{ r.path }}</span>
      <span class="tag">linked · {{ r.owner_slug }}</span>
      <button class="row-x" title="Unlink repo" @click="removeRepo(r.id)">✕</button>
    </div>

    <div v-if="!state.repos.own.length && !state.repos.linked.length" class="empty">
      <span class="glyph">⌂</span>
      <p>No repos attached. The agent works inside the repos you attach here —
      plus any repos linked from other rooms. The first repo becomes the
      agent's working directory.</p>
    </div>
  </div>
</template>
