<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import pC_WeekSelectCard from '@/components/parts/cards/pC_WeekSelectCard.vue'
import pT_WeekSelectTable from '@/components/parts/tables/pT_WeekSelectTable.vue'
import pB_Btn from '@/components/parts/btns/pB_Btn.vue'


// variable
const router = useRouter()
const props = defineProps({
  create: {type: Boolean, default: false},
  course_id : {type: Number, required: true}
})
const course_info = ref({})
const weeks = ref([])
const sw = ref(false)

// function
const get_course_info = () => {
  axios.get(`https://demo-fast-api-lms.vercel.app/get_course_info/${props.course_id}`, {withCredentials: true}).then(function(response){
    // console.log(response.data)
    course_info.value = response.data
  })
}
const get_weeks = () => {
  axios.get(`https://demo-fast-api-lms.vercel.app/get_weeks/${props.course_id}`, {withCredentials: true}).then(function(response){
    // console.log(response.data)
    weeks.value = response.data
  })
}
const move_preview = (week_id) => router.push({name: 'T_Week', params: {course_id: props.course_id, week_id: week_id, page: 1}})
const move_edit = (week_id) => router.push({name: 'T_EditWeek', params: {course_id: props.course_id, week_id: week_id}})
const move_score = (week_id) => router.push({name: 'T_WeekScore', params: {course_id: props.course_id, week_id: week_id}})
const move_T_RegisterWeek = () => router.push({name: 'T_RegisterWeek', params: {course_id: props.course_id}})

// created
get_course_info()
get_weeks()
</script>

<template>
  <div>
    <h2>{{ course_info.subject_name }}</h2>
    <h3>{{ course_info.course_name }} / {{ course_info.period }}</h3>
    <pB_Btn v-if='course_info.update_answer' text='コンテンツの追加' position='right-center' @func='move_T_RegisterWeek'/>
    <v-row class='d-flex align-center justify-end mr-3'>
      <v-icon icon='mdi-table-column' size='x-large' class='pb-6'/>
      <v-switch color='secondary' v-model='sw'/>
      <v-icon icon='mdi-table' size='x-large' class='pb-6'/>
    </v-row>
    <v-row class='mt-n10' v-show='sw'>
      <v-col cols='4' v-for='week in weeks' :key='week.week_id'>
        <pC_WeekSelectCard :create='create' :week='week' :update_answer='course_info.update_answer' @move_preview='move_preview' @move_edit='move_edit' @move_score='move_score'/>
      </v-col>
    </v-row>
    <v-row class='mt-n10' v-show='!sw'>
      <pT_WeekSelectTable :create='create' :weeks='weeks' :update_answer='course_info.update_answer' @move_preview='move_preview' @move_edit='move_edit' @move_score='move_score'/>
    </v-row>
  </div>
</template>