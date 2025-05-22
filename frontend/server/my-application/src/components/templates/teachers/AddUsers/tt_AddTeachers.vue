<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'

// variable
const headers = ref([
  {title: 'メールアドレス', align: 'start', key: 'email'},
  {title: 'ユーザ名', align: 'start', key: 'username'},
  {title: '閲覧権限', align: 'start', key: 'read_answer'},
  {title: '編集権限', align: 'start', key: 'update_answer'},
  {title: '削除権限', align: 'start', key: 'delete_answer'}
])
const props = defineProps({
  course_id : {type: Number, required: true},
  unregistered_teachers: {type: Object},
  update_answer: {type: Boolean, default: false} 
})
const emit = defineEmits([
  'reload_teacher'
])

// function
const filter_add = (data) => {
  const result = data.filter(item => {
    return Object.values(item).includes(true)
  })
  return result
}
const add_grant_teacher = (user_list) => {
  const filter_user = filter_add(user_list)
  const params = {'course_id': props.course_id, 'user_list': filter_user}
  console.log(JSON.stringify(params))
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  axios.post('https://demo-fast-api-lms.vercel.app/register_grant_teacher', params, config).then(function(response){
    console.log(response.data)
    emit('reload_teacher')
  })
}
</script>

<template>
  <div>
    <h3 class='mb-3'>権限付与</h3>
    <v-row class='align-center justify-end mx-5'>
      <v-btn v-if='update_answer' depressed color="primary" @click='add_grant_teacher(unregistered_teachers)'>追加</v-btn>
    </v-row>
    <v-data-table :headers='headers' :items='unregistered_teachers'>
      <template v-slot:item.read_answer='{ item }'>
        <v-checkbox-btn v-model='item.read_answer' :disabled='!update_answer'/>
      </template>
      <template v-slot:item.update_answer='{ item }'>
        <v-checkbox-btn v-model='item.update_answer' :disabled='!update_answer'/>
      </template>
      <template v-slot:item.delete_answer='{ item }'>
        <v-checkbox-btn v-model='item.delete_answer' :disabled='!update_answer'/>
      </template>
    </v-data-table>
  </div>
</template>