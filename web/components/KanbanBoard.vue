<script setup lang="ts">
import { computed, ref } from 'vue'
import { useWorkspace, STATUSES, type Status } from '../composables/useWorkspace'

const { state, moveTask, openTask } = useWorkspace()

const COLS: { key: Status; label: string; color: string }[] = [
  { key: 'todo', label: 'To do', color: 'var(--slate)' },
  { key: 'in_progress', label: 'In progress', color: 'var(--brass)' },
  { key: 'review', label: 'Review', color: 'var(--lilac)' },
  { key: 'done', label: 'Done', color: 'var(--sage)' }
]

const tasks = computed<any[]>(() => state.current ? state.tasks : state.allTasks)
const byStatus = computed(() =>
  Object.fromEntries(STATUSES.map(s => [s, tasks.value.filter((t: any) => t.status === s)])))

const dragOver = ref<Status | null>(null)

function onDrop(status: Status, e: DragEvent) {
  dragOver.value = null
  const id = Number(e.dataTransfer?.getData('text/task-id'))
  if (id) moveTask(id, status)
}

// Card buttons cover what drag-and-drop does, for keyboard and touch use.
function nextOf(s: Status): Status | null {
  const i = STATUSES.indexOf(s)
  return i < STATUSES.length - 1 ? STATUSES[i + 1] : null
}
</script>

<template>
  <div class="board">
    <section
      v-for="col in COLS" :key="col.key"
      class="col" :class="{ 'drop-over': dragOver === col.key }"
      @dragover.prevent="dragOver = col.key"
      @dragleave="dragOver = null"
      @drop="onDrop(col.key, $event)">
      <header class="col-head">
        <span class="dot" :style="{ background: col.color }"></span>
        {{ col.label }}
        <span class="n">{{ byStatus[col.key].length }}</span>
      </header>
      <div class="col-cards">
        <article
          v-for="t in byStatus[col.key]" :key="t.id"
          class="card" :class="{ arriving: state.arrived.has(t.id) }"
          :style="{ '--status': col.color }"
          draggable="true"
          @click="openTask(t.id)"
          @dragstart="$event.dataTransfer?.setData('text/task-id', String(t.id))">
          <span v-if="!state.current && t.room_name" class="room-tag">{{ t.room_name }}</span>
          <div class="card-title">{{ t.title }}</div>
          <div class="card-meta">
            <span>#{{ t.id }}</span>
            <span>{{ t.created_by }}</span>
          </div>
          <div v-if="t.status === 'in_progress' && state.progress[t.id]" class="card-progress">
            {{ state.progress[t.id] }}
          </div>
          <div v-if="t.result" class="card-result">{{ t.result }}</div>
          <div class="card-actions">
            <button v-if="nextOf(t.status)" @click.stop="moveTask(t.id, nextOf(t.status)!)">
              → {{ COLS.find(c => c.key === nextOf(t.status))?.label }}
            </button>
            <button v-if="t.status !== 'done'" @click.stop="moveTask(t.id, 'done')">Close</button>
          </div>
        </article>
        <div v-if="!byStatus[col.key].length" class="empty" style="padding: 18px 8px; font-size: 12.5px">
          <template v-if="col.key === 'todo'">Type an instruction in the corridor →</template>
          <template v-else>Empty</template>
        </div>
      </div>
    </section>
  </div>
</template>
