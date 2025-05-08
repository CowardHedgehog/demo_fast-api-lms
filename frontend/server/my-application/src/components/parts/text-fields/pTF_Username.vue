<script setup>
import { computed } from 'vue'
const props = defineProps({
  username: {type: String, default: ''},
  complete: {type: String, default: 'on'}
})
const emit = defineEmits(["update:username"])
const setUsername = computed({
  get: () => props.username,
  set: (newVal) => emit('update:username', newVal)
})
const rules = [
  v => !!v || 'ユーザー名を入力してください'
]

</script>

<template>
  <v-row class='align-center justify-center'>
    <v-text-field
      :rules="rules"
      label="ユーザー名"
      bg-color='white'
      v-model='setUsername'
      name='username'
      :autocomplete='complete'
    ></v-text-field>
  </v-row>
</template>