<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { reloadMathJax } from '@/components/methods/markdown.js'

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
const go_flow_top_page = () => {
  if(props.create){ router.push({name:'T_Flow', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id}})}
  else{             router.push({name:'S_Flow', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id}})}
}

const go_any_page = (page) => {
  if(props.create){ router.push({name: 'T_FlowSession', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id, flow_session_id: props.flow_session_id, page: page}})}
  else{             router.push({name: 'S_FlowSession', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id, flow_session_id: props.flow_session_id, page: page}})}  
  reloadMathJax()
}
const go_flow_completion_page = () => {
  if(props.create){ router.push({name: 'T_FlowCompletion', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id, flow_session_id: props.flow_session_id}})}
  else{             router.push({name: 'S_FlowCompletion', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id, flow_session_id: props.flow_session_id}})}
}
const finish_flow_session = () => {
  const params = {flow_session_id: props.flow_session_id}
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  axios.post(`http://localhost:8000/finish_flow_session`, params, config).then(function(response){
    console.log(response.data)
    go_flow_completion_page()
  }).catch(function(error){
    console.log(error)
  })
}
</script>

<template>
  <v-container>
    <v-responsive :min-height='50'>
      <v-container class='pa-0'>
        <div :class='`rounded-lg`' class='bg-secondary'>
          <v-row no-gutters class='d-flex align-center'>
            <v-col cols='1'>
              <v-container fill-height>
                <v-row no-gutters>
                  <v-btn block class='pa-1' @click='go_flow_top_page()'>もどる</v-btn>
                </v-row>
              </v-container>
            </v-col>
            <v-col cols='10'>
              <v-container class='pa-2' fill-height>
                <v-row no-gutters>
                  <v-col cols='1' class='pa-1' v-for='page_i in num_of_pages' :key='page_i'>
                    <v-btn block class='pa-1' v-if='page_i == page' disabled color='black'>{{ page_i }}</v-btn>
                    <v-btn block class='pa-1' v-if='page_i != page' @click='go_any_page(page_i)'>{{ page_i }}</v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-col>
            <v-col cols='1'>
              <v-container fill-height>
                <v-row no-gutters>
                  <v-btn block class='pa-1' @click='finish_flow_session()'>終了</v-btn>
                </v-row>
              </v-container>
            </v-col>
          </v-row>
        </div>
      </v-container>
    </v-responsive>
  </v-container>
</template>