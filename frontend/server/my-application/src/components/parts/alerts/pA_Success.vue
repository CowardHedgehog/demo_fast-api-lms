<script setup>
const props = defineProps({
  message: {
    type: String,
    default: ''
  }
})
</script>

<template>
  <v-alert
    color='success'
    icon='$success'
    style='white-space: pre-wrap;'
  >
  {{ message }}
  </v-alert>
</template>