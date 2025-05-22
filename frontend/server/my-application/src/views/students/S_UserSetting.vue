<script setup>
// import
import axios from "axios";
import { ref } from "vue";
import tc_access_time from "@/components/templates/common/tc_access_time.vue";
import ts_Header from "@/components/templates/students/ts_Header.vue";
import ts_SelectHome from "@/components/templates/students/ts_SelectHome.vue";
import tc_UserInfo from "@/components/templates/common/tc_UserInfo.vue";
import ts_UserSetting from "@/components/templates/students/ts_UserSetting.vue";
import tc_SessionError from "@/components/templates/common/tc_SessionError.vue";

// variable
const user_info = ref({});
const nickname = ref();
const session_error = ref(false);

// function
const get_nickname = () => {
  const config = {
    headers: { "Content-Type": "application/json" },
    withCredentials: true,
  };
  axios
    .get("https://demo-fast-api-lms.vercel.app/get_nickname", config, {
      withCredentials: true,
    })
    .then((response) => (nickname.value = response.data));
};
const home_profile = () => {
  axios
    .get("https://demo-fast-api-lms.vercel.app/home_profile", { withCredentials: true })
    .then(function (response) {
      console.log(response.data);
      user_info.value = response.data;
    })
    .catch(function (error) {
      if (error.response?.status == 401) {
        session_error.value = true;
      } else {
        console.log(error.response);
      }
    });
};

// created
get_nickname();
home_profile();
</script>

<template>
  <div>
    <tc_access_time page="S_UserSetting" />
    <ts_Header :user_info="user_info" />
    <v-main>
      <v-container>
        <v-responsive :max-width="1200" class="mx-auto">
          <v-container>
            <ts_SelectHome location="S_UserSetting" />
            <v-row>
              <v-container class="pt-5">
                <!-- Component -->
                <ts_UserSetting :user_info="user_info" :nickname="nickname" />
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
