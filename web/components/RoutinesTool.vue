<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'
import { roomIcon } from '../composables/icons'

const { state, routinesApi, open, openTask } = useWorkspace()
const runs = ref<Record<number, any[]>>({})
const expanded = ref<Record<number, boolean>>({})

async function toggleRuns(r: any) {
  expanded.value[r.id] = !expanded.value[r.id]
  if (expanded.value[r.id] && !runs.value[r.id]) {
    const res = await fetch(`/api/routines/${r.id}/runs`)
    runs.value[r.id] = await res.json()
  }
}

function tickOf(run: any) {
  if (run.status === 'done') return run.result?.startsWith('(') ? '✗' : '✓'
  if (run.status === 'review') return '◉'
  return '…'
}

function tickClass(run: any) {
  if (run.status === 'done') return run.result?.startsWith('(') ? 'bad' : 'ok'
  return run.status === 'review' ? 'eye' : 'run'
}

function fmtRun(ts: number) {
  return new Date(ts * 1000).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

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
        <div v-for="r in g.rows" :key="r.id" class="panel-col" :class="{ off: !r.enabled }">
          <div class="panel-row rt-clickable" role="button" tabindex="0"
            :aria-expanded="!!expanded[r.id]" :aria-label="`Run history for ${r.title}`"
            @click="toggleRuns(r)" @keydown.enter="toggleRuns(r)">
            <div class="routine-main">
              <div class="routine-title">{{ r.title }}</div>
              <div class="dim" style="margin-left: 0">
                {{ fmtSchedule(r.schedule) }} · next: {{ fmtNext(r.next_run) }}
              </div>
            </div>
            <button class="btn ghost" style="flex: none" @click.stop="toggle(r)">
              {{ r.enabled ? 'Pause' : 'Resume' }}
            </button>
            <button class="row-x" style="margin-left: 4px" :title="`Delete routine: ${r.title}`" @click.stop="remove(r)">✕</button>
          </div>
          <div v-if="expanded[r.id]" class="rt-runs">
              <div v-if="!(runs[r.id] || []).length" class="dim" style="margin: 0; font-size: 12px">
            No runs yet — first fire is at the next scheduled time.
            </div>
            <button v-for="run in runs[r.id]" :key="run.id" class="rt-run" @click.stop="openTask(run.id)">
              <span class="rt-tick" :class="tickClass(run)">{{ tickOf(run) }}</span>
              <span>{{ fmtRun(run.created_at) }}</span>
              <span class="dim" style="margin-left: auto">card #{{ run.id }}</span>
            </button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
