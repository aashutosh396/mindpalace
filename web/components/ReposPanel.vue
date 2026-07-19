<script setup lang="ts">
import { ref } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, addRepo } = useWorkspace()
const path = ref('')

async function add() {
  const p = path.value.trim()
  if (!p) return
  await addRepo(p, !state.repos.own.length)   // first repo becomes primary
  path.value = ''
}
</script>

<template>
  <div class="panel">
    <form @submit.prevent="add">
      <input v-model="path" placeholder="/absolute/path/to/repo" aria-label="Repo path" />
      <button class="btn" :disabled="!path.trim()">Attach repo</button>
    </form>

    <div v-for="r in state.repos.own" :key="r.id" class="panel-row">
      <span class="path">{{ r.path }}</span>
      <span v-if="r.is_primary" class="tag">primary</span>
    </div>
    <div v-for="r in state.repos.linked" :key="'l' + r.id" class="panel-row">
      <span class="path">{{ r.path }}</span>
      <span class="tag">linked · {{ r.owner_slug }}</span>
    </div>

    <div v-if="!state.repos.own.length && !state.repos.linked.length" class="empty">
      <span class="glyph">⌂</span>
      <p>No repos attached. The agent works inside the repos you attach here —
      plus any repos linked from other rooms.</p>
    </div>
  </div>
</template>
