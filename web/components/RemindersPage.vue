<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { AlarmClock } from 'lucide-vue-next'
import { useWorkspace } from '../composables/useWorkspace'

const { state, remindersApi, toast } = useWorkspace()

const text = ref('')
const when = ref('')

onMounted(() => remindersApi.list())

async function add() {
  if (!text.value.trim() || !when.value) return
  const due = new Date(when.value).getTime() / 1000
  await remindersApi.add(text.value.trim(), due)
  text.value = ''; when.value = ''
  await remindersApi.list()
  toast('Reminder set')
}

async function remove(r: any) {
  await remindersApi.remove(r.id)
  await remindersApi.list()
}

function fmt(ts: number) {
  return new Date(ts * 1000).toLocaleString([], {
    weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
  })
}
</script>

<template>
  <div class="main-body">
    <div class="panel">
      <form class="rem-add page" @submit.prevent="add">
        <input v-model="text" placeholder="Remind me to…" aria-label="Reminder text" />
        <input v-model="when" type="datetime-local" aria-label="When" />
        <button class="btn" :disabled="!text.trim() || !when">Set</button>
      </form>

      <div v-if="!state.reminders.length" class="side-empty" style="padding: 18px 4px">
        No reminders — set one above, or just tell {{ state.agentName }} in Home:
        “remind me tomorrow at 9 to call the bank”.
      </div>

      <div v-for="r in state.reminders" :key="r.id" class="panel-row rem-row">
        <AlarmClock :size="14" :stroke-width="1.75" class="rem-ico" />
        <span class="rem-text">{{ r.text }}</span>
        <span class="rem-when">{{ fmt(r.due_at) }}</span>
        <button class="row-x" :aria-label="`Delete reminder: ${r.text}`" @click="remove(r)">✕</button>
      </div>
    </div>
  </div>
</template>
