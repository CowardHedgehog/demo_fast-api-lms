<!-- 科目選択前のセレクト -->

<script setup>
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ref} from 'vue'
import pSelectPageTab from '@/components/parts/btns/pB_TabItem.vue'
import { useTheme } from 'vuetify'

const router = useRouter()
const theme = useTheme()
const menu = ref(false)
const porps = defineProps({
  location: String,
})
const themes = ref([
  { name: 'theme1', displayName: 'light blue' },
  { name: 'theme2', displayName: 'green' },
  { name: 'theme3', displayName: 'purple' },
  { name: 'theme4', displayName: 'red' },
  { name: 'theme5', displayName: 'black' },
  { name: 'theme6', displayName: 'school' },
  { name: 'theme7', displayName: 'pink'},
  { name: 'theme8', displayName: 'orange'},
  { name: 'theme9', displayName: 'blue'},
  { name: 'theme10', displayName: 'random'}
])
const selectedTheme = ref('light')
const themeName = ref('')

const selectTheme = (themeNameValue) => {
  selectedTheme.value = themeNameValue
  themeName.value = themeNameValue
}
const applyTheme = () => {
  theme.global.name.value = selectedTheme.value
  menu.value = false
  const params = {
    'theme': themeName.value
  }
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  
  axios.post('https://demo-fast-api-lms.vercel.app/register_theme', params,config, { withCredentials: true })
    .then(response => {
      console.log('レスポンスデータ:', response.data)
    })
    .catch(error => {
      console.error('テーマの登録に失敗しました:')
      console.error('エラーレスポンス:', error.response?.data)
      console.error('エラーステータス:', error.response?.status)
      console.error('エラーメッセージ:', error.message)
    })
}
const fetchThemeFromDB = () => {
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  try {
    axios.get('https://demo-fast-api-lms.vercel.app/get_theme', config).then(response => {
      const data = response.data;
      console.log('レスポンスデータ:', data);
      theme.global.name.value = data;
    }).catch(error => {
      console.error("エラーが発生しました:", error);
      console.error("ステータスコード:", error.response?.status);
      console.error("レスポンスデータ:", error.response?.data);
      console.error("メッセージ:", error.message);
      throw new Error("テーマの取得に失敗しました");
    });
  } catch (error) {
    console.error("エラーが発生しました:", error);
    console.error("詳細情報:", error.stack);
    return 'light';
  }
}
const openThemeMenu = () => {menu.value = true}
const moveStudentHome = () => router.push({name: 'S_Home'})
const moveUserSetting = () => router.push({name: 'S_UserSetting'})
const goToExternalLink1 = () => {window.open('https://w3e.kanazawa-it.ac.jp/math/stem/', '_blank')}

fetchThemeFromDB()
</script>

<template>
  <div>
    <v-row>
      <pSelectPageTab :location='location' page='S_Home'            tab-name='コース一覧'        :move='moveStudentHome'/>
      <pSelectPageTab :location="location" @click = 'goToExternalLink1' tab-name = '数理工ナビ'/>
      <pSelectPageTab :location="location" @click = 'openThemeMenu' tab-name="テーマ変更"/>
      <pSelectPageTab :location='location' page='S_UserSetting'     tab-name='ユーザ情報'        :move='moveUserSetting'/>
    </v-row>
    <v-divider class='my-3' :thickness='3'/>
    <v-dialog v-model="menu" max-width="600">
      <v-card>
        <v-card-title class="text-h6 font-weight-bold text-center">テーマを選択</v-card-title>
        <v-card-text>
          <v-row dense class="pa-2">
            <v-col 
              v-for="theme in themes" :key="theme.name" cols="6" class="d-flex justify-center align-center">
              <v-btn block :class="{'selected-theme': selectedTheme === theme.name}" @click="selectTheme(theme.name)" class="theme-btn">
                <b>{{ theme.displayName }}</b>
              </v-btn>
            </v-col>
          </v-row>
        <div class="theme-preview mt-3 text-center">
          <v-divider />
          <div :class="`preview-${selectedTheme}`" class="pa-4 mt-2">
            <p class="text-h6 font-weight-bold">プレビュー</p>
          </div>
        </div>
        </v-card-text>
          <v-card-actions>
            <v-btn text @click="menu = false">キャンセル</v-btn>
            <v-btn text color="primary" @click="applyTheme">適用</v-btn>
          </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
.preview-theme1 {
  background-color: #3b96c3;
  color: #e7881a;
}

.preview-theme2 {
  background-color: #7bc1bb;
  color: #d07986;
}

.preview-theme3 {
  background-color: #A066dd;
  color: #99D0F0;
}

.preview-theme4 {
  background-color: #cf2b0e;
  color: #162e3a;
}

.preview-theme5 {
  background-color: #232122;
  color: #7ba4a8;
}

.preview-theme6 {
  background-color: #2C6B6A;
  color: #C39140;
}
.preview-theme7 {
  background-color: #f18d9e;
  color: #5bc8ac;
}
.preview-theme8 {
  background-color: #FAA755;
  color: #DAC4A5;
}
.preview-theme9{
  background-color: #1C6BC2;
  color: #48a9a6;
}
.preview-theme10{
  background: linear-gradient(270deg, #ff9a9e, #fad0c4, #fbc2eb, #a18cd1);
  background-size: 600% 600%;
  animation: rainbowBackground 6s ease infinite;
  color: #fff;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}
@keyframes rainbowBackground {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.theme-btn {
  max-height: 100px;
  color: inherit;
  border-radius: 8px;
  transition: all 0.3s ease;
}
.theme-btn:active {
  transform: scale(0.97);
  background-color: rgba(0, 0, 0, 0.1);
}
</style>