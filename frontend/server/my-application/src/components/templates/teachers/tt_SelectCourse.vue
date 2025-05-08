<!-- 科目選択後のセレクト -->

<script setup>
import { useRouter } from 'vue-router'
import pSelectPageTab from '@/components/parts/btns/pB_TabItem.vue'

const router = useRouter()
const props = defineProps({
  location: String,
  course_id: Number,
})

const move_T_SyllabusInfo = () => router.push({name: 'T_SyllabusInfo', params: {course_id: props.course_id}})
const move_T_Course = () => router.push({name: 'T_Course', params: {course_id: props.course_id}})
const move_T_EditCourseInfo = () => router.push({name: 'T_EditCourseInfo', params: {course_id: props.course_id}})
const move_T_CourseTaking = () => router.push({name: 'T_CourseTaking', params: {course_id: props.course_id}})
const move_T_CourseScore = () => router.push({name: 'T_CourseScore', params: {course_id: props.course_id}})
</script>

<template>
  <div>
    <v-row>
      <pSelectPageTab :location='location' page='T_Syllabus'        tab-name='シラバス情報'         :move='move_T_SyllabusInfo'/>
      <pSelectPageTab :location='location' page='T_EditCourseInfo'  tab-name='コース情報編集'       :move='move_T_EditCourseInfo'/>
      <pSelectPageTab :location='location' page='T_Course'          tab-name='コンテンツ一覧'       :move='move_T_Course'/>
      <pSelectPageTab :location='location' page='T_CourseTaking'    tab-name='履修者登録・権限設定' :move='move_T_CourseTaking'/>
      <pSelectPageTab :location='location' page='T_CourseScore'           tab-name='学習状況一覧'         :move='move_T_CourseScore'/>
      <pSelectPageTab :location='location' page='S_Community'       tab-name='コミュニティ' />
    </v-row>
    <v-divider class='my-3' :thickness='3'/>
  </div>
</template>