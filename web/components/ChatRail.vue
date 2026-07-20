<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, open, loadOlderChat } = useWorkspace()
const log = ref<HTMLElement>()

const msgs = computed<any[]>(() => state.current ? state.chat : state.homeChat)

function roomOf(m: any) {
  return state.rooms.find(r => r.id === m.ref_room_id)
}

// Keyed on the LAST message id: new messages scroll to bottom, but prepending
// an older page (scroll-up pagination) doesn't yank the view down.
watch(() => [msgs.value[msgs.value.length - 1]?.id, state.awaitingReply, state.current?.id], async () => {
  await nextTick()
  log.value?.scrollTo({ top: log.value.scrollHeight })
}, { immediate: true })

async function onScroll() {
  const el = log.value
  if (!el || el.scrollTop > 60 || state.chatOlderLoading) return
  const prevHeight = el.scrollHeight
  const added = await loadOlderChat()
  if (!added) return
  await nextTick()
  el.scrollTop += el.scrollHeight - prevHeight   // keep the view anchored
}
</script>

<template>
  <aside class="corridor">
    <div ref="log" class="chat-log" @scroll.passive="onScroll">
      <div class="chat-inner">
      <div v-if="state.chatOlderLoading" class="chat-older">loading earlier…</div>
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
        <div class="who">{{ m.role === 'user' ? 'You' : m.role === 'brief' ? 'The palace' : state.agentName }}</div>
        <div class="bubble">{{ m.text }}</div>
        <div v-if="m.task_id" class="ticket">
          → card #{{ m.task_id }}
          <template v-if="!state.current && roomOf(m)">
            in <a class="room-link" href="#" @click.prevent="open(roomOf(m)!)">{{ roomOf(m)!.name }}</a>
          </template>
        </div>
      </div>
      <div v-if="state.awaitingReply" class="msg agent">
        <div class="who">{{ state.agentName }}</div>
        <div class="bubble writing">…</div>
      </div>
      </div>
    </div>
  </aside>
</template>
