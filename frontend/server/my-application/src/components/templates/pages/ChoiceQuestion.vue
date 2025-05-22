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
  course_id: Number,
  week_id: Number,
  flow_id: Number,
  flow_session_id: Number,
  page: Number,
  page_content: Object,
  blank_answers: Array,
  answer_comment: String,
})
const blank_answer = ref([])
const is_correct = ref("")
const is_answered = ref(false)

// function
const register_answer = () => {
  const params = [{
    "flow_session_id": props.flow_session_id,
    "page": props.page,
    "blank_id": props.page_content.blank_id,
    "answer": blank_answer.value.sort().toString(),
    "is_correct": is_correct.value
  }]
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  console.log(params)
  axios.post('https://demo-fast-api-lms.vercel.app/register_blank_answer', params, config).then(function(response){
    // console.log(response.data[0])
    is_correct.value=response.data[0]['is_correct']
    is_answered.value = true
    reloadMathJax()
  })
  reloadMathJax()
}
const set_blank = () => {
  if(props.blank_answers != "") {
    console.log(props.blank_answers)
    blank_answer.value = props.blank_answers[0]['answer'].split(',')
  }
}

// created

// onMounted
onMounted(() => {
  reloadMathJax()
  set_blank()
})
// onBeforeUpdate
onBeforeUpdate(() => {
  if(!is_answered.value)
    is_correct.value = ''
    is_answered.value = false
  reloadMathJax()
})
onUpdated(() => {
  if(is_answered.value)
    is_answered.value = false
  blank_answer.value = []
  set_blank()
})
</script>

<template>
  <v-container fluid class='pa-0'>
    <v-responsive :min-height='300'>
      <v-container fluid>
        <MathJaxComp>
          <div v-html='markdownToHtml(page_content.content)'/>
        </MathJaxComp>
      </v-container>
    </v-responsive>
    <v-container class='pa-0'>
      <div class='rounded-lg pa-8 pl-12 bg-grey-lighten-3 text-no-wrap'>
        <!-- <v-row>
          <v-radio-group v-model='blank_answer[page_content.blank_id]'>
            <v-row class='d-flex align-center' v-for='choice in page_content.choices' :key='choice.order'>
              <v-col cols='1'>
                <v-radio :value='choice.id'/>
              </v-col>
              <MathJaxComp>
                <div v-html='markdownToHtml(choice.content)'/>
              </MathJaxComp>
            </v-row>
          </v-radio-group>
        </v-row> -->
        <div v-for='choice in page_content.choices' :key='choice.order'>
          <v-row class='d-flex align-center'>
            <v-checkbox v-model='blank_answer' :value='choice.id' class='shrink mr-2'/>
            <MathJaxComp class='mt-n5'>
              <div v-html='markdownToHtml(choice.content)'/>
            </MathJaxComp>
          </v-row>
        </div>
        <pDefaultBtn position='end-end' text='解答する' @func='register_answer' />
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