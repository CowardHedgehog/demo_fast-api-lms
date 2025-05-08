<script setup>
import axios from 'axios'
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'


const router = useRouter()
const props = defineProps ({
  user_info: Object,
})
const drawer = ref(false)
const size = ref(10)

watch(size, () => {
  document.querySelector('body').style.fontSize = `${size.value * 2}px`
})

const moveLogin = () => router.push({name: 'C_Login'})
const move_S_Home = () => router.push({name: 'S_Home'})
const move_S_UserSetting = () => router.push({name: 'S_UserSetting'})
const openManual = () => window.open("https://drive.google.com/file/d/1xaJvoquj3cUJIc7RjSeD4cv1Cur5XV1C/view?usp=sharing", '_blank')
const logout =() => {
  axios.post('http://localhost:8000/logout',{}, {withCredentials: true}).then(function(response){
    console.log(response.data)
    moveLogin()
  }).catch(
    function(error){
      console.log(error)
    }
  )
}
</script>

<template>
  <div>
    <v-app-bar color="primary">
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-btn @click='size -= 1'>
        小
      </v-btn>
      <v-btn @click='size += 1'>
        大
      </v-btn>
      <v-btn @click='size = 10'>
        リセット
      </v-btn>
    </v-app-bar>
    <v-navigation-drawer v-model='drawer' absolute temporary style='position:fixed;'>
      <v-list>
        <!--v-list-item height='75' prepend-avatar='https://s3-ap-northeast-1.amazonaws.com/cdn.bibi-star.jp/production/imgs/images/000/428/176/original.?1573470222' :title='user_info.username' :subtitle='user_info.email'/-->
        <v-list-item height='75' prepend-icon='mdi-account' :title='user_info.username' :subtitle='user_info.email' @click='move_S_UserSetting()' />
        <v-divider />
        <v-list-item prepend-icon='mdi-home' title='コース一覧' @click='move_S_Home'/>
        <v-list-item prepend-icon='mdi-view-dashboard' title='ダッシュボード' value='Dashboard'/>
        <!--v-list-item prepend-icon='mdi-card-account-details' title='あなたの学習状況' @click='moveUserProfile'/-->
        <!--v-list-item prepend-icon='mdi-forum' title='コミュニティ' value='StudentCommunity'/>
        <v-list-item prepend-icon='mdi-lock-reset' title='パスワード変更' @click='moveStudentUpdatePassword'/-->
        <v-list-item prepend-icon='mdi-television-guide' title='マニュアル' @click='openManual()'/>
      </v-list>
      <template v-slot:append>
        <div class='pa-2'>
          <v-btn color='red' block @click='logout()'>
            <v-icon>mdi-logout</v-icon>
            ログアウト
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>
  </div>
</template>