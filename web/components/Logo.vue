<script setup lang="ts">
// The mindpalace mark: a palace gate — an arch within an arch over the
// ground line. Inherits color (currentColor) so it works in any context.
defineProps({ size: { type: Number, default: 16 } })
</script>

<template>
  <svg
    :width="size" :height="size" viewBox="0 0 24 24" fill="none"
    stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    aria-hidden="true" class="mp-logo">
    <path d="M4.5 20v-8.5a7.5 7.5 0 0 1 15 0V20" />
    <path d="M9.5 20v-5a2.5 2.5 0 0 1 5 0v5" />
    <path d="M2.5 20h19" />
  </svg>
</template>
