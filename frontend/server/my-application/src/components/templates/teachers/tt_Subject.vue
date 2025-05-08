<script setup>
// import
import axios from 'axios'
import { useTheme } from 'vuetify'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import pB_Btn from '@/components/parts/btns/pB_Btn.vue'
import pC_CourseSelect from '@/components/parts/cards/pC_CourseSelect.vue'

// variable
const router = useRouter()
const props = defineProps({
  subject_id: {type: Number, required: true},
  create: {type: Boolean, default: false} 
})
const created_courses = ref([])
const shared_courses = ref([])

// function
const get_courses = () => {
  axios.get(`http://localhost:8000/get_created_courses/${props.subject_id}`, {withCredentials: true}).then(function(response){
    console.log(response.data)
    created_courses.value = response.data.created
    shared_courses.value = response.data.shared
  })
}
const move_course = (course_id) => router.push({name: 'T_Course', params: {course_id: course_id}})
const move_score = (course_id) => router.push({name: 'T_CourseScore', params: {course_id: course_id}})
const move_syllabus_info = (course_id) => router.push({name: 'T_SyllabusInfo', params: {course_id: course_id}})
const move_register_course = () => router.push({name: 'T_RegisterCourse', params: {subject_id: props.subject_id}})

// created
get_courses()
</script>


<template>
  <div>
    <h2 v-if='created_courses.length!=0'>コース一覧</h2>
    <pB_Btn text='コースの追加' position='right-center' @func='move_register_course()'/>
    <h3 class='mt-3'>作成したコース</h3>
    <v-row>
      <v-col cols='4' v-for='course in created_courses' :key='course.course_id' class='pb-3'>
        <pC_CourseSelect :create='create' :course='course' @move_course='move_course' @move_score='move_score' @move_syllabus_info='move_syllabus_info'/>
      </v-col>
      <h3 v-if='created_courses.length==0' class='ma-10'>作成したコースがありません</h3>
    </v-row>
    <v-divider class='my-2' :thickness="5" />
    <h3 class='mt-5'>共有中のコース</h3>
    <v-row>
      <v-col cols='4' v-for='course in shared_courses' :key='course.course_id' class='pb-3'>
        <pC_CourseSelect :create='create' :course='course' @move_course='move_course' @move_score='move_score' @move_syllabus_info='move_syllabus_info'/>
      </v-col>
    </v-row>
    <h3 v-if='shared_courses.length==0' class='ma-10'>共有中のコースがありません</h3>
  </div>
</template>
