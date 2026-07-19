<script setup lang="ts">
import { useWorkspace } from '../composables/useWorkspace'

const { state } = useWorkspace()

function fmtSize(n: number) {
  if (n > 1e6) return (n / 1e6).toFixed(1) + ' MB'
  if (n > 1e3) return (n / 1e3).toFixed(0) + ' KB'
  return n + ' B'
}
</script>

<template>
  <div class="panel">
    <div v-for="a in state.assets" :key="a.id" class="panel-row">
      <span class="path">{{ a.filename }}</span>
      <span class="dim">{{ fmtSize(a.size) }}</span>
    </div>
    <div v-if="!state.assets.length" class="empty">
      <span class="glyph">🗄</span>
      <p>No assets in this room yet. Uploads arrive here in the next build —
      everything the agent should see (briefs, designs, exports) will live in this shelf.</p>
    </div>
  </div>
</template>
