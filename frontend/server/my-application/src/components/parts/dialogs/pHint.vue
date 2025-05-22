<script setup>
import axios from 'axios'
import { ref,watch, onMounted ,computed} from 'vue'
import MathJaxComp from '@/components/methods/MathJax.vue'
import { markdownToHtml, reloadMathJax } from '@/components/methods/markdown.js'

// variable
const props = defineProps({
  title: String,
  dialog: Boolean,
  flow_session_id: Number,
  page: Number,
})
const use = ref(props.dialog)
const emit = defineEmits(["update:dialog"])
const text = ref()

// method
const setdialog = computed({
  get: () => props.dialog,
  set: (newVal) => emit('update:dialog', newVal)
})
const get_hint = () => {
  axios.get(`https://demo-fast-api-lms.vercel.app/get_flowpage_hint/${props.flow_session_id}/${props.page}`, {withCredentials: true}).then(function(response){
    // console.log(response.data)
    text.value = response.data.content
})}

// created
get_hint()

// mounted
onMounted(() => reloadMathJax())

// watch
watch(() => props.dialog, () => {
  use.value = props.dialog
  console.log('watch:' + use.value)
})
</script>

<template>
  <v-dialog  v-model = use opacity=0>
    <v-row justify = 'end'>
      <v-sheet width='500' height = '400' class ='custom-dialog' >
      <v-row class='my-10 mx-10 d-flex flex-row'>
        <h2 class='text-center'>{{ title }}</h2>
        <v-sheet class = 'ml-auto'>
          <v-btn size='x-small' class='mx-auto' icon='mdi-close' @click='use=false; setdialog=false'></v-btn>
        </v-sheet>
      </v-row>
      <v-row class='my-5 mx-5 d-flex flex-row'>
        <MathJaxComp>
          <div v-html='markdownToHtml(text)' />
        </MathJaxComp>
      </v-row>
      <!--v-sheet class='my-5 mx-10 d-flex justify-end'>
        <pDefaultBtn class='mt-4' text='閉じる'  @click='use = false; setdialog = false'/>
      </!--v-sheet-->
      </v-sheet>
    </v-row>
  </v-dialog>
</template>

<style scoped>
.custom-dialog{
  border: 2mm ridge #c5fa26;
  border-radius:8px;
  position : fixed;
  overflow: hidden;
  max-height: 250px; /* ダイアログ内のスクロール可能エリアの高さを指定 */
  overflow-y: auto;  /* 垂直方向にスクロール可能 */
  padding: 16px; /* ダイアログ全体はスクロールさせない */
}
</style>