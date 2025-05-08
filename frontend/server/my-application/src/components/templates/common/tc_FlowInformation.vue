<script setup>
// import
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MathJaxComp from '@/components/methods/MathJax.vue'
import { markdownToHtml, reloadMathJax } from '@/components/methods/markdown.js'

// variable
const router = useRouter()
const props = defineProps({
  create: {type: Boolean, default: false},
  course_id: {type: Number, required: true},
  week_id: {type: Number, required: true},
  flow_id: {type: Number, required: true},
  previous: {type: Boolean, default: true}
})
const welcome_page_content = ref("")


const get_welcome_page_content = () => {
  axios.get(`http://localhost:8000/get_flow_welcome_page/${props.flow_id}`, {withCredentials: true}).then(function(response){
    welcome_page_content.value = response.data.content
  })
}
const move_week = () => {
  if(props.create){ router.push({name: 'T_Week', params: {course_id: props.course_id, week_id: props.week_id, page: 1}})}
  else{             router.push({name: 'S_Week', params: {course_id: props.course_id, week_id: props.week_id, page: 1}})}
}
const start_new_flow_session = () => {
  const params = {"flow_id": props.flow_id}
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  axios.post(`http://localhost:8000/start_new_flow_session`, params, config).then(function(response){
    console.log(response.data)
    if(response.data.start_success){
      if(props.create){ router.push({name:'T_FlowSession', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id, flow_session_id: response.data.flow_session_id, page: 1}})}
      else{             router.push({name:'S_FlowSession', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id, flow_session_id: response.data.flow_session_id, page: 1}})}
    }
})}

// created
get_welcome_page_content()

// onMounted
onMounted(() => reloadMathJax())
</script>

<template>
  <div>
    <MathJaxComp>
      <div v-html='markdownToHtml(welcome_page_content)' />
    </MathJaxComp>
    <v-row class='my-5'>
      <v-btn class='mr-10 bg-primary' @click='start_new_flow_session()'>演習問題を開始</v-btn>
      <v-btn class='bg-secondary' v-if='previous' @click='move_week()'>教科書ページに戻る</v-btn>
    </v-row>
  </div>
</template>