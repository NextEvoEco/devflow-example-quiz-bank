<script setup lang="ts">
defineProps<{
  heading: string
  message: string
  actionLabel?: string
}>()

defineEmits<{ action: [] }>()
</script>

<template>
  <div class="empty-state">
    <div class="empty-icon" aria-hidden="true">?</div>
    <h2>{{ heading }}</h2>
    <p>{{ message }}</p>
    <button v-if="actionLabel" type="button" class="btn btn-primary" @click="$emit('action')">
      {{ actionLabel }}
    </button>
  </div>
</template>
