<script setup>
// import
import axios from "axios";
import { ref, computed } from "vue";
import { reloadMathJax } from "@/components/methods/markdown.js";
import tc_access_time from "@/components/templates/common/tc_access_time.vue";
import ts_Header from "@/components/templates/students/ts_Header.vue";
import ts_SelectCourse from "@/components/templates/students/ts_SelectCourse.vue";
import tc_FlowSessionLocationBar from "@/components/templates/common/tc_FlowSessionLocationBar.vue";
import tc_FlowSessionQuestion from "@/components/templates/common/tc_FlowSessionQuestion.vue";
import tc_SessionError from "@/components/templates/common/tc_SessionError.vue";

// variable
const user_info = ref({});
const session_error = ref(false);
const props = defineProps({
  course_id: { type: Number, required: true },
  week_id: { type: Number, required: true },
  flow_id: { type: Number, required: true },
  flow_session_id: { type: Number, required: true },
  page: { type: Number, required: true },
});
const flow_title = ref();
const num_of_pages = ref();

// function
const home_profile = () => {
  axios
    .get("https://demo-fast-api-lms.vercel.app/home_profile", { withCredentials: true })
    .then(function (response) {
      // console.log(response.data)
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
const get_flow_info = () => {
  axios
    .get(`https://demo-fast-api-lms.vercel.app/get_flow_info/${props.flow_session_id}`, {
      withCredentials: true,
    })
    .then(function (response) {
      // console.log(response.data)
      flow_title.value = response.data.flow_title;
      num_of_pages.value = response.data.num_of_pages;
    });
};

// created
home_profile();
get_flow_info();
</script>

<template>
  <div>
    <tc_access_time
      page="S_FlowSession"
      :details="
        'course_id:' +
        course_id +
        ',week_id:' +
        week_id +
        ',flow_id:' +
        flow_id +
        ',flow_session_id:' +
        flow_session_id
      "
    />
    <ts_Header :user_info="user_info" />
    <v-main>
      <v-container>
        <v-responsive :max-width="1200" class="mx-auto">
          <v-container>
            <ts_SelectCourse location="S_FlowSession" />
            <v-row>
              <v-container class="pt-5">
                <h2>{{ flow_title }}</h2>
                <tc_FlowSessionLocationBar
                  :create="user_info.create"
                  :course_id="course_id"
                  :week_id="week_id"
                  :flow_id="flow_id"
                  :flow_session_id="flow_session_id"
                  :page="page"
                  :num_of_pages="num_of_pages"
                />
                <tc_FlowSessionQuestion
                  :create="user_info.create"
                  :course_id="course_id"
                  :week_id="week_id"
                  :flow_id="flow_id"
                  :flow_session_id="flow_session_id"
                  :page="page"
                  :num_of_pages="num_of_pages"
                />
              </v-container>
            </v-row>
          </v-container>
        </v-responsive>
      </v-container>
      <tc_SessionError v-if="session_error" />
    </v-main>
  </div>
</template>
