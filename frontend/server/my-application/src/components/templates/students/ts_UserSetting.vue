<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// variable
const props = defineProps({
  user_info: Object,
  nickname : String
})
const router = useRouter()

// function
const move_update_password = () => router.push({name: 'S_UpdatePassword'})

// created
</script>

<template>
  <div>
    <h2>ユーザ情報</h2>
    <v-row>
    <v-container class='mt-5 bg-grey-lighten-3'>
      <v-table>
        <tbody>
          <tr>
            <th><b>ユーザ名</b></th>
            <th>{{ user_info.username }}</th>
            <th />
          </tr>
          <tr>
            <th><b>メールアドレス</b></th>
            <th>{{ user_info.email }}</th>
            <th />
          </tr>
          <tr>
            <th><b>ニックネーム（コミュニティ内での）</b></th>
            <th>{{ nickname }}</th>
            <!--<th><v-btn color='primary' icon='mdi-lead-pencil' /></th>-->          
          </tr>
          <tr>
            <th><b>パスワード</b></th>
            <th>●●●●●●●●</th>
            <th><v-btn color='primary' icon='mdi-lead-pencil' @click='move_update_password()'/></th>
          </tr>
        </tbody>
      </v-table>
    </v-container>
    </v-row>
  </div>
</template>