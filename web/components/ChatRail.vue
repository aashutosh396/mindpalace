<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, open } = useWorkspace()
const log = ref<HTMLElement>()

const msgs = computed<any[]>(() => state.current ? state.chat : state.homeChat)

function roomOf(m: any) {
  return state.rooms.find(r => r.id === m.ref_room_id)
}

watch(() => [msgs.value.length, state.awaitingReply, state.current?.id], async () => {
  await nextTick()
  log.value?.scrollTo({ top: log.value.scrollHeight })
})
</script>

<template>
  <aside class="corridor">
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
  </aside>
</template>
