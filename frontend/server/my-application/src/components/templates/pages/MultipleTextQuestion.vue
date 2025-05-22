<script setup>
// import
import axios from 'axios'
import { ref, onMounted, onBeforeUpdate, onUpdated } from 'vue'
import MathJaxComp from '@/components/methods/MathJax.vue'
import { markdownToHtml, reloadMathJax } from '@/components/methods/markdown.js'
import pAnswer from '@/components/parts/text-fields/pTF_Answer.vue'
import pDefaultBtn from '@/components/parts/btns/pB_Btn.vue'

// variable
const props = defineProps({
  flow_session_id: Number,
  page: Number,
  page_content: Object,
  blank_answers: Array,
  answer_comment: String
})
const blank_answer = ref({})
const is_correct = ref("")
const is_answered = ref(false)

// function
const register_answer = () => {
  const params = []
  //console.log(params.value)
  for (const blank_id in blank_answer.value){
    params.push({
      "flow_session_id": props.flow_session_id,
      "page": props.page,
      "blank_id": Number(blank_id),
      "answer": blank_answer.value[blank_id]
    })
  }
  console.log(params)
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  axios.post(`https://demo-fast-api-lms.vercel.app/register_blank_answer`, params, config).then(function(response){
    var blanklength = props.page_content.answer_column_content.length
    let cnt = 0
    for(let i = 0; i < response.data.length; i++){if(response.data[i]["is_correct"] == true) cnt++}
    is_correct.value = ""
    is_answered.value = true
    // 全問正解ならば'正解'と表示
    is_correct.value = (cnt==blanklength)
    reloadMathJax()
  })
  reloadMathJax()
}
const set_blank = () => {
  props.blank_answers.forEach(ba => {
    blank_answer.value[ba.blank_id] = ba.answer ? ba.answer : ''
    // console.log(ba.answer)
})}

// created
set_blank()

onBeforeUpdate(() => {
  if(!is_answered.value)
    is_correct.value = ""
  is_answered.value = false
  reloadMathJax()
})

onUpdated(() => {
  if(is_answered.value) 
    is_answered.value = false
  blank_answer.value = []
  set_blank()
})

// onMounted
onMounted(() => reloadMathJax())
</script>

<template>
  <v-container fluid class='pa-0'>
    <v-responsive :min-height='300'>
      <v-container fluid>
        <MathJaxComp>
          <div v-html='markdownToHtml(page_content.content)' />
        </MathJaxComp>
      </v-container>
    </v-responsive>
    <v-container class='pa-0'>
      <div class='rounded-lg pa-8 bg-grey-lighten-3 text-no-wrap'>
        <div class='mx-2' v-for='answer_column in page_content.answer_column_content' :key='answer_column.data'>
          <MathJaxComp>
            <div v-html='markdownToHtml(answer_column.md)' class='mb-4'/>
          </MathJaxComp>
          <pAnswer v-model:answer='blank_answer[answer_column.blank_id]' @keydown.enter='register_answer'/>
        </div>
        <pDefaultBtn position='end-end' text='解答する' @func='register_answer'/>
      </div>
    </v-container>
    <v-container class='pa-0 mt-4' v-if='is_answered'>
      <div :class='`rounded-lg`' class='pa-6 my-6 bg-green-lighten-5' :max-width='300' v-if='is_correct'>
        <v-row><h2>正解です！！</h2></v-row>
        <MathJaxComp>
          <div v-html='markdownToHtml(answer_comment)' class='rounded-lg pa-6 my-6 bg-white' :overflow-wrap='`break-word`' style='width:100%' />
        </MathJaxComp>
      </div>
      <div :class='`rounded-lg`' class='pa-6 my-6 bg-red-lighten-5' :max-width='300' v-if='!is_correct'>
        <v-row><h2>不正解です</h2></v-row>
        <MathJaxComp>
          <div v-html='markdownToHtml(answer_comment)' class='rounded-lg pa-6 my-6 bg-white' :overflow-wrap='`break-word`' style='width:100%' />
        </MathJaxComp>
      </div>
    </v-container>
  </v-container>
</template>