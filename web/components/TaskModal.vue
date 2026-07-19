<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { useWorkspace, STATUSES, type Status } from '../composables/useWorkspace'

const { state, moveTask } = useWorkspace()
const trail = ref<HTMLElement>()

const LABELS: Record<string, string> = {
  todo: 'To do', in_progress: 'In progress', review: 'Review', done: 'Done'
}
const COLORS: Record<string, string> = {
  todo: 'var(--slate)', in_progress: 'var(--brass)', review: 'var(--lilac)', done: 'var(--sage)'
}

const t = computed(() => state.modal!.task)

function nextOf(s: Status): Status | null {
  const i = STATUSES.indexOf(s)
  return i < STATUSES.length - 1 ? STATUSES[i + 1] : null
}

function fmtTime(ts: number) {
  return new Date(ts * 1000).toLocaleTimeString()
}

watch(() => state.modal?.log.length, async () => {
  await nextTick()
  trail.value?.scrollTo({ top: trail.value.scrollHeight })
})
</script>

<template>
  <div class="sheet-backdrop" @click.self="state.modal = null">
    <div class="task-modal" role="dialog" :aria-label="`Card #${t.id}`">
      <div class="tm-head">
        <span class="status-pill" :style="{ '--c': COLORS[t.status] }">{{ LABELS[t.status] }}</span>
        <span v-if="state.modal!.room" class="room-tag">{{ state.modal!.room.name }}</span>
        <span class="tm-id">#{{ t.id }}</span>
        <button class="row-x" title="Close" aria-label="Close" @click="state.modal = null">✕</button>
      </div>

      <h2 class="tm-title">{{ t.title }}</h2>
      <p v-if="t.body && t.body !== t.title" class="tm-body">{{ t.body }}</p>

      <div class="tm-section">The work</div>
      <div ref="trail" class="tm-trail">
        <div v-for="l in state.modal!.log" :key="l.id" class="tm-step">
          <span class="tm-time">{{ fmtTime(l.created_at) }}</span>{{ l.text }}
        </div>
        <div v-if="!state.modal!.log.length" class="tm-step dim">
          {{ t.status === 'todo' ? 'Waiting for the worker to pick this up…' : 'No steps recorded.' }}
        </div>
        <div v-if="t.status === 'in_progress'" class="tm-step working">⚡ working…</div>
      </div>

      <template v-if="t.result">
        <div class="tm-section">Result</div>
        <div class="tm-result">{{ t.result }}</div>
      </template>

      <div class="tm-actions">
        <button v-if="nextOf(t.status)" class="btn ghost" @click="moveTask(t.id, nextOf(t.status)!)">
          → {{ LABELS[nextOf(t.status)!] }}
        </button>
        <button v-if="t.status !== 'done'" class="btn" @click="moveTask(t.id, 'done'); state.modal = null">
          Close card
        </button>
      </div>
    </div>
  </div>
</template>
