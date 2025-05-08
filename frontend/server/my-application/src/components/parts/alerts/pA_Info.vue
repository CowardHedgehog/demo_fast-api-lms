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
    color='secondary'
    closable
  >
  {{ message }}
  </v-alert>
</template>