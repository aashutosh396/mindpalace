<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { Moon, Sun } from 'lucide-vue-next'
import { useWorkspace } from '../composables/useWorkspace'

const { state } = useWorkspace()
const dark = ref(false)

onMounted(() => {
  dark.value = localStorage.getItem('theme') === 'dark'
  apply()
})

function apply() {
  document.documentElement.dataset.theme = dark.value ? 'dark' : 'light'
}

function toggleTheme() {
  dark.value = !dark.value
  localStorage.setItem('theme', dark.value ? 'dark' : 'light')
  apply()
}
</script>

<template>
  <div class="side-user">
    <div class="avatar"><Logo :size="15" /></div>
    <div class="side-user-meta">
      <div class="name">mindpalace</div>
      <div class="plan">
        <span :style="{ color: state.connected ? 'var(--sage)' : 'var(--danger)' }">●</span>
        {{ state.connected ? 'live' : 'reconnecting…' }}
        <template v-if="state.health"> · {{ state.health.commit.slice(0, 7) }}</template>
      </div>
    </div>
    <button class="theme-toggle" :title="dark ? 'Switch to light' : 'Switch to dark'" aria-label="Toggle theme"
      @click="toggleTheme"><Sun v-if="dark" :size="15" :stroke-width="1.75" /><Moon v-else :size="15" :stroke-width="1.75" /></button>
  </div>
</template>
