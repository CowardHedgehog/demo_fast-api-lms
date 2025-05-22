<script setup>
// import
import axios from "axios";
import { ref, onMounted } from "vue";
import {
  markdownToHtml,
  reloadMathJax,
} from "@/components/methods/markdown.js";
import tc_access_time from "@/components/templates/common/tc_access_time.vue";
import ts_Header from "@/components/templates/students/ts_Header.vue";
import ts_SelectCourse from "@/components/templates/students/ts_SelectCourse.vue";
import tc_FlowInformation from "@/components/templates/common/tc_FlowInformation.vue";
import tc_SessionError from "@/components/templates/common/tc_SessionError.vue";

// variable
const props = defineProps({
  course_id: { type: Number, required: true },
  week_id: { type: Number, required: true },
});
const week = ref({});
const flows = ref({});
const user_info = ref({});
const session_error = ref(false);

// function
const home_profile = () => {
  axios
    .get("https://demo-fast-api-lms.vercel.app/home_profile", { withCredentials: true })
    .then(function (response) {
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
const get_week = () => {
  axios
    .get(`https://demo-fast-api-lms.vercel.app/get_week/${props.week_id}`, {
      withCredentials: true,
    })
    .then(function (response) {
      console.log(response.data);
      week.value = response.data;
    });
};
const get_week_flows = () => {
  axios
    .get(`https://demo-fast-api-lms.vercel.app/get_week_flows/${props.week_id}`, {
      withCredentials: true,
    })
    .then(function (response) {
      console.log(response.data);
      flows.value = response.data;
    });
};

// created
home_profile();
get_week();
get_week_flows();
</script>

<template>
  <div>
    <tc_access_time
      page="S_WeekFlows"
      :details="'course_id:' + course_id + ',week_id:' + week_id"
    />
    <ts_Header :user_info="user_info" />
    <v-main>
      <v-container>
        <v-responsive :max-width="1200" class="mx-auto">
          <v-container>
            <ts_SelectCourse location="S_WeekFlows" :course_id="course_id" />
            <v-row>
              <v-container>
                <h2>
                  第{{ week.week_num }}回　{{ week.week_name }}の演習問題一覧
                </h2>
                <v-container
                  class="pa-0 pt-5"
                  v-for="flow in flows"
                  :key="flow.id"
                >
                  <h3 class="mb-3">{{ flow.title }}</h3>
                  <tc_FlowInformation
                    :create="user_info.create"
                    :course_id="course_id"
                    :week_id="week_id"
                    :flow_id="flow.id"
                    :previous="false"
                  />
                  <v-divider class="my-5" :thickness="3" />
                </v-container>
              </v-container>
            </v-row>
          </v-container>
        </v-responsive>
      </v-container>
      <tc_SessionError v-if="session_error" />
    </v-main>
  </div>
</template>
