<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, routinesApi } = useWorkspace()
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

    <div v-for="r in routines" :key="r.id" class="panel-row" :class="{ off: !r.enabled }">
      <div class="routine-main">
        <div class="routine-title">{{ r.title }}</div>
        <div class="dim" style="margin-left: 0">
          {{ fmtSchedule(r.schedule) }} · next: {{ fmtNext(r.next_run) }}
        </div>
      </div>
      <button class="btn ghost" style="flex: none" @click="toggle(r)">
        {{ r.enabled ? 'Pause' : 'Resume' }}
      </button>
      <button class="row-x" style="margin-left: 4px" title="Delete routine" @click="remove(r)">✕</button>
    </div>

    <div v-if="!routines.length" class="empty">
      <span class="glyph">—</span>
      <p>No routines in this room. A routine drops its card on the board on a
      schedule — the agent works it like any other card.</p>
    </div>
  </div>
</template>
