<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import pC_SubjectSelect from '@/components/parts/cards/pC_SubjectSelect.vue'

// variable
const router = useRouter()
const during_subjects = ref([])
const outside_subjects = ref([])

// function
const get_subjects = () => {
  axios.get('http://localhost:8000/get_subjects', {withCredentials: true}).then(function(response){
    console.log(response.data)
    during_subjects.value = response.data.during_result
    outside_subjects.value = response.data.outside_result
    console.log(during_subjects.value, outside_subjects.value)
})}

const move_subject = (subject_id) => router.push({name: 'T_Subject', params: {subject_id: subject_id}})

// created
get_subjects()


</script>


<template>
  <div>
    <h2>科目一覧</h2>
    <h3 class='mt-3'>対象期間中の科目</h3>
    <v-row>
      <v-col cols='4' v-for='subject in during_subjects' :key='subject.id' class='pb-4'>
        <pC_SubjectSelect @click='move_subject(subject.id)' :subject='subject' />
      </v-col>
    </v-row>
    <h3 class='mt-5'>対象期間外の科目</h3>
    <v-row>
      <v-col cols='4' v-for='subject in outside_subjects' :key='subject.id' class='pb-4'>
        <pC_SubjectSelect @click='move_subject(subject.id)' :subject='subject' />
      </v-col>
    </v-row>
  </div>
</template>
