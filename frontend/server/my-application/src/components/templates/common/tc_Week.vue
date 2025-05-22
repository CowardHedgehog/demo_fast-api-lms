<script setup>
// import
import axios from 'axios'
import { ref, onMounted, onBeforeUnmount } from 'vue'
import dayjs from 'dayjs'
import ja from 'dayjs/locale/ja'
import MathJaxComp from '@/components/methods/MathJax.vue'
import { markdownToHtml, reloadMathJax } from '@/components/methods/markdown.js'
import { onBeforeRouteUpdate, useRouter } from 'vue-router'

dayjs.locale('ja')
// variable
const router = useRouter()
const props = defineProps({
  create:     {type: Boolean, default: false},
  course_id:  {type: Number, required: true},
  week_id:    {type: Number, required: true},
  page:       {type: Number, required: true},
})
const anchor = ref('#pagetop')
const move_top = ref(false)
const week = ref({})
const content = ref()
const s_time = ref()
const e_time = ref()
const time = ref()

// function
const get_week_content = (page) => {
  axios.get(`https://demo-fast-api-lms.vercel.app/get_week_content/${props.week_id}/${page}`, {withCredentials: true}).then(function(response){
    console.log(response.data)
    week.value = response.data
    content.value = markdownToHtml(week.value.content)
    reloadMathJax()
  })
}
const go_next_page = () => {
  if(props.create){ router.push({name: 'T_Week', params: {course_id: props.course_id, week_id: props.week_id, page: props.page + 1}})}
  else{             router.push({name: 'S_Week', params: {course_id: props.course_id, week_id: props.week_id, page: props.page + 1}})}
}
const go_previous_page = () => {
  if(props.create){ router.push({name: 'T_Week', params: {course_id: props.course_id, week_id: props.week_id, page: props.page - 1}})}
  else{             router.push({name: 'S_Week', params: {course_id: props.course_id, week_id: props.week_id, page: props.page - 1}})}
}
const go_flow_page = () => {
  if(props.create){ router.push({name: 'T_Course', params: {course_id: props.course_id}})}
  else{             router.push({name: 'S_Course', params: {course_id: props.course_id}})}
}

// created
get_week_content(props.page)

onMounted(() => {
  reloadMathJax()
  router.afterEach(() => {window.scrollTo({top:0, left:0, behavior: 'instant'})})
  s_time.value = dayjs()
  console.log(s_time.value)
  
})

onBeforeRouteUpdate  ((to, from, next) => {
  get_week_content(to.params.page)
  reloadMathJax()
  next()
})

onBeforeUnmount (() => {
  e_time.value = dayjs()
  console.log(e_time.value)
  time.value = e_time.value.diff(s_time.value, 'second')
  console.log(time.value)
})

</script>

<template>
  <div>
    <!-- Component -->
    <h2 id='page_top'>第{{ week.week_num }}回 _ {{ week.week_name }}</h2>
    <v-container class='mt-3' style="line-height: 2;">
      <MathJaxComp>
        <div v-html='content'/>
      </MathJaxComp>
    </v-container>
    <v-row>
      <v-col>
        <v-btn v-if='page > 1' @click='go_previous_page()'>前のページ</v-btn>
      </v-col>
      <v-col class='d-flex align-end flex-column'>
        <v-btn v-if='page < week.page_num' @click='go_next_page()'>次のページ</v-btn>
        <v-btn v-if='page == week.page_num' @click='go_flow_page()'>コンテンツ一覧に戻る</v-btn>
      </v-col>
    </v-row>
    <!-- End -->
  </div>
</template>

<style>
.box {
  background: #c4d9ff;
  border-left: #4e7bcc 5px solid;
  padding: 10px;
}
.box p {
  margin: 0;
  padding: 0;
}
.indent_1 {
  padding-left: 20px;
}
.indent_2 {
  padding-left: 40px;
}
.solid_border_1 {
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #333333;
}
.dashed_border_1 {
  padding: 10px;
  margin-bottom: 10px;
  border: 1px dashed #333333;
}
.example {
  padding: 10px;
  margin-bottom: 10px;
  border: 2px dashed #333333;
}
.answer {
  text-align: center;
  width:40px;
  margin: 1em;
  border: solid 2px #000000;
}
.definition {
  padding: 10px;
  margin-bottom: 10px;
  border: 2px solid #333333;
}
</style>