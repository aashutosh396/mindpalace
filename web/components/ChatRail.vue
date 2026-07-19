<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, sendChat } = useWorkspace()
const text = ref('')
const log = ref<HTMLElement>()

async function send() {
  const t = text.value.trim()
  if (!t || !state.current) return
  text.value = ''
  await sendChat(t)
}

function onKey(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() }
}

watch(() => state.chat.length, async () => {
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
      <div v-if="!state.chat.length" class="empty" style="margin-top: 30%">
        <span class="glyph">✒️</span>
        <p v-if="state.current">Nothing said in this room yet.</p>
        <p v-else>Open a room to start talking.</p>
      </div>
      <div v-for="m in state.chat" :key="m.id" class="msg" :class="{ user: m.role === 'user' }">
        <div class="who">{{ m.role === 'user' ? 'You' : 'Agent' }}</div>
        <div class="bubble">{{ m.text }}</div>
        <div v-if="m.task_id" class="ticket">→ card #{{ m.task_id }}</div>
      </div>
    </div>

    <form class="chat-input" @submit.prevent="send">
      <textarea
        v-model="text"
        :placeholder="state.current ? 'Fix the login bug on the dashboard…' : 'Open a room first'"
        :disabled="!state.current"
        aria-label="Instruction"
        @keydown="onKey"></textarea>
      <button class="btn" :disabled="!text.trim() || !state.current">Send</button>
    </form>
  </aside>
</template>
