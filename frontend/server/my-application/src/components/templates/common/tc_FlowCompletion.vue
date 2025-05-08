<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MathJaxComp from '@/components/methods/MathJax.vue'
import { markdownToHtml, reloadMathJax } from '@/components/methods/markdown.js'


const router = useRouter()
const props = defineProps({
  create: {type: Boolean, default: false},
  course_id : {type: Number, required: true},
  week_id: {type: Number, required: true},
  flow_id: {type: Number, required: true},
  flow_session_id: {type: Number, required: true},
  
})
const flow_title = ref("")
const completion_page_content = ref("")

// function
const get_flow_info = () => {
  axios.get(`http://localhost:8000/get_flow_info/${props.flow_session_id}`, {withCredentials: true}).then(function(response){
    // console.log(response.data)
    flow_title.value = response.data.flow_title
})}
const get_flow_completion_page = () => {
  axios.get(`http://localhost:8000/get_flow_completion_page/${props.flow_id}`, {withCredentials: true}).then(function(response){
    // console.log(response)
    completion_page_content.value = response.data.content
})}
const move_to_flow_top = () => {
  if(props.create){ router.push({name: 'T_Flow', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id}})}
  else{             router.push({name: 'S_Flow', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id}})}
}

// created
get_flow_info()
get_flow_completion_page()

// onMounted
onMounted(() => reloadMathJax())
</script>

<template>
  <div>
    <h2>{{ flow_title }}</h2>
    <v-container class='mt-6'>
      <v-row>
        <MathJaxComp>
          <div v-html='markdownToHtml(completion_page_content)'/>
        </MathJaxComp>
      </v-row>
      <v-row class='mt-8'>
        <v-btn depressed color='primary' @click='move_to_flow_top()'>
          演習問題ページのトップに戻る
        </v-btn>
      </v-row>
    </v-container>
  </div>
</template>