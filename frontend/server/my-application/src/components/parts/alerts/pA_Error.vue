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
    color='error'
    icon='$error'
    style='white-space: pre-wrap;'
  >
  {{ message }}
  </v-alert>
</template>