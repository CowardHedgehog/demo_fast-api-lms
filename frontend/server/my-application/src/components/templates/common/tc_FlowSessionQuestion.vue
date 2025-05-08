<script setup>
// import
import { ref, watch, shallowRef } from 'vue'
import { onBeforeRouteUpdate, useRouter } from 'vue-router'
import axios from 'axios'
import { markdownToHtml, reloadMathJax } from '@/components/methods/markdown.js'
//import SimplePage from '@/components/templates/pages/SimplePage.vue'
import SingleTextQuestion from '@/components/templates/pages/SingleTextQuestion.vue'
import MultipleTextQuestion from '@/components/templates/pages/MultipleTextQuestion.vue'
import ChoiceQuestion from '@/components/templates/pages/ChoiceQuestion.vue'
import DescriptiveTextQuestion from '@/components/templates/pages/DescriptiveTextQuestion.vue'
import pHint from '@/components/parts/dialogs/pHint.vue'

// variable
const router = useRouter()
const props = defineProps({
  create:           {type: Boolean, default: false},
  course_id:        {type: Number, required: true},
  week_id:          {type: Number, required: true},
  flow_id:          {type: Number, required: true},
  flow_session_id:  {type: Number, required: true},
  page:             {type: Number, required: true},
  num_of_pages:     {type: Number, required: true},
})
const flowpage = ref()
const page_content = ref({})
const component = shallowRef()
const answer_comment = ref("")
const blank_answers = ref([])
const dialog = ref(false)
const page_type = shallowRef({'SingleTextQuestion': SingleTextQuestion, 'MultipleTextQuestion': MultipleTextQuestion, 'ChoiceQuestion': ChoiceQuestion, 'DescriptiveTextQuestion': DescriptiveTextQuestion})

// function
const get_flowpage = (page_i) => {
  axios.get(`http://localhost:8000/get_flowpage/${props.flow_session_id}/${page_i}`, {withCredentials: true}).then(function(response){
    console.log(response.data)
    flowpage.value = response.data
    page_content.value = response.data.page_content
    component.value = page_type.value[response.data.page_type]
    answer_comment.value = response.data.answer_comment
  })
}
const get_blank_answer = (page_i) => {
  axios.get(`http://localhost:8000/get_blank_answer/${props.flow_session_id}/${page_i}`, {withCredentials: true}).then(function(response){
    // console.log(response.data)
    blank_answers.value = response.data
  })
}
const update_data = (page_i) => {
  get_flowpage(page_i)
  get_blank_answer(page_i)
  dialog.value = false
}
const go_previous_page = () => {
  if(props.create){ router.push({name: 'T_FlowSession', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id, flow_session_id: props.flow_session_id, page: props.page-1}})}
  else{             router.push({name: 'S_FlowSession', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id, flow_session_id: props.flow_session_id, page: props.page-1}})}
}
const go_next_page = () => {
  if(props.create){ router.push({name: 'T_FlowSession', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id, flow_session_id: props.flow_session_id, page: props.page+1}})}
  else{             router.push({name: 'S_FlowSession', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id, flow_session_id: props.flow_session_id, page: props.page+1}})}
}
const go_flow_completion_page = () => {
  if(props.create){ router.push({name: 'T_FlowCompletion', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id, flow_session_id: props.flow_session_id}})}
  else{             router.push({name: 'S_FlowCompletion', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id, flow_session_id: props.flow_session_id}})}
}
const finish_flow_session = () => {
  const params = {flow_session_id: props.flow_session_id}
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  axios.post(`http://localhost:8000/finish_flow_session`, params, config).then(function(response){
    // console.log(response.data)
    go_flow_completion_page()
  })
}
const change = () =>{
  reloadMathJax()
  dialog.value = !dialog.value
  console.log(dialog.value)
}

// created
update_data(props.page)

onBeforeRouteUpdate  ((to, from, next) => {
  update_data(to.params.page)
  reloadMathJax()
  next()
})
</script>

<template>
  <div>
    <v-responsive :min-height='600'>
      <v-container fluid>
        <v-col class='d-flex align-end flex-column'>
          <v-btn color = "yellow" icon='mdi-lightbulb' @click='change()'/>
          <pHint v-model:dialog='dialog' title='ヒント!!' :flow_session_id='flow_session_id' :page='page'/>
        </v-col>
        <component :is='component' :course_id='course_id' :week_id='week_id' :flow_id='flow_id' :flow_session_id='flow_session_id' :page='page' :page_content='page_content' :blank_answers='blank_answers' :answer_comment='answer_comment'/>
      </v-container>
    </v-responsive>
    <v-row>
      <v-col>
        <v-btn v-if='page > 1' @click='go_previous_page()'>前のページ</v-btn>
      </v-col>
      <v-col class='d-flex align-end flex-column'>
        <v-btn v-if='page < num_of_pages' @click='go_next_page()'>次のページ</v-btn>
        <v-btn v-if='page == num_of_pages' @click='finish_flow_session()'>終了</v-btn>
      </v-col>
    </v-row>
  </div>
</template>