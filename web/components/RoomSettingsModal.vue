<script setup lang="ts">
import { ref } from 'vue'
import { X } from 'lucide-vue-next'
import { useWorkspace } from '../composables/useWorkspace'
import { ROOM_ICONS } from '../composables/icons'

const { state, updateRoom } = useWorkspace()
const room = state.roomSettings!
const name = ref(room.name)
const context = ref((room as any).context || '')
const icon = ref(room.icon || 'hash')

async function save() {
  await updateRoom(room.id, { name: name.value, icon: icon.value, context: context.value })
  state.roomSettings = null
}
</script>

<template>
  <div class="sheet-backdrop" @click.self="state.roomSettings = null">
    <div class="task-modal room-settings" role="dialog" :aria-label="`Settings — ${room.name}`">
      <div class="tm-head">
        <span class="rail-title">Room settings</span>
        <button class="row-x" title="Close" aria-label="Close" @click="state.roomSettings = null">
          <X :size="15" :stroke-width="1.75" />
        </button>
      </div>

      <div class="tm-section">Name</div>
      <input v-model="name" class="onboard-input" aria-label="Room name" @keydown.enter="save" />

      <div class="tm-section">Context</div>
      <textarea
        v-model="context" class="onboard-input" rows="3" maxlength="250" style="resize: none"
        placeholder="What is this room for? (~250 chars — helps the agent know what to do here)"
        aria-label="Room context"></textarea>

      <div class="tm-section">Icon</div>
      <div class="icon-grid" role="radiogroup" aria-label="Room icon">
        <button
          v-for="(comp, key) in ROOM_ICONS" :key="key"
          class="icon-cell" :class="{ active: icon === key }"
          role="radio" :aria-checked="icon === key" :aria-label="key" :title="key"
          @click="icon = key">
          <component :is="comp" :size="18" :stroke-width="1.75" />
        </button>
      </div>

      <div class="tm-actions">
        <button class="btn ghost" @click="state.roomSettings = null">Cancel</button>
        <button class="btn" :disabled="!name.trim()" @click="save">Save</button>
      </div>
    </div>
  </div>
</template>
