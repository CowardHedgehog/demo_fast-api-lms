<script setup>
import { useRouter } from 'vue-router'
import pA_Error from '@/components/parts/alerts/pA_Error.vue'
const router = useRouter()
const session_error = true
const moveToLogin = () => {router.push({name: 'C_Login'})}
</script>

<template>
  <v-overlay v-model='session_error' class='align-center justify-center'>
    <pA_Error message='セッションが切れました お手数をおかけしますがログインしなおしてください' />
    <v-row class='justify-center mt-5'>
      <v-btn depressed color='primary' @click='moveToLogin()'>ログイン画面に戻る</v-btn>
    </v-row>
  </v-overlay>
</template>