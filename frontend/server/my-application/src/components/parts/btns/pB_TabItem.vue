<script setup>
const props = defineProps({
  page: String,
  location: String,
  tabName: String,
  move: Function,
})
</script>

<template>
  <v-col cols='2'>
    <div v-if='location === page'>
      <v-btn block disabled color='secondary'>
        {{ tabName }}
      </v-btn>
    </div>
    <div v-if='location != page'>
      <v-btn block @click='move'>
        {{ tabName }}
      </v-btn>
    </div>
  </v-col>
  
</template>