<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, sendChat } = useWorkspace()
const text = ref('')
const log = ref<HTMLElement>()
const LANES = [
  { key: 'auto', label: 'Auto', hint: 'I decide: work becomes a card, talk gets an answer' },
  { key: 'chat', label: '💬 Chat', hint: 'Just talk — never makes a card' },
  { key: 'task', label: '🎫 Ticket', hint: 'Always make a card on the board' }
] as const
const lane = ref<'auto' | 'chat' | 'task'>('auto')

async function send() {
  const t = text.value.trim()
  if (!t || !state.current) return
  text.value = ''
  await sendChat(t, lane.value)
}

function onKey(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() }
}

// stay pinned to the latest message — on new messages AND on opening a room
watch(() => [state.chat.length, state.awaitingReply, state.current?.id], async () => {
  await nextTick()
  log.value?.scrollTo({ top: log.value.scrollHeight })
})
</script>

<template>
  <aside class="corridor">
    <div class="corridor-head">
      The corridor
      <div class="corridor-sub">Speak an instruction — it becomes a card on the board.</div>
    </div>

    <div ref="log" class="chat-log">
      <div v-if="!state.chat.length" class="chat-hello">
        <span class="star">✳</span><template v-if="state.current">What shall we build?</template>
        <template v-else>Open a room to begin.</template>
        <div v-if="state.current" class="chat-hello-sub">
          Work becomes a card on the board · questions just get an answer
        </div>
      </div>
      <div v-for="m in state.chat" :key="m.id" class="msg" :class="m.role === 'user' ? 'user' : 'agent'">
        <div class="who">{{ m.role === 'user' ? 'You' : 'Agent' }}</div>
        <div class="bubble">{{ m.text }}</div>
        <div v-if="m.task_id" class="ticket">→ card #{{ m.task_id }}</div>
      </div>
      <div v-if="state.awaitingReply" class="msg agent">
        <div class="who">Agent</div>
        <div class="bubble writing">…</div>
      </div>
    </div>

    <form class="composer" @submit.prevent="send">
      <textarea
        v-model="text"
        :placeholder="state.current ? 'How can I help in this room?' : 'Open a room first'"
        :disabled="!state.current"
        aria-label="Instruction"
        @keydown="onKey"></textarea>
      <div class="composer-controls" role="radiogroup" aria-label="Message lane">
        <button
          v-for="l in LANES" :key="l.key" type="button"
          class="lane" :class="{ active: lane === l.key }"
          :title="l.hint" :aria-checked="lane === l.key" role="radio"
          @click="lane = l.key">{{ l.label }}</button>
        <button class="send" :disabled="!text.trim() || !state.current" title="Send" aria-label="Send">↑</button>
      </div>
    </form>
  </aside>
</template>
