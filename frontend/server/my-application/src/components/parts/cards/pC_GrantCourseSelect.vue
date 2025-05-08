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

// created
</script>

<template>
  <v-card min-height='200' class='bg-grey-lighten-3 mx-auto mt-5 ' >
    <template v-slot:title>
      {{ course.course_name }}
    </template>
    <v-divider/>
    <v-card-text>
      {{ course.subject_name }} <br>
      {{ course.period }} <br>
      権限：
      <span v-if='course.read_answer'>読取権限　</span>
      <span v-if='course.update_answer'>編集権限　</span>
      <span v-if='course.delete_answer'>削除権限</span>
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
  </v-card>
</template>