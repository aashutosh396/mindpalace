<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { X, Square, Target } from 'lucide-vue-next'
import { useWorkspace, STATUSES, type Status } from '../composables/useWorkspace'

const { state, moveTask, replyTask, stopTask } = useWorkspace()
const trail = ref<HTMLElement>()
const reply = ref('')

async function sendReply() {
  const t2 = reply.value.trim()
  if (!t2) return
  reply.value = ''
  await replyTask(t.value.id, t2)
}

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
}, { immediate: true })
</script>

<template>
  <div class="sheet-backdrop" @click.self="state.modal = null">
    <div class="task-modal" role="dialog" :aria-label="`Card #${t.id}`">
      <div class="tm-head">
        <span class="status-pill" :style="{ '--c': COLORS[t.status] }">{{ LABELS[t.status] }}</span>
        <span v-if="t.kind === 'goal'" class="room-tag"><Target :size="11" :stroke-width="1.75" /> goal · iteration {{ t.iterations || 0 }}</span>
        <span v-if="state.modal!.room" class="room-tag">{{ state.modal!.room.name }}</span>
        <span class="tm-id">#{{ t.id }}</span>
        <button class="row-x" title="Close" aria-label="Close" @click="state.modal = null"><X :size="15" :stroke-width="1.75" /></button>
      </div>

      <h2 class="tm-title">{{ t.title }}</h2>
      <p v-if="t.body && t.body !== t.title" class="tm-body">{{ t.body }}</p>

      <div class="tm-cols">
        <div class="tm-left">
          <template v-if="t.result">
            <div class="tm-section">Result</div>
            <div class="tm-result">{{ t.result }}</div>
          </template>

          <template v-if="state.modal!.thread.length">
            <div class="tm-section">Follow-ups</div>
            <div class="tm-thread">
              <div v-for="m in state.modal!.thread" :key="m.id" class="tm-thread-msg" :class="m.role">
                <span class="who">{{ m.role === 'user' ? 'You' : 'Agent' }}</span>{{ m.text }}
              </div>
            </div>
          </template>

          <form class="tm-reply" @submit.prevent="sendReply">
            <input
              v-model="reply"
              :placeholder="t.status === 'in_progress' ? 'Working — wait for it to finish…' : 'Reply on this card — the agent continues the work'"
              :disabled="t.status === 'in_progress'"
              aria-label="Reply on card" />
            <button class="btn" :disabled="!reply.trim() || t.status === 'in_progress'">Send</button>
          </form>

          <div class="tm-actions">
            <button v-if="t.status === 'in_progress'" class="btn ghost stop-btn" @click="stopTask(t.id)">
              <Square :size="12" :stroke-width="2" /> Stop
            </button>
            <button v-if="nextOf(t.status)" class="btn ghost" @click="moveTask(t.id, nextOf(t.status)!)">
              → {{ LABELS[nextOf(t.status)!] }}
            </button>
            <button v-if="t.status !== 'done'" class="btn" @click="moveTask(t.id, 'done'); state.modal = null">
              Close card
            </button>
          </div>
        </div>

        <div class="tm-right">
          <div class="tm-section" style="margin-top: 0">The work</div>
          <div ref="trail" class="tm-trail">
            <div v-for="l in state.modal!.log" :key="l.id" class="tm-step"
              :class="{ marker: l.text.startsWith('—') }">
              <span class="tm-time">{{ fmtTime(l.created_at) }}</span>{{ l.text }}
            </div>
            <div v-if="!state.modal!.log.length" class="tm-step dim">
              {{ t.status === 'todo' ? 'Waiting for the worker to pick this up…' : 'No steps recorded.' }}
            </div>
            <div v-if="t.status === 'in_progress'" class="tm-step working">⚡ working…</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
