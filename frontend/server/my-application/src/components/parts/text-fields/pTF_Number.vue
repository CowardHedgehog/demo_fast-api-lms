<script setup>
import { computed, watch } from 'vue'
const props = defineProps({
  num: {type: String, default: ''},
  label: {type: String, default: ''},
  hint: {type: String, default: ''}
})
const emit = defineEmits(["update:num"])
const setNum = computed({
  get: () => props.num,
  set: (newVal) => emit('update:num', newVal.replace(/\D/g, ''))
})
const rules = [
  v => !!v || '',
]


//:rules='rules'
</script>

<template>
  <v-col>
    <v-text-field
      :rules='rules'
      :label='label'
      :hint='hint'
      bg-color='white'
      v-model='setNum'
      autocomplete='off'
      type='number'
      class='no-spin'
    ></v-text-field>
  </v-col>
</template>

<style>
.no-spin::-webkit-inner-spin-button,
.no-spin::-webkit-outer-spin-button {
  -webkit-appearance: none !important;
  margin: 0 !important;
  -moz-appearance: textfield !important;
}
</style>