<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'

// variable
const props = defineProps({
  course_id : {type: Number, required: true}
})
const syllabus_info = ref()
const keyword = ref()

// function
const get_syllabus_info = () => {
  axios.get(`http://localhost:8000/get_syllabus_info/${props.course_id}`, {withCredentials: true}).then(function(response){
    console.log(response.data)
    syllabus_info.value = response.data
    keyword.value = response.data.subject_keyword.split(',')
})}

// created
get_syllabus_info()
</script>

<template>
  <div v-if='syllabus_info'>
    <v-table>
      <thead>
        <tr class='bg-primary'>
          <th class='text-center'>授業科目区分</th>
          <th class='text-center'>科目名</th>
          <th class='text-center'>単位数</th>
          <th class='text-center'>科目コード</th>
          <th class='text-center'>開講時期</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th class='text-center'>{{ syllabus_info.subject_class }}</th>
          <th class='text-center'>{{ syllabus_info.subject_name }}</th>
          <th class='text-center'>{{ syllabus_info.subject_credit }}</th>
          <th class='text-center'>{{ syllabus_info.subject_code }}</th>
          <th class='text-center'>{{ syllabus_info.subject_period }}</th>
        </tr>
      </tbody>
    </v-table>
    <div class='mb-5'/>
    <v-table>
      <thead  class='bg-primary'>
        <tr>
          <th colspan='2' class='text-center'>授業科目の学習・教育目標</th>
        </tr>
        <tr>
          <th class='text-center'>キーワード</th>
          <th class='text-center'>学習・教育目標</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th width='250'>
            <div v-for='(item, i) in keyword' :key='i' class='text-left my-2'>
              {{ i+1 }}. {{ item }}
            </div>
          </th>
          <th class='text'>{{ syllabus_info.subject_goals }}</th>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style lang="scss" scoped>
table{
  width: 80%;
  text-size-adjust: 120%;
  thead{
    color: white;
  }
  th,td{
    border: thin solid rgba(0, 0, 0, 0.12);
    text-align: center;
  }
}
</style>