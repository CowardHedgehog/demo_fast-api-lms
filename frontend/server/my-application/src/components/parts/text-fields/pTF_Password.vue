<script setup>
import { ref, computed } from 'vue'
const props = defineProps({
  password: {type: String, default: ''},
  label: {type: String, default: 'パスワード'},
  name: {type: String, default: 'password'},
  complete: {type: String, default: 'on'}
})
const pswd = ref(false)
const emit = defineEmits(["update:password"])
const setPassword = computed({
  get: () => props.password,
  set: (newVal) => emit('update:password', newVal)
})
const rules = [
  value => !!value || 'パスワードを入力してください',
]
</script>

<template>
  <v-row class='align-center justify-center'>
    <form @submit.prevent class='w-100'>
      <v-text-field 
        :append-icon="pswd ? 'mdi-eye' : 'mdi-eye-off'"
        :rules="rules" 
        :type="pswd ? 'text' : 'password'"
        :label='label'
        :name='name'
        class="input-group--focused"
        bg-color='white'
        @click:append="pswd = !pswd"
        :autocomplete='complete'
        v-model="setPassword"
      ></v-text-field>
    </form>
  </v-row>
</template>