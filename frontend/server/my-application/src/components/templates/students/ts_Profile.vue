<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'
import { marked } from 'marked'
import { markdownToHtml, reloadMathJax } from '@/components/methods/markdown.js'
import { processDate } from '@/components/methods/display_format'

// variable
const props = defineProps({
  course_id : {type: Number, required: true}
})
const flow_session_history = ref()

// function
const get_flow_session_history = () => {
  axios.get(`https://demo-fast-api-lms.vercel.app/get_flow_session_history/${props.course_id}`, {withCredentials: true}).then(function(response){
    console.log(response.data)
    flow_session_history.value = response.data
    console.log(flow_session_history.value)
})}

// created
get_flow_session_history()
</script>

<template>
  <div>
    <h2 class='mb-3'>演習履歴</h2>
      <div v-for='(week, week_index) in flow_session_history' :key='week_index'>
        <v-expansion-panels>
          <v-expansion-panel v-for='(week_content, week_key) in week' :key='week_key'>
            <v-expansion-panel-title>
              <p class='text-body-2'>{{ week_key }}</p>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <div v-for='(flow, flow_index) in week_content' :key='flow_index'>
              <v-expansion-panels>
                <v-expansion-panel v-for='(flow_content, flow_key) in flow' :key='flow_key'>
                    <v-expansion-panel-title>
                      {{ flow_key }}
                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                      <div v-for='(flow_session, flow_session_index) in flow_content' :key='flow_session_index'>
                        <v-expansion-panels>
                          <v-expansion-panel :disabled='flow_session.flow_session_grade == 100' @click='reloadMathJax()'>
                            <v-expansion-panel-title>
                              {{ processDate(flow_session.finish_date_time) }}
                              <v-progress-linear :model-value='flow_session.flow_session_grade' color='secondary' height='35'>
                                <strong class='white'>{{ Math.ceil(flow_session.flow_session_grade.toFixed(0)) }}%</strong>
                              </v-progress-linear>
                            </v-expansion-panel-title>
                            <v-expansion-panel-text>
                              <h4>あなたが間違えた問題</h4>
                              <v-container v-for='(flowpage, flowpage_index) in flow_session.flow_page' :key='flowpage_index'>
                                <div v-html='markdownToHtml(flowpage.content)' />
                              </v-container>
                            </v-expansion-panel-text>
                          </v-expansion-panel>
                        </v-expansion-panels>
                      </div>
                    </v-expansion-panel-text>
                  </v-expansion-panel>
                </v-expansion-panels>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </div>
  </div>
</template>