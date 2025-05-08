<script setup>
// import
import axios from "axios";
import { ref, computed } from "vue";
import tc_access_time from "@/components/templates/common/tc_access_time.vue";
import ts_Header from "@/components/templates/students/ts_Header.vue";
import ts_SelectCourse from "@/components/templates/students/ts_SelectCourse.vue";
import tc_UserInfo from "@/components/templates/common/tc_UserInfo.vue";
import tc_SessionError from "@/components/templates/common/tc_SessionError.vue";
import ts_CourseScore from "@/components/templates/students/ts_CourseScore.vue";

const props = defineProps({
  course_id: {
    type: Number,
    required: true,
  },
});
// variable
const user_info = ref({});
const session_error = ref(false);

// function
const home_profile = () => {
  axios
    .get("http://localhost:8000/home_profile", { withCredentials: true })
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

// created
home_profile();
</script>

<template>
  <div>
    <tc_access_time page="S_CourseScore" :details="'course_id:' + course_id" />
    <ts_Header :user_info="user_info" />
    <v-main>
      <v-container>
        <v-responsive :max-width="1200" class="mx-auto">
          <v-container>
            <ts_SelectCourse location="S_CourseScore" />
            <v-row>
              <v-container class="pt-5">
                <ts_CourseScore :course_id="course_id" />
              </v-container>
            </v-row>
          </v-container>
        </v-responsive>
      </v-container>
      <tc_SessionError v-if="session_error" />
    </v-main>
  </div>
</template>
