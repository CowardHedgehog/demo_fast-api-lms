<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'

// variable
const headers = ref([
  {title: 'メールアドレス', align: 'start', key: 'email'},
  {title: 'ユーザ名', align: 'start', key: 'username'},
  {title: '種別', align: 'start', key: 'kind_name'}
])
const select = ref()
const props = defineProps({
  course_id : {type: Number, required: true},
  registered_students: {type: Object},
  update_answer: {type: Boolean, default: false} 
})
const emit = defineEmits([
  'reload_student'
])

// function
const delete_taking_students = (user_list) => {
  const params = {'course_id': props.course_id, 'user_list': user_list}
  console.log(JSON.stringify(params))
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  axios.post('http://localhost:8000/delete_taking_student', params, config).then(function(response){
    console.log(response.data)
    emit('reload_student')
  })
}
</script>

<template>
  <div>
    <h3 class='mb-3'>履修者確認</h3>
    <v-row class='align-center justify-end mx-5'>
      <v-btn v-if='update_answer' depressed color="primary" @click='delete_taking_students(select)'>削除</v-btn>
    </v-row>
    <v-data-table :headers='headers' :items='registered_students' v-model='select' :show-select='update_answer' />
  </div>
</template>