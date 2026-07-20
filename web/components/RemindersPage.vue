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

const editing = ref<any | null>(null)

function startEdit(r: any) {
  const d = new Date(r.due_at * 1000)
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
  editing.value = { id: r.id, text: r.text, when: d.toISOString().slice(0, 16) }
}

async function saveEdit() {
  if (!editing.value) return
  await remindersApi.update(editing.value.id, {
    text: editing.value.text,
    due_at: new Date(editing.value.when).getTime() / 1000
  })
  editing.value = null
  await remindersApi.list()
  toast('Reminder updated')
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
        <template v-if="editing?.id === r.id">
          <form class="rem-add" style="flex: 1" @submit.prevent="saveEdit">
            <input v-model="editing.text" aria-label="Reminder text" />
            <input v-model="editing.when" type="datetime-local" aria-label="When" />
            <button class="btn">Save</button>
            <button class="btn ghost" type="button" @click="editing = null">Cancel</button>
          </form>
        </template>
        <template v-else>
          <AlarmClock :size="14" :stroke-width="1.75" class="rem-ico" />
          <span class="rem-text">{{ r.text }}</span>
          <span class="rem-when">{{ fmt(r.due_at) }}</span>
          <button class="btn ghost" style="flex: none" @click="startEdit(r)">Edit</button>
          <button class="row-x" :aria-label="`Delete reminder: ${r.text}`" @click="remove(r)">✕</button>
        </template>
      </div>
    </div>
  </div>
</template>
