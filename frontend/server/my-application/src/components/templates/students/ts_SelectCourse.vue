<!-- 科目選択後のセレクト -->

<script setup>
import { useRouter } from 'vue-router'
import pSelectPageTab from '@/components/parts/btns/pB_TabItem.vue'

const router = useRouter()
const props = defineProps({
  location: String,
  course_id: Number,
})

const moveSSyllabusInfo = () => router.push({name: 'S_SyllabusInfo', params: {course_id: props.course_id}})
const moveSCourse = () => router.push({name: 'S_Course', params: {course_id: props.course_id}})
const moveSProfile = () => router.push({name: 'S_Profile', params: {course_id: props.course_id}})
const moveSCourseScore = () => router.push({name: 'S_CourseScore', params: {course_id: props.course_id}})
</script>

<template>
  <div>
    <v-row>
      <pSelectPageTab :location='location' page='S_Syllabus'      tab-name='シラバス情報'      :move='moveSSyllabusInfo'/>
      <pSelectPageTab :location='location' page='S_Course'        tab-name='コンテンツ一覧'    :move='moveSCourse'/>
      <pSelectPageTab :location='location' page='S_Profile'       tab-name='演習履歴'          :move='moveSProfile'/>
      <pSelectPageTab :location='location' page='S_ReviewMat'     tab-name='関連教材' />
      <pSelectPageTab :location='location' page='S_CourseScore'   tab-name='学習状況一覧'      :move='moveSCourseScore'/>
      <pSelectPageTab :location='location' page='S_Community'     tab-name='コミュニティ' />
    </v-row>
    <v-divider class='my-3' :thickness='3'/>
  </div>
</template>