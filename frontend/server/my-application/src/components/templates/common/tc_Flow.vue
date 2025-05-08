<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'
import { markdownToHtml, reloadMathJax } from '@/components/methods/markdown.js'
import tc_FlowInformation from '@/components/templates/common/tc_FlowInformation.vue'
import pT_FlowSessionTable from '@/components/parts/tables/pT_FlowSessionTable.vue';

// variable
const props = defineProps({
  create: {type: Boolean, default: false},
  course_id: {type: Number, required: true},
  week_id: {type: Number, required: true},
  flow_id: {type: Number, required: true},
})
const flow = ref({})
const last_flowsession_id = ref()
const last_flowsession_grade = ref()
const user_ability = ref()

// function
const get_flow = () => {
  axios.get(`http://localhost:8000/get_flow/${props.flow_id}`, {withCredentials: true}).then(function(response){
    flow.value = response.data
    console.log(flow.value)
  })
}

// created
get_flow()

</script>

<template>
  <v-container class='pa-0'>
    <h2 class='mb-3'>{{ flow.title }}</h2>
    <tc_FlowInformation :create='create' :course_id='course_id' :week_id='week_id' :flow_id='flow_id'/>
    <v-divider class='my-5' :thickness='3'/>
    <pT_FlowSessionTable :create='create' :course_id='course_id' :week_id='week_id' :flow_id='flow_id' :restart_session='flow.restart_session'/>
  </v-container>
</template>