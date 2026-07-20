<script setup lang="ts">
import { computed, reactive } from 'vue'
import { useWorkspace, STATUSES, type Status } from '../composables/useWorkspace'

const { state, moveTask, openTask } = useWorkspace()

const COLS: { key: Status; label: string; color: string }[] = [
  { key: 'review', label: 'Review', color: 'var(--lilac)' },      // your inbox first
  { key: 'in_progress', label: 'In progress', color: 'var(--brass)' },
  { key: 'todo', label: 'To do', color: 'var(--slate)' },
  { key: 'done', label: 'Done', color: 'var(--sage)' }
]
const CAP = 30

const collapsed = reactive<Record<string, boolean>>(
  JSON.parse(localStorage.getItem('railCollapsed') || '{"done":true}'))

function toggle(k: string) {
  collapsed[k] = !collapsed[k]
  localStorage.setItem('railCollapsed', JSON.stringify(collapsed))
}

const tasks = computed<any[]>(() => state.current ? state.tasks : state.allTasks)
const byStatus = computed(() =>
  Object.fromEntries(STATUSES.map(s => [s, tasks.value.filter((t: any) => t.status === s)])))

function nextOf(s: Status): Status | null {
  const i = STATUSES.indexOf(s)
  return i < STATUSES.length - 1 ? STATUSES[i + 1] : null
}
</script>

<template>
  <aside class="board-rail">
    <div class="rail-head">
      <span class="rail-title">{{ state.current ? 'The board' : 'All rooms' }}</span>
      <button class="expand" title="Expand the board" aria-label="Expand the board"
        @click="state.boardOpen = true">⛶</button>
    </div>

    <div class="rail-body">
      <section v-for="col in COLS" :key="col.key" class="rail-group">
        <header class="rail-group-head clickable" role="button" tabindex="0"
          @click="toggle(col.key)" @keydown.enter="toggle(col.key)">
          <span class="dot" :style="{ background: col.color }"></span>
          {{ col.label }}
          <span class="n">{{ byStatus[col.key].length }}</span>
          <span class="caret">{{ collapsed[col.key] ? '▸' : '▾' }}</span>
        </header>
        <template v-if="!collapsed[col.key]">
          <article
            v-for="t in byStatus[col.key].slice(0, CAP)" :key="t.id"
            class="rail-row" :class="{ arriving: state.arrived.has(t.id) }"
            :style="{ '--status': col.color }"
            role="button" tabindex="0"
            @click="openTask(t.id)"
            @keydown.enter="openTask(t.id)">
            <span class="title">{{ t.title }}</span>
            <span v-if="t.kind === 'goal'" class="row-meta">🎯×{{ t.iterations || 0 }}</span>
            <span v-if="!state.current && t.room_name" class="row-meta">{{ t.room_name }}</span>
            <span class="row-meta">#{{ t.id }}</span>
            <span class="row-actions">
              <button v-if="nextOf(t.status)" title="Advance"
                @click.stop="moveTask(t.id, nextOf(t.status)!)">→</button>
              <button v-if="t.status !== 'done'" title="Close"
                @click.stop="moveTask(t.id, 'done')">✓</button>
            </span>
          </article>
          <div v-if="byStatus[col.key].some((t: any) => t.status === 'in_progress' && state.progress[t.id])"
            class="card-progress" style="padding: 0 8px 4px">
            {{ state.progress[byStatus[col.key].find((t: any) => state.progress[t.id])?.id] }}
          </div>
          <button v-if="byStatus[col.key].length > CAP" class="rail-more"
            @click="state.boardOpen = true">
            …and {{ byStatus[col.key].length - CAP }} more — open the board ⛶
          </button>
        </template>
      </section>
      <div v-if="!tasks.length" class="empty" style="padding: 24px 10px; font-size: 12.5px">
        No cards yet — send an instruction in the chat.
      </div>
    </div>
  </aside>
</template>
