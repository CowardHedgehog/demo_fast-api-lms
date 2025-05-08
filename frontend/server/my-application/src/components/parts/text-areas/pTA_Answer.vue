<script setup>
import { computed, onUpdated } from 'vue'
const props = defineProps({
  answer: {type: String, default: ''},
  label: {type: String, default: '解答を入力'}
})
const emit = defineEmits(["update:answer"])
const setAnswer = computed({
  get: () => props.answer,
  set: (newVal) => emit('update:answer', newVal)
})
const rules = [
  v => !!v || '',
]

//:rules='rules'
</script>

<template>
  <v-row class='align-center justify-center'>
    <v-textarea
      :label='label'
      bg-color='white'
      v-model='setAnswer'
    ></v-textarea>
  </v-row>
</template>