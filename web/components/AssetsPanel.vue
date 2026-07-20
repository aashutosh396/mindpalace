<script setup lang="ts">
import { ref } from 'vue'
import { useWorkspace } from '../composables/useWorkspace'

const { state, uploadAssets, deleteAsset } = useWorkspace()
const over = ref(false)
const input = ref<HTMLInputElement>()

function onDrop(e: DragEvent) {
  over.value = false
  if (e.dataTransfer?.files.length) uploadAssets(e.dataTransfer.files)
}

function onPick() {
  if (input.value?.files?.length) uploadAssets(input.value.files)
  if (input.value) input.value.value = ''
}

function fmtSize(n: number) {
  if (n > 1e6) return (n / 1e6).toFixed(1) + ' MB'
  if (n > 1e3) return (n / 1e3).toFixed(0) + ' KB'
  return n + ' B'
}

function fmtDate(ts: number) {
  return new Date(ts * 1000).toLocaleDateString()
}
</script>

<template>
  <div class="panel">
    <div
      class="dropzone" :class="{ over }"
      @dragover.prevent="over = true"
      @dragleave="over = false"
      @drop.prevent="onDrop"
      @click="input?.click()"
      role="button" tabindex="0"
      @keydown.enter="input?.click()">
      <input ref="input" type="file" multiple hidden aria-label="Upload assets" @change="onPick" />
      Drop files here, or click to choose.
      <div class="dz-sub">Everything you put on this shelf is visible to the agent when it works a ticket.</div>
    </div>

    <div v-for="a in state.assets" :key="a.id" class="panel-row">
      <a class="path" :href="`/api/assets/${a.id}/download`">{{ a.filename }}</a>
      <span class="dim">{{ fmtSize(a.size) }} · {{ fmtDate(a.uploaded_at) }}</span>
      <button class="row-x" title="Delete asset" @click="deleteAsset(a.id)">✕</button>
    </div>

    <div v-if="!state.assets.length" class="empty">
      <span class="glyph">—</span>
      <p>The shelf is empty. Drop briefs, designs, or exports above —
      the agent reads them while working this room's tickets.</p>
    </div>
  </div>
</template>
