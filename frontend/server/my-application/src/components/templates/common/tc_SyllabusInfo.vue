<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'
import pT_SyllabusInfoTable from '@/components/parts/tables/pT_SyllabusInfoTable.vue'

// variable
const props = defineProps({
  course_id : {type: Number, required: true}
})

// function

// created
</script>

<template>
  <div>
    <h2 class='mb-3'>シラバス情報</h2>
    <pT_SyllabusInfoTable :course_id='course_id' />
  </div>
</template>