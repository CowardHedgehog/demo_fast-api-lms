<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'
import tc_access_time from '@/components/templates/common/tc_access_time.vue'
import tt_Header from '@/components/templates/teachers/tt_Header.vue'
import tt_SelectHome from '@/components/templates/teachers/tt_SelectHome.vue'
import tc_UserInfo from '@/components/templates/common/tc_UserInfo.vue'
import tc_UpdatePassword from '@/components/templates/common/tc_UpdatePassword.vue'
import tc_SessionError from '@/components/templates/common/tc_SessionError.vue'

// variable
const user_info = ref({})
const session_error = ref(false)

// function
const home_profile = () => {
  axios.get('https://demo-fast-api-lms.vercel.app/home_profile', {withCredentials: true}).then(function(response){
    console.log(response.data)
    user_info.value = response.data
  }).catch(
    function(error){
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
    <tc_access_time page='T_UpdatePassword'/>
    <tt_Header :user_info='user_info'/>    
    <v-main>
      <v-container>
        <v-responsive :max-width='1200' class='mx-auto'>
          <v-container>
            <tt_SelectHome location='S_UpdatePassword'/>
            <v-row>
              <v-container class='pt-5'>
                <!-- Component -->
                 <tc_UpdatePassword :user_info='user_info'/>
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