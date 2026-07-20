<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'
import { md } from '../composables/md'

const { state, open, loadOlderChat } = useWorkspace()
const log = ref<HTMLElement>()

const msgs = computed<any[]>(() => state.current ? state.chat : state.homeChat)

function roomOf(m: any) {
  return state.rooms.find(r => r.id === m.ref_room_id)
}

function msgTime(ts: number) {
  const d = new Date(ts * 1000)
  const sameDay = new Date().toDateString() === d.toDateString()
  return sameDay
    ? d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    : d.toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

// The kitchen spinner from the Discord days: a cook-verb that rotates while
// the agent works, plus how long it's been at it. Random start so every turn
// opens on a different word.
const COOK_VERBS = [
  'Simmering', 'Fermenting', 'Marinating', 'Whisking', 'Kneading', 'Reducing',
  'Proofing', 'Basting', 'Caramelizing', 'Plating', 'Seasoning', 'Sautéing',
  'Folding', 'Searing', 'Glazing', 'Braising', 'Tasting', 'Stirring'
]
const waitSecs = ref(0)
const verbOffset = ref(0)
let waitTimer: ReturnType<typeof setInterval> | null = null

const cookLine = computed(() => {
  const verb = COOK_VERBS[(Math.floor(waitSecs.value / 4) + verbOffset.value) % COOK_VERBS.length]
  return `${verb}… ${waitSecs.value}s`
})

watch(() => state.awaitingReply, (on) => {
  if (waitTimer) { clearInterval(waitTimer); waitTimer = null }
  if (on) {
    waitSecs.value = 0
    verbOffset.value = Math.floor(Math.random() * COOK_VERBS.length)
    waitTimer = setInterval(() => { waitSecs.value++ }, 1000)
  }
}, { immediate: true })

// Keyed on the LAST message id: new messages scroll to bottom, but prepending
// an older page (scroll-up pagination) doesn't yank the view down.
watch(() => [msgs.value[msgs.value.length - 1]?.id, state.awaitingReply, state.current?.id], async () => {
  await nextTick()
  log.value?.scrollTo({ top: log.value.scrollHeight })
}, { immediate: true })

const holdOlder = ref(false)                     // keeps the badge up through the hold

async function onScroll() {
  const el = log.value
  if (!el || el.scrollTop > 60 || state.chatOlderLoading || holdOlder.value) return
  if (state.current ? state.chatDone : state.homeChatDone) return   // no older pages
  const anchorId = msgs.value[0]?.id               // the message the reader is at
  if (!anchorId) return
  holdOlder.value = true
  // small deliberate hold so the badge reads and the page settles before more scrolling
  const [added] = await Promise.all([loadOlderChat(), new Promise(r => setTimeout(r, 2000))])
  if (added) {
    await nextTick()
    const anchor = el.querySelector(`[data-mid="${anchorId}"]`) as HTMLElement | null
    if (anchor) {                                  // pin the exact message — no jumping
      el.scrollTop = anchor.getBoundingClientRect().top - el.getBoundingClientRect().top
        + el.scrollTop - 54
    }
  }
  holdOlder.value = false
}
</script>

<template>
  <aside class="corridor">
    <div ref="log" class="chat-log" @scroll.passive="onScroll">
      <div class="chat-inner">
      <div v-if="state.chatOlderLoading || holdOlder" class="chat-older">
        <span class="chat-older-badge"><span class="chat-older-dot"></span> loading earlier…</span>
      </div>
      <div v-if="!msgs.length" class="chat-hello">
        <span class="star"><Logo :size="30" /></span><template v-if="state.current">What shall we build?</template>
        <template v-else>What's on your mind?</template>
        <div class="chat-hello-sub">
          <template v-if="state.current">Work becomes a card on the board · questions just get an answer</template>
          <template v-else>Just talk — I'll answer, or file work into your rooms (I never make rooms; those are yours)</template>
        </div>
      </div>
      <div v-for="m in msgs" :key="m.id" :data-mid="m.id" class="msg"
        :class="m.role === 'user' ? 'user' : m.role === 'brief' ? 'brief' : 'agent'">
        <div class="who">{{ m.role === 'user' ? 'You' : m.role === 'brief' ? 'The palace' : state.agentName }}
          <span class="when">{{ msgTime(m.created_at) }}</span></div>
        <div class="bubble" v-html="md(m.text)"></div>
        <div v-if="m.task_id" class="ticket">
          → card #{{ m.task_id }}
          <template v-if="!state.current && roomOf(m)">
            in <a class="room-link" href="#" @click.prevent="open(roomOf(m)!)">{{ roomOf(m)!.name }}</a>
          </template>
        </div>
      </div>
      <div v-if="state.awaitingReply" class="msg agent">
        <div class="who">{{ state.agentName }}</div>
        <div class="bubble writing cook">
          <span class="cook-star"><Logo :size="13" /></span> {{ cookLine }}
        </div>
      </div>
      </div>
    </div>
  </aside>
</template>
