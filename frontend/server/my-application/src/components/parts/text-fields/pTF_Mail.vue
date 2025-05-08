<script setup>
import { computed } from 'vue'
const props = defineProps({
  email: {type: String, default: ''}
})
const emit = defineEmits(["update:email"])
const setEmail = computed({
  get: () => props.email,
  set: (newVal) => emit('update:email', newVal)
})
const rules = [
  v => !!v || 'メールアドレスを入力してください',
  v => /.+@.+\..+/.test(v) || 'メールアドレスが正しくありません'
]

</script>

<template>
  <v-row class='align-center justify-center'>
    <v-text-field
      :rules="rules"
      label="メールアドレス"
      bg-color='white'
      autocomplete='on'
      v-model='setEmail'
      name='email'
    ></v-text-field>
  </v-row>
</template>