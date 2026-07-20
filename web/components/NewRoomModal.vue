<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { X } from 'lucide-vue-next'
import { useWorkspace } from '../composables/useWorkspace'

const { state, createRoom } = useWorkspace()
const name = ref('')
const context = ref('')
const nameInput = ref<HTMLInputElement>()

onMounted(() => nameInput.value?.focus())

async function create() {
  if (!name.value.trim()) return
  const n = name.value.trim()
  const c = context.value.trim()
  state.createRoomOpen = false
  await createRoom(n, c)
}
</script>

<template>
  <div class="sheet-backdrop" @click.self="state.createRoomOpen = false">
    <form class="task-modal room-settings" role="dialog" aria-label="New chatroom" @submit.prevent="create">
      <div class="tm-head">
        <span class="rail-title">New chatroom</span>
        <button class="row-x" type="button" title="Close" aria-label="Close" @click="state.createRoomOpen = false">
          <X :size="15" :stroke-width="1.75" />
        </button>
      </div>

      <div class="tm-section">Name</div>
      <input ref="nameInput" v-model="name" class="onboard-input" placeholder="e.g. saauzi, blog, client-x"
        aria-label="Chatroom name" />

      <div class="tm-section">Context</div>
      <textarea
        v-model="context" class="onboard-input" rows="3" maxlength="250" style="resize: none"
        placeholder="What is this room for? (~250 chars — helps the agent know what to attach and do here)"
        aria-label="Room context"></textarea>

      <div class="tm-actions">
        <button class="btn ghost" type="button" @click="state.createRoomOpen = false">Cancel</button>
        <button class="btn" :disabled="!name.trim()">Create</button>
      </div>
    </form>
  </div>
</template>
