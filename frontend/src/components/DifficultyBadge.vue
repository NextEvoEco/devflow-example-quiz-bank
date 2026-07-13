<script setup lang="ts">
defineProps<{ difficulty: string }>()
</script>

<template>
  <span class="badge" :class="`badge-${difficulty.toLowerCase()}`">{{ difficulty }}</span>
</template>
