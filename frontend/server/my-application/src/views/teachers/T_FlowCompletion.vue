<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'
import tc_access_time from '@/components/templates/common/tc_access_time.vue'
import tt_Header from '@/components/templates/teachers/tt_Header.vue'
import tt_SelectCourse from '@/components/templates/teachers/tt_SelectCourse.vue'
import tc_FlowCompletion from '@/components/templates/common/tc_FlowCompletion.vue'
import tc_SessionError from '@/components/templates/common/tc_SessionError.vue'

// variable
const props = defineProps({
  course_id : {type: Number, required: true},
  week_id: {type: Number, required: true},
  flow_id: {type: Number, required: true},
  flow_session_id: {type: Number, required: true}
})
const user_info = ref({})
const session_error = ref(false)

// function
const home_profile = () => {
  axios.get('https://demo-fast-api-lms.vercel.app/home_profile', {withCredentials: true}).then(function(response){
    // console.log(response.data)
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
    <tc_access_time page='T_FlowCompletion' :details="'course_id:'+course_id+',week_id:'+week_id+',flow_id:'+flow_id+',flow_session_id:'+flow_session_id"/>
    <tt_Header :user_info='user_info'/>    
    <v-main>
      <v-container>
        <v-responsive :max-width='1200' class='mx-auto'>
          <v-container>
            <tt_SelectCourse location='S_Week' :course_id='course_id'/>
            <v-row>
              <v-container class='pt-5'>
                <!-- Component -->
                <tc_FlowCompletion  :create='user_info.create' :course_id='course_id' :week_id='week_id' :flow_id='flow_id' :flow_session_id='flow_session_id'/>
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