<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'
import tc_access_time from '@/components/templates/common/tc_access_time.vue'
import tt_Header from '@/components/templates/teachers/tt_Header.vue'
import ts_SelectHome from '@/components/templates/teachers/tt_SelectHome.vue'
import tt_Subject from '@/components/templates/teachers/tt_Subject.vue'
import tc_SessionError from '@/components/templates/common/tc_SessionError.vue'

// variable
const user_info = ref({})
const session_error = ref(false)
const props = defineProps({
  subject_id: {type: Number, required: true}
})

// function
const home_profile = () => {
  axios.get('https://demo-fast-api-lms.vercel.app/home_profile', {withCredentials: true}).then(function(response){
    //console.log(response.data)
    user_info.value = response.data
  }).catch(
    function(error){
      //console.log(error)
      if(error.response?.status == 401) {session_error.value = true}
      else{console.log(error.response)}
    }
  )
}

// created
home_profile()
</script>

<template>
  <div>
    <tc_access_time page='T_Subject' :details="'subject_id:'+subject_id"/>
    <tt_Header :user_info='user_info'/>    
    <v-main>
      <v-container>
        <v-responsive :max-width='1200' class='mx-auto'>
          <v-container>
            <ts_SelectHome location='T_Home'/>
            <v-row>
              <v-container class='pt-5'>
                <!-- Component -->
                <tt_Subject :subject_id='subject_id' :create='user_info.create'/>
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