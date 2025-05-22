<script setup>
// import
import axios from 'axios'
import { useTheme } from 'vuetify'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import pC_CourseSelect from '@/components/parts/cards/pC_CourseSelect.vue'

// variable
const router = useRouter()
const props = defineProps({
  create: {type: Boolean, default: false} 
})
const courses = ref([])

// function
const get_courses = () => {
  axios.get('https://demo-fast-api-lms.vercel.app/get_courses', {withCredentials: true}).then(function(response){
    console.log(response.data)
    courses.value = response.data
  })
}
const move_course = (course_id) => router.push({name: 'S_Course', params: {course_id: course_id}})
const move_score = (course_id) => router.push({name: 'S_CourseScore', params: {course_id: course_id}})
const move_syllabus_info = (course_id) => router.push({name: 'S_SyllabusInfo', params: {course_id: course_id}})

// created
get_courses()
</script>


<template>
  <div>
    <h2>科目選択</h2>
    <v-row>
      <v-col cols='6' v-for='course in courses' :key='course.course_id' class='pb-4'>
        <pC_CourseSelect :create='create' :course='course' @move_course='move_course' @move_score='move_score' @move_syllabus_info='move_syllabus_info'/>
      </v-col>
    </v-row>
  </div>
</template>
