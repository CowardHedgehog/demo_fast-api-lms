<script setup>
// import
import { ref } from 'vue'

// variable
const props = defineProps({
  create: {type: Boolean, default: false},
  course: {type: Object, required: true}, 
})
const emit = defineEmits(['move_course', 'move_score', 'move_syllabus_info'])

// function
const move_course = (course_id) => emit('move_course', course_id)
const move_score = (course_id) => emit('move_score', course_id)
const move_syllabus_info = (course_id) => emit('move_syllabus_info', course_id)

// created
</script>

<template>
  <v-card min-height='200' class='bg-grey-lighten-3 mx-auto mt-5 ' >
    <template v-slot:title>
      {{ course.subject_name }}
    </template>
    <v-divider/>
    <v-card-text>
      コース名：{{ course.course_name }} <br>
      開講時期：{{ course.period }}<br>
      <div v-if='create'>作成者：{{ course.username }}</div>
    </v-card-text>
    <div v-if='create'>
      <v-card-actions>
        <v-row class='d-flex flex-row justify-space-between mx-1 mb-1'>
          <v-col cols='6'>
            <v-btn block depressed class='mt-2 bg-primary' text='コース情報' @click='move_course(course.course_id)'/>
          </v-col>
          <v-col cols='6'>
            <v-btn block depressed class='mt-2 bg-primary' text='学習状況照会' @click='move_score(course.course_id)'/>
          </v-col>
        </v-row>
      </v-card-actions>
    </div>
    <div v-else>
      <v-card-actions>
        <v-row class='d-flex flex-row justify-space-between mx-1 mb-1'>
          <v-col cols='4'>
            <v-btn block depressed class='mt-2 bg-primary' text='学習を始める' @click='move_course(course.course_id)'/>
          </v-col>
          <v-col cols='4'>
            <v-btn block depressed class='mt-2 bg-primary' text='学習状況照会' @click='move_score(course.course_id)'/>
          </v-col>
          <v-col cols='4'>
            <v-btn block depressed class='mt-2 bg-primary' text='シラバス情報' @click='move_syllabus_info(course.course_id)'/>
          </v-col>
        </v-row>
      </v-card-actions>
    </div>
    
  </v-card>
</template>