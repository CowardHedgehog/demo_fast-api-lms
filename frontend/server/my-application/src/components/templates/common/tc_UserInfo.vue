<!-- 開発用のため、通常は非表示で可 -->

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const props = defineProps({
  user_info: Object,
  home: {
    type: Boolean,
    default: false
  },
  session: {
    type: Boolean,
    default: false
  }
})

const move_to_home = () => {
  if(props.user_info.kind_name == 'student') router.push({name:'StudentHome'})
  else router.push({name:'TeacherHome'})
}
const move_to_login = () => router.push({name: 'Login'})
</script>

<template>
  <!--v-row justify='end' class='mb-3'>
    <v-responsive :max-width='300'>
      <v-container>
        <v-row justify='end'>
          {{ user_info.username }}さん ( {{ user_info.email }} ) <br>
          {{ user_info.kind_name }}としてログイン中
        </v-row>
        <v-row justify='end'>
          <v-btn variant='text' color='blue' @click=move_to_home() v-show='!(home||session)'>ホーム</v-btn>
          <v-btn variant='text' color='red' @click='move_to_login()' v-show='!session'>ログアウト</v-btn>
        </v-row>
      </v-container>
    </v-responsive>
  </v-row-->
</template>