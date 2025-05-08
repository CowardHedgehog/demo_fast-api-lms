<script setup>
// import
import axios from 'axios'
import { ref, onMounted} from 'vue'
//import { markdownToHtml, reloadMathJax } from '@/components/methods/markdown.js'
import { onBeforeRouteUpdate, useRouter } from 'vue-router'
import tc_access_time from '@/components/templates/common/tc_access_time.vue'
import tt_Header from '@/components/templates/teachers/tt_Header.vue'
import tt_SelectCourse from '@/components/templates/teachers/tt_SelectCourse.vue'
import tc_Week from '@/components/templates/common/tc_Week.vue'
import tc_SessionError from '@/components/templates/common/tc_SessionError.vue'

// variable
const user_info = ref({})
const session_error = ref(false)

const props = defineProps({
  course_id: Number,
  week_id: Number,
  page: Number,
})

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

//onMounted(() => reloadMathJax())
</script>

<template>
  <div>
    <tc_access_time page='T_Week' :details="'course_id:' + course_id + ',week_id:' + week_id"/>
    <tt_Header :user_info='user_info'/>    
    <v-main>
      <v-container>
        <v-responsive :max-width='1200' class='mx-auto'>
          <v-container>
            <tt_SelectCourse location='T_Week' :course_id='course_id'/>
            <v-row>
              <v-container class='pt-5'>
                <!-- Component -->
                <tc_Week :create='user_info.create' :course_id='course_id' :week_id='week_id' :page='page'/>
                <!-- End -->
              </v-container>
            </v-row>
          </v-container>
        </v-responsive>
      </v-container>
      <tc_SessionError v-if='session_error'/>
    </v-main>
  </div>
</template>