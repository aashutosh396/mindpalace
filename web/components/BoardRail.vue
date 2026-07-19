<script setup lang="ts">
import { computed } from 'vue'
import { useWorkspace, STATUSES, type Status } from '../composables/useWorkspace'

const { state, moveTask } = useWorkspace()

const COLS: { key: Status; label: string; color: string }[] = [
  { key: 'todo', label: 'To do', color: 'var(--slate)' },
  { key: 'in_progress', label: 'In progress', color: 'var(--brass)' },
  { key: 'review', label: 'Review', color: 'var(--lilac)' },
  { key: 'done', label: 'Done', color: 'var(--sage)' }
]

const byStatus = computed(() =>
  Object.fromEntries(STATUSES.map(s => [s, state.tasks.filter(t => t.status === s)])))

function nextOf(s: Status): Status | null {
  const i = STATUSES.indexOf(s)
  return i < STATUSES.length - 1 ? STATUSES[i + 1] : null
}
</script>

<template>
  <aside class="board-rail">
    <div class="rail-head">
      <span class="rail-title">The board</span>
      <button class="expand" title="Expand the board" aria-label="Expand the board"
        @click="state.boardOpen = true">⛶</button>
    </div>

    <div class="rail-body">
      <section v-for="col in COLS" :key="col.key" class="rail-group">
        <header class="rail-group-head">
          <span class="dot" :style="{ background: col.color }"></span>
          {{ col.label }}
          <span class="n">{{ byStatus[col.key].length }}</span>
        </header>
        <article
          v-for="t in byStatus[col.key]" :key="t.id"
          class="rail-card" :class="{ arriving: state.arrived.has(t.id) }"
          :style="{ '--status': col.color }">
          <div class="rail-card-title">{{ t.title }}</div>
          <div v-if="t.status === 'in_progress' && state.progress[t.id]" class="card-progress">
            {{ state.progress[t.id] }}
          </div>
          <div class="rail-card-foot">
            <span class="id">#{{ t.id }}</span>
            <button v-if="nextOf(t.status)" @click="moveTask(t.id, nextOf(t.status)!)">→</button>
            <button v-if="t.status !== 'done'" title="Close" @click="moveTask(t.id, 'done')">✓</button>
          </div>
        </article>
      </section>
      <div v-if="!state.tasks.length" class="empty" style="padding: 24px 10px; font-size: 12.5px">
        No cards yet — send an instruction in the chat.
      </div>
    </div>
  </aside>
</template>
