<!-- 科目選択前のセレクト -->

<script setup>
import { useRouter } from 'vue-router'
import pSelectPageTab from '@/components/parts/btns/pB_TabItem.vue'

const router = useRouter()
const porps = defineProps({
  location: String,
})
const move_T_Home = () => router.push({name: 'T_Home'})
const move_T_AddUser = () => router.push({name: 'T_AddUser'})
const move_T_UserSetting = () => router.push({name: 'T_UserSetting'})
</script>

<template>
  <div>
    <v-row>
      <pSelectPageTab :location='location' page='T_Home'            tab-name='コース一覧'           :move='move_T_Home'/>
      <pSelectPageTab :location='location' page='T_AddUser'         tab-name='ユーザー登録'         :move='move_T_AddUser' />
      <pSelectPageTab :location='location' page='T_UserSetting'     tab-name='ユーザ情報'           :move='move_T_UserSetting'/>

    </v-row>
    <v-divider class='my-3' :thickness='3'/>
  </div>
</template>