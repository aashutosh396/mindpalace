<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, sendChat, sendHomeChat, open } = useWorkspace()
const text = ref('')
const log = ref<HTMLElement>()
const LANES = [
  { key: 'auto', label: 'Auto', hint: 'I decide: work becomes a card, talk gets an answer' },
  { key: 'chat', label: '💬 Chat', hint: 'Just talk — never makes a card' },
  { key: 'task', label: '🎫 Ticket', hint: 'Always make a card on the board' },
  { key: 'goal', label: '🎯 Goal', hint: 'A card that iterates until the goal is truly done' }
] as const
const lane = ref<'auto' | 'chat' | 'task' | 'goal'>('auto')

const msgs = computed<any[]>(() => state.current ? state.chat : state.homeChat)

function roomOf(m: any) {
  return state.rooms.find(r => r.id === m.ref_room_id)
}

async function send() {
  const t = text.value.trim()
  if (!t) return
  text.value = ''
  if (state.current) await sendChat(t, lane.value)
  else await sendHomeChat(t)
}

function onKey(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() }
}

// stay pinned to the latest message — on new messages AND on switching views
watch(() => [msgs.value.length, state.awaitingReply, state.current?.id], async () => {
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
      <div v-if="!msgs.length" class="chat-hello">
        <span class="star">✳</span><template v-if="state.current">What shall we build?</template>
        <template v-else>What's on your mind?</template>
        <div class="chat-hello-sub">
          <template v-if="state.current">Work becomes a card on the board · questions just get an answer</template>
          <template v-else>Just talk — I'll answer, or file work into your rooms (I never make rooms; those are yours)</template>
        </div>
      </div>
      <div v-for="m in msgs" :key="m.id" class="msg"
        :class="m.role === 'user' ? 'user' : m.role === 'brief' ? 'brief' : 'agent'">
        <div class="who">{{ m.role === 'user' ? 'You' : m.role === 'brief' ? 'The palace' : 'Agent' }}</div>
        <div class="bubble">{{ m.text }}</div>
        <div v-if="m.task_id" class="ticket">
          → card #{{ m.task_id }}
          <template v-if="!state.current && roomOf(m)">
            in <a class="room-link" href="#" @click.prevent="open(roomOf(m)!)">{{ roomOf(m)!.name }}</a>
          </template>
        </div>
      </div>
      <div v-if="state.awaitingReply" class="msg agent">
        <div class="who">Agent</div>
        <div class="bubble writing">…</div>
      </div>
    </div>

    <form class="composer" @submit.prevent="send">
      <textarea
        v-model="text"
        :placeholder="state.current ? 'How can I help in this room?' : 'Tell me anything — I\'ll route it to the right room'"
        aria-label="Instruction"
        @keydown="onKey"></textarea>
      <div class="composer-controls" role="radiogroup" aria-label="Message lane">
        <template v-if="state.current">
          <button
            v-for="l in LANES" :key="l.key" type="button"
            class="lane" :class="{ active: lane === l.key }"
            :title="l.hint" :aria-checked="lane === l.key" role="radio"
            @click="lane = l.key">{{ l.label }}</button>
        </template>
        <span v-else class="lane active" style="cursor: default" title="The concierge decides: answer, file into one of your rooms, or hand palace chores to the keeper">🏛 Concierge</span>
        <button class="send" :disabled="!text.trim()" title="Send" aria-label="Send">↑</button>
      </div>
    </form>
  </aside>
</template>
