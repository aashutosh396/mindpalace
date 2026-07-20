<script setup lang="ts">
import { AlarmClock, Repeat } from 'lucide-vue-next'
import { useWorkspace } from '../composables/useWorkspace'

const { state, openTool } = useWorkspace()
</script>

<template>
  <div class="sheet-backdrop" @click.self="state.toolsOpen = false">
    <div class="modal tools-modal" role="dialog" aria-label="Tools">
      <div class="tm-head">
        <span class="tm-title">Tools</span>
        <button class="row-x" aria-label="Close tools" @click="state.toolsOpen = false">✕</button>
      </div>
      <div class="tool-grid">
        <button class="tool-tile" @click="openTool('reminders')">
          <AlarmClock :size="20" :stroke-width="1.75" />
          <span class="tool-name">Reminders</span>
        </button>
        <button class="tool-tile" @click="openTool('routines')">
          <Repeat :size="20" :stroke-width="1.75" />
          <span class="tool-name">Routines</span>
        </button>
      </div>
    </div>
  </div>
</template>
