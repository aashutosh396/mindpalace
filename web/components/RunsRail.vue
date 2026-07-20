<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { Repeat } from 'lucide-vue-next'
import { useWorkspace } from '../composables/useWorkspace'
import { md } from '../composables/md'

const { state } = useWorkspace()
const runs = ref<any[]>([])

async function load() {
  if (!state.runsFor) return
  const res = await fetch(`/api/routines/${state.runsFor.id}/runs`)
  runs.value = await res.json()
}

onMounted(load)
watch(() => state.runsFor?.id, load)
// a fire of THIS routine refreshes the list live
watch(() => state.routineRuns[0]?.id, () => {
  if (state.routineRuns[0]?.routine_id === state.runsFor?.id) load()
})
onUnmounted(() => { state.runsFor = null })

function tick(run: any) {
  return run.status === 'ok' ? '✓' : run.status === 'failed' ? '✗' : '…'
}

function tickClass(run: any) {
  return run.status === 'ok' ? 'ok' : run.status === 'failed' ? 'bad' : 'run'
}

function fmtRun(ts: number) {
  return new Date(ts * 1000).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>

<template>
  <aside class="board-rail runs-rail">
    <div class="rail-head">
      <Repeat :size="14" :stroke-width="1.75" />
      <span class="rail-title">{{ state.runsFor?.title }}</span>
      <button class="row-x" aria-label="Close run history" @click="state.runsFor = null">✕</button>
    </div>
    <div class="runs-list">
      <div v-if="!runs.length" class="side-empty" style="padding: 12px">
        No runs yet — first fire is at the next scheduled time.
      </div>
      <div v-for="run in runs" :key="run.id" class="run-card">
        <div class="run-card-head">
          <span class="rt-tick" :class="tickClass(run)">{{ tick(run) }}</span>
          <span class="run-card-when">{{ fmtRun(run.created_at) }}</span>
        </div>
        <div class="run-card-result" v-html="run.result ? md(run.result) : 'still running…'"></div>
      </div>
    </div>
  </aside>
</template>
