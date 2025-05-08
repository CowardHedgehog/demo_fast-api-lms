<script setup>
// import
import { computed } from 'vue'

// variable
const props = defineProps({
  week_name: {
    type: String,
    default: ''
  }
})
const emit = defineEmits(["update:week_name"])
const rules = [
  v => !!v || 'コンテンツ名は必須です.'
]

// function
const setCourseName = computed({
  get: () => props.week_name,
  set: (newVal) => emit('update:week_name', newVal)
})

// created

</script>

<template>
  <v-row class='align-center justify-space-around'>
    <v-text-field
      :rules="rules"
      label="コンテンツ名"
      bg-color='white'
      v-model='setCourseName'
    ></v-text-field>
  </v-row>
</template>