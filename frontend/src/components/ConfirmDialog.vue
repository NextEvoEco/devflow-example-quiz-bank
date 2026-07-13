<script setup lang="ts">
defineProps<{
  open: boolean
  title: string
  message: string
}>()

defineEmits<{
  cancel: []
  confirm: []
}>()
</script>

<template>
  <div v-if="open" class="modal-backdrop" @click.self="$emit('cancel')">
    <div class="modal modal-sm" role="dialog" aria-modal="true" :aria-label="title">
      <div class="modal-body confirm-body">
        <div class="empty-icon" aria-hidden="true">!</div>
        <h2>{{ title }}</h2>
        <p>{{ message }}</p>
      </div>
      <footer class="modal-footer">
        <button type="button" class="btn btn-secondary" @click="$emit('cancel')">Cancel</button>
        <button type="button" class="btn btn-danger" @click="$emit('confirm')">Delete</button>
      </footer>
    </div>
  </div>
</template>
