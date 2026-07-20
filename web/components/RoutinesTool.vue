<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'
import { roomIcon } from '../composables/icons'

const { state, routinesApi, open } = useWorkspace()
const routines = ref<any[]>([])

async function load() {
  const res = await fetch('/api/routines')
  routines.value = await res.json()
}
onMounted(load)

const byRoom = computed(() => {
  const groups: Record<string, { name: string; slug: string; rows: any[] }> = {}
  for (const r of routines.value) {
    const g = groups[r.room_slug] ||= { name: r.room_name, slug: r.room_slug, rows: [] }
    g.rows.push(r)
  }
  return Object.values(groups)
})

function fmtSchedule(s: string) {
  const [k, arg] = s.split('@')
  return k === 'daily' ? `daily at ${arg}` : `every ${arg}`
}

function fmtNext(ts: number | null) {
  return ts ? new Date(ts * 1000).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) : '—'
}

function goRoom(slug: string) {
  const room = state.rooms.find(r => r.slug === slug)
  if (room) open(room)
}

async function toggle(r: any) {
  await routinesApi.toggle(r.id, !r.enabled)
  await load()
}

async function remove(r: any) {
  await routinesApi.remove(r.id)
  await load()
}
</script>

<template>
  <div class="main-body">
    <div class="panel">
      <div v-if="!routines.length" class="side-empty" style="padding: 18px 4px">
        No routines anywhere yet — open a room's Routines tab to schedule one.
      </div>

      <template v-for="g in byRoom" :key="g.slug">
        <button class="rt-room" @click="goRoom(g.slug)">
          <component :is="roomIcon(state.rooms.find(r => r.slug === g.slug)?.icon)" :size="13" :stroke-width="1.75" />
          {{ g.name }}
        </button>
        <div v-for="r in g.rows" :key="r.id" class="panel-row" :class="{ off: !r.enabled }">
          <div class="routine-main">
            <div class="routine-title">{{ r.title }}</div>
            <div class="dim" style="margin-left: 0">
              {{ fmtSchedule(r.schedule) }} · next: {{ fmtNext(r.next_run) }}
            </div>
          </div>
          <button class="btn ghost" style="flex: none" @click="toggle(r)">
            {{ r.enabled ? 'Pause' : 'Resume' }}
          </button>
          <button class="row-x" style="margin-left: 4px" :title="`Delete routine: ${r.title}`" @click="remove(r)">✕</button>
        </div>
      </template>
    </div>
  </div>
</template>
