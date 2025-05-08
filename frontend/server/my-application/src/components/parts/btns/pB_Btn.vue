<script setup>
const props = defineProps({
  text: String,
  position: String,
  loading: Boolean
})
const emit = defineEmits(['func'])

const func = () => emit('func')
</script>

<template>
  <v-row class='align-center justify-center' v-if='position==="center"'>
    <v-btn :loading='loading' depressed color="primary" @click='func'>{{ text }}</v-btn>
  </v-row>
  <v-row class='align-end justify-end' v-else-if='position==="end-end"'>
    <v-btn :loading='loading' depressed color="primary" @click='func'>{{ text }}</v-btn>
  </v-row>
  <v-row class='align-center justify-end' v-else-if='position==="right-center"'>
    <v-btn :loading='loading' depressed color="primary" @click='func'>{{ text }}</v-btn>
  </v-row>
  <div v-else>
    <v-btn :loading='loading' depressed color="primary" @click='func'>{{ text }}</v-btn>
  </div>
</template>