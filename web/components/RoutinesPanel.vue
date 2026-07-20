<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, routinesApi, openTask } = useWorkspace()
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
const title = ref('')
const body = ref('')
const mode = ref<'daily' | 'every'>('daily')
const at = ref('09:00')
const everyN = ref(4)
const everyUnit = ref<'h' | 'm'>('h')

async function load() {
  if (state.current) routines.value = await routinesApi.list(state.current.id)
}
onMounted(load)

function scheduleStr() {
  return mode.value === 'daily' ? `daily@${at.value}` : `every@${everyN.value}${everyUnit.value}`
}

function fmtSchedule(s: string) {
  const [k, arg] = s.split('@')
  return k === 'daily' ? `daily at ${arg}` : `every ${arg}`
}

function fmtNext(ts: number | null) {
  return ts ? new Date(ts * 1000).toLocaleString() : '—'
}

async function add() {
  if (!title.value.trim() || !state.current) return
  await routinesApi.add(state.current.id, {
    title: title.value, body: body.value, schedule: scheduleStr()
  })
  title.value = ''; body.value = ''
  await load()
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
  <div class="panel">
    <div class="routine-form">
      <input v-model="title" placeholder="What should happen? (becomes the card title)" aria-label="Routine title" />
      <textarea v-model="body" rows="2" placeholder="Details for the agent (optional)" aria-label="Routine details"></textarea>
      <div class="routine-when">
        <select v-model="mode" aria-label="Schedule type">
          <option value="daily">daily at</option>
          <option value="every">every</option>
        </select>
        <input v-if="mode === 'daily'" v-model="at" type="time" aria-label="Time of day" />
        <template v-else>
          <input v-model.number="everyN" type="number" min="1" style="width: 70px" aria-label="Interval" />
          <select v-model="everyUnit" aria-label="Interval unit">
            <option value="h">hours</option>
            <option value="m">minutes</option>
          </select>
        </template>
        <button class="btn" :disabled="!title.trim()" @click="add">Add routine</button>
      </div>
    </div>

    <div v-for="r in routines" :key="r.id" class="panel-col" :class="{ off: !r.enabled }">
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
        <button class="row-x" style="margin-left: 4px" title="Delete routine" @click.stop="remove(r)">✕</button>
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

    <div v-if="!routines.length" class="empty">
      <span class="glyph">—</span>
      <p>No routines in this room. A routine drops its card on the board on a
      schedule — the agent works it like any other card.</p>
    </div>
  </div>
</template>
