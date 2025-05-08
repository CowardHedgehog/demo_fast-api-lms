<script setup>
import { ref } from 'vue'

const props = defineProps({
  title: String,
  text: String,
  dialog: Boolean,
})
const use = ref(props.dialog)


</script>

<template>
  <v-dialog v-model = use>
    <v-sheet width='800' class='mx-auto'>
      <v-sheet class='my-10 mx-10 justify-center'>
        <h2 class='text-center'>{{ title }}</h2>
        <p class='text-center'>{{ text }}</p>
        <pDefaultBtn class='mt-4' text='閉じる' position='center' @click='use = false'/>
      </v-sheet>
    </v-sheet>
  </v-dialog>
</template>