<script setup>
// import
import axios from "axios";
import { ref } from "vue";
import tc_access_time from "@/components/templates/common/tc_access_time.vue";
import ts_Header from "@/components/templates/students/ts_Header.vue";
import ts_SelectHome from "@/components/templates/students/ts_SelectHome.vue";
import tc_UserInfo from "@/components/templates/common/tc_UserInfo.vue";
import ts_Home from "@/components/templates/students/ts_Home.vue";
import tc_SessionError from "@/components/templates/common/tc_SessionError.vue";

// variable
const user_info = ref({});
const session_error = ref(false);

// function
const home_profile = () => {
  axios
    .get("http://localhost:8000/home_profile", { withCredentials: true })
    .then(function (response) {
      //console.log(response.data)
      user_info.value = response.data;
    })
    .catch(function (error) {
      //console.log(error)
      if (error.response?.status == 401) {
        session_error.value = true;
      } else {
        console.log(error.response);
      }
    });
};

// created
home_profile();
</script>

<template>
  <div>
    <tc_access_time page="S_Home" />
    <ts_Header :user_info="user_info" />
    <v-main>
      <v-container>
        <v-responsive :max-width="1200" class="mx-auto">
          <v-container>
            <ts_SelectHome location="S_Home" />
            <v-row>
              <v-container class="pt-5">
                <!-- Component -->
                <ts_Home :create="user_info.create" />
                <!-- End -->
              </v-container>
            </v-row>
          </v-container>
        </v-responsive>
      </v-container>
      <tc_SessionError v-if="session_error" />
    </v-main>
  </div>
</template>
