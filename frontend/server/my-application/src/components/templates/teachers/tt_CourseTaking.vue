<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'
import tt_AddStudents from '@/components/templates/teachers/AddUsers/tt_AddStudents.vue'
import tt_ConfStudents from '@/components/templates/teachers/AddUsers/tt_ConfStudents.vue'
import tt_AddTeachers from '@/components/templates/teachers/AddUsers/tt_AddTeachers.vue'
import tt_ConfTeachers from '@/components/templates/teachers/AddUsers/tt_ConfTeachers.vue'

// variable
const tab = ref('one')
const update_answer = ref()
const registered_students = ref()
const unregistered_students =ref()
const registered_teachers = ref()
const unregistered_teachers =ref()
const props = defineProps({
  course_id : {type: Number, required: true}
})

// function
const get_course = () => {
  axios.get(`http://localhost:8000/get_course_info/${props.course_id}`, {withCredentials: true}).then(function(response){
    update_answer.value = response.data.update_answer
  })
}
const get_taking_students = () => {
  axios.get(`http://localhost:8000/get_taking_students/${props.course_id}`, {withCredentials: true}).then(function(response){
    console.log(response.data)
    registered_students.value = response.data.registered
    unregistered_students.value = response.data.unregistered
  })
}
const get_grant_teachers = () => {
  axios.get(`http://localhost:8000/get_grant_teachers/${props.course_id}`, {withCredentials: true}).then(function(response){
    console.log(response.data)
    registered_teachers.value = response.data.registered
    unregistered_teachers.value = response.data.unregistered
  })
}

// created
get_course()
get_taking_students()
get_grant_teachers()
</script>

<template>
  <div>
    <h2 class='mb-3'>履修者登録・権限設定</h2>
    <v-tabs v-model='tab' fixed-tabs bg-color='grey-lighten-3' slider-color='secondary'>
      <h3 class='d-flex align-center mx-10'>学生</h3>
      <v-tab value='add_students' class='bg-primary'>履修者登録</v-tab>
      <v-tab value='conf_students' class='bg-primary'>履修者確認</v-tab>
      <h3 class='d-flex align-center mx-10'>教員</h3>
      <v-tab value='add_teachers' class='bg-primary'>権限付与</v-tab>
      <v-tab value='conf_teachers' class='bg-primary'>権限確認</v-tab>
    </v-tabs>
    <v-container>
      <v-tabs-window v-model='tab'>
        <v-tabs-window-item value='add_students'>
          <tt_AddStudents :course_id='course_id' :unregistered_students='unregistered_students' :update_answer='update_answer' @reload_student='get_taking_students'/>
        </v-tabs-window-item>
        <v-tabs-window-item value='conf_students'>
          <tt_ConfStudents :course_id='course_id' :registered_students='registered_students' :update_answer='update_answer' @reload_student='get_taking_students'/>
        </v-tabs-window-item>
        <v-tabs-window-item value='add_teachers'>
          <tt_AddTeachers :course_id='course_id' :unregistered_teachers='unregistered_teachers' :update_answer='update_answer' @reload_teacher='get_grant_teachers'/>
        </v-tabs-window-item>
        <v-tabs-window-item value='conf_teachers'>
          <tt_ConfTeachers :course_id='course_id' :registered_teachers='registered_teachers' :update_answer='update_answer' @reload_teacher='get_grant_teachers'/>
        </v-tabs-window-item>
      </v-tabs-window>
    </v-container>
  </div>
</template>