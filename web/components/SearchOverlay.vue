<script setup lang="ts">
import { nextTick, onMounted, ref, watch } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, doSearch, open, openTask } = useWorkspace()
const q = ref('')
const box = ref<HTMLInputElement>()
let timer: ReturnType<typeof setTimeout> | null = null

onMounted(async () => {
  await nextTick()
  box.value?.focus()
})

watch(q, () => {
  if (timer) clearTimeout(timer)
  timer = setTimeout(() => doSearch(q.value), 200)
})

function close() {
  state.searchOpen = false
  state.searchResults = null
}

async function goRoom(r: any) {
  close()
  const p = state.projects.find(p => p.id === r.id)
  if (p) await open(p)
}

async function goTask(t: any) {
  close()
  await openTask(t.id)
}

async function goChat(c: any) {
  close()
  const p = state.projects.find(p => p.id === c.project_id)
  if (p) await open(p)
}
</script>

<template>
  <div class="sheet-backdrop" @click.self="close">
    <div class="search-box" role="dialog" aria-label="Search the palace">
      <input ref="box" v-model="q" placeholder="Search rooms, cards, chats…" aria-label="Search" />
      <div v-if="state.searchResults" class="search-results">
        <template v-if="state.searchResults.rooms.length">
          <div class="tm-section">Rooms</div>
          <button v-for="r in state.searchResults.rooms" :key="'r' + r.id" class="search-hit" @click="goRoom(r)">
            ● {{ r.name }} <span class="dim-inline">{{ r.slug }}</span>
          </button>
        </template>
        <template v-if="state.searchResults.tasks.length">
          <div class="tm-section">Cards</div>
          <button v-for="t in state.searchResults.tasks" :key="'t' + t.id" class="search-hit" @click="goTask(t)">
            #{{ t.id }} {{ t.title }} <span class="dim-inline">{{ t.room_name }} · {{ t.status }}</span>
          </button>
        </template>
        <template v-if="state.searchResults.chats.length">
          <div class="tm-section">Chat</div>
          <button v-for="c in state.searchResults.chats" :key="'c' + c.id" class="search-hit" @click="goChat(c)">
            {{ c.text.slice(0, 80) }} <span class="dim-inline">{{ c.room_name }}</span>
          </button>
        </template>
        <div v-if="q.length >= 2 && !state.searchResults.rooms.length && !state.searchResults.tasks.length && !state.searchResults.chats.length"
          class="tm-section" style="text-transform: none">Nothing found for “{{ q }}”.</div>
      </div>
    </div>
  </div>
</template>
