<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'

// variable
const headers = ref([
  {title: 'メールアドレス', align: 'start', key: 'email'},
  {title: 'ユーザ名', align: 'start', key: 'username'},
  {title: '読取権限', align: 'start', key: 'read_answer'},
  {title: '更新権限', align: 'start', key: 'update_answer'},
  {title: '削除権限', align: 'start', key: 'delete_answer'}
])
const props = defineProps({
  course_id : {type: Number, required: true},
  registered_teachers: {type: Object},
  update_answer: {type: Boolean, default: false} 
})
const emit = defineEmits([
  'reload_teacher'
])

// function
const add_grant_teacher = (user_list) => {
  const params = {'course_id': props.course_id, 'user_list': user_list}
  console.log(JSON.stringify(params))
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  axios.post('https://demo-fast-api-lms.vercel.app/update_grant_teacher', params, config).then(function(response){
    console.log(response.data)
    emit('reload_teacher')
  })
}
</script>

<template>
  <div>
    <h3 class='mb-3'>権限確認・追加</h3>
    <v-row class='align-center justify-end mx-5'>
      <v-btn v-if='update_answer' depressed color="primary" @click='add_grant_teacher(registered_teachers)'>更新</v-btn>
    </v-row>
    <v-data-table :headers='headers' :items='registered_teachers'>
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