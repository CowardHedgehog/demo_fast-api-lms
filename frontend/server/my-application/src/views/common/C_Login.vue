<script setup>
import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";
import tc_access_time from "@/components/templates/common/tc_access_time.vue";
import tc_Header from "@/components/templates/common/tc_Header.vue";
import pTF_Mail from "@/components/parts/text-fields/pTF_Mail.vue";
import pTF_Password from "@/components/parts/text-fields/pTF_Password.vue";
import pB_Btn from "@/components/parts/btns/pB_Btn.vue";
import pA_Info from "@/components/parts/alerts/pA_Info.vue";
import pA_Error from "@/components/parts/alerts/pA_Error.vue";

const alert = ref(true);
const login_error = ref(false);
const email = ref("");
const password = ref("");
const loading = ref(false);
const router = useRouter();
const count = ref(0);

const moveStudentHome = () => {
  router.push({ name: "S_Home" });
};
const moveTeacherHome = () => {
  router.push({ name: "T_Home" });
};
const moveLogin = () => {
  router.push({ name: "Login" });
};
const login = () => {
  //console.log(email, password)
  loading.value = true;
  const config = {
    headers: { "Content-Type": "application/json" },
    withCredentials: true,
  };
  const params = { email: email.value, password: password.value };
  axios
    .post("http://localhost:8000/token", params, config)
    .then(function (response) {
      console.log(response);
      axios
        .get("http://localhost:8000/home_profile", { withCredentials: true })
        .then(function (response) {
          //console.log(response)
          if (response.data.create) {
            moveTeacherHome();
          } else {
            moveStudentHome();
          }
        })
        .catch(function (error) {
          console.log(error);
          loading.value = false;
          if (error.response?.status == 401) {
            moveLogin();
          } else {
            console.log(error.response);
          }
        });
    })
    .catch(function (error) {
      axios
        .post("http://localhost:8000/token", params, config)
        .then(function (response) {
          console.log(response);
          axios
            .get("http://localhost:8000/home_profile", {
              withCredentials: true,
            })
            .then(function (response) {
              //console.log(response)
              if (response.data.create) {
                moveTeacherHome();
              } else {
                moveStudentHome();
              }
            })
            .catch(function (error) {
              console.log(error);
              loading.value = false;
              if (error.response?.status == 401) {
                moveLogin();
              } else {
                console.log(error.response);
              }
            });
        })
        .catch(function (error) {
          loading.value = false;
          login_error.value = true;
          console.log(error);
        });
    });
};
</script>

<template>
  <div>
    <tc_access_time page="C_Login" />
    <tc_Header />
    <v-main>
      <v-container>
        <v-responsive :max-width="800" class="mx-auto pt-5 px-5">
          <pTF_Mail v-model:email="email" />
          <pTF_Password v-model:password="password" @keydown.enter="login()" />
          <pB_Btn
            position="center"
            @func="login"
            text="ログイン"
            :loading="loading"
          />
          <v-row class="justify-center pt-5">
            <pA_Info
              v-if="alert"
              message="本サイトを使って学習を行われたデータは慎重に管理し、研究に使用させていただきます。"
            />
          </v-row>
          <v-row class="justify-center pt-5">
            <pA_Error
              v-if="login_error"
              message="メールアドレスもしくはパスワードが違います"
            />
          </v-row>
          <h3 class="text-center pt-5">
            <a
              href="mailto:adplms.kit@gmail.com?subject=【問い合わせ】&amp;body=学籍番号：%0d%0aお名前：%0d%0a内容：%0d%0a"
              >お問い合わせはこちら</a
            >
          </h3>
        </v-responsive>
      </v-container>
    </v-main>
  </div>
</template>
