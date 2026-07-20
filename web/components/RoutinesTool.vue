<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'
import { roomIcon } from '../composables/icons'

const { state, routinesApi, open, openTask } = useWorkspace()

const editing = ref<any | null>(null)

function startEdit(r: any) {
  const [kind, arg] = (r.schedule || 'daily@09:00').split('@')
  editing.value = {
    id: r.id, title: r.title, body: r.body || '',
    mode: kind === 'every' ? 'every' : 'daily',
    at: kind === 'daily' ? arg : '09:00',
    everyN: kind === 'every' ? (parseInt(arg) || 1) : 4,
    everyUnit: kind === 'every' && String(arg).endsWith('m') ? 'm' : 'h'
  }
}

async function saveEdit() {
  if (!editing.value) return
  const e = editing.value
  const schedule = e.mode === 'daily' ? `daily@${e.at}` : `every@${e.everyN}${e.everyUnit}`
  await routinesApi.update(e.id, { title: e.title, body: e.body, schedule })
  editing.value = null
  await load()
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
  if (!window.confirm(`Delete routine “${r.title}”? Its run history goes with it — this cannot be undone.`)) return
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
            :aria-label="`Run history for ${r.title}`"
            @click="state.runsFor = r" @keydown.enter="state.runsFor = r">
            <div class="routine-main">
              <div class="routine-title">{{ r.title }}</div>
              <div class="dim" style="margin-left: 0">
                {{ fmtSchedule(r.schedule) }} · next: {{ fmtNext(r.next_run) }}
              </div>
            </div>
            <button class="btn ghost" style="flex: none" @click.stop="startEdit(r)">Edit</button>
            <button class="btn ghost" style="flex: none" @click.stop="toggle(r)">
              {{ r.enabled ? 'Pause' : 'Resume' }}
            </button>
            <button class="btn ghost danger" style="flex: none; margin-left: 4px" @click.stop="remove(r)">Delete</button>
          </div>
          <div v-if="editing?.id === r.id" class="routine-form" style="margin: 4px 0 6px" @click.stop>
            <input v-model="editing.title" aria-label="Routine title" />
            <textarea v-model="editing.body" rows="2" aria-label="Routine details"></textarea>
            <div class="routine-when">
              <select v-model="editing.mode" aria-label="Schedule type">
                <option value="daily">daily at</option>
                <option value="every">every</option>
              </select>
              <input v-if="editing.mode === 'daily'" v-model="editing.at" type="time" aria-label="Time of day" />
              <template v-else>
                <input v-model.number="editing.everyN" type="number" min="1" style="width: 70px" aria-label="Interval" />
                <select v-model="editing.everyUnit" aria-label="Interval unit">
                  <option value="h">hours</option>
                  <option value="m">minutes</option>
                </select>
              </template>
              <button class="btn" @click="saveEdit">Save</button>
              <button class="btn ghost" @click="editing = null">Cancel</button>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
