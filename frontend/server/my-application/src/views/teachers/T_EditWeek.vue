<script setup>
// import
import axios from 'axios'
import { ref, watch } from 'vue'
import { markdownToHtml, reloadMathJax } from '@/components/methods/markdown.js'
import tc_access_time from '@/components/templates/common/tc_access_time.vue'
import tt_Header from '@/components/templates/teachers/tt_Header.vue'
import tt_SelectCourse from '@/components/templates/teachers/tt_SelectCourse.vue'
import tt_EditWeekInfos from '@/components/templates/teachers/EditWeeks/tt_EditWeekInfos.vue'
import tt_EditWeekContent from '@/components/templates/teachers/EditWeeks/tt_EditWeekContent.vue'
import tt_EditFlowContent from '@/components/templates/teachers/EditWeeks/tt_EditFlowContent.vue'
import tc_SessionError from '@/components/templates/common/tc_SessionError.vue'

// variable
const props = defineProps({
  course_id: Number,
  week_id: Number
})
const user_info = ref({})
const session_error = ref(false)
const tab = ref('')

// function
const home_profile = () => {
  axios.get('http://localhost:8000/home_profile', {withCredentials: true}).then(function(response){
    user_info.value = response.data
  }).catch(
    function(error){
      if(error.response?.status == 401) { session_error.value = true }
      else{console.log(error.response)}
    }
  )
}

// created
home_profile()
</script>

<template>
  <div>
    <tc_access_time page='T_EditWeek' :details="'course_id:'+course_id+',week_id:'+week_id"/>
    <tt_Header :user_info='user_info'/>    
    <v-main>
      <v-container>
        <v-responsive :max-width='1200' class='mx-auto'>
          <v-container>
            <tt_SelectCourse location='T_EditWeek'/>
            <v-row>
              <v-container class='pt-5'>
                <h2>詳細・コンテンツ編集</h2>
                <v-tabs v-model='tab' class='mt-3' slider-color='secondary' grow>
                  <v-tab value='week_info'    class='bg-primary'>詳細編集</v-tab>
                  <v-tab value='week_content' class='bg-primary' @click='reloadMathJax()'>教科書コンテンツ編集</v-tab>
                  <v-tab value='flow_content' class='bg-primary'>演習問題編集</v-tab>
                </v-tabs>
              </v-container>
            </v-row>
          </v-container>
        </v-responsive>
        <v-responsive :max-width='1800' class='mx-auto'>
          <v-tabs-window v-model='tab'>
            <v-tabs-window-item value='week_info'>
              <tt_EditWeekInfos :course_id='course_id' :week_id='week_id' />
            </v-tabs-window-item>
            <v-tabs-window-item value='week_content'>
              <tt_EditWeekContent :course_id='course_id' :week_id='week_id' />
            </v-tabs-window-item>
            <v-tabs-window-item value='flow_content'>
              <tt_EditFlowContent :course_id='course_id' :week_id='week_id' />
            </v-tabs-window-item>
          </v-tabs-window>
        </v-responsive>
      </v-container>
      <tc_SessionError v-if='session_error'/>
    </v-main>
  </div>
</template>