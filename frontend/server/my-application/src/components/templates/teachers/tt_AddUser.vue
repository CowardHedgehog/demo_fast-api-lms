<script setup>
import axios from 'axios'
import { ref } from 'vue'
import pA_Error from '@/components/parts/alerts/pA_Error.vue'
import pA_Success from '@/components/parts/alerts/pA_Success.vue'
import pTF_Username from '@/components/parts/text-fields/pTF_Username.vue'
import pTF_Mail from '@/components/parts/text-fields/pTF_Mail.vue'
import pTF_Password from '@/components/parts/text-fields/pTF_Password.vue'

const users = ref()
const add_username = ref('')
const add_email = ref('')
const add_password = ref('')
const re_password = ref('')
const add_kind_name = ref('')
const fileusers = ref([])
const error_msgs = ref([])
const kind_names = ['学生', '教師', 'テスト']
const success_name = ref('')
const is_file = ref(false)
const is_add = ref(false)

// function
const get_users = () => {
  axios.get('https://demo-fast-api-lms.vercel.app/get_users', {withCredentials: true}).then(function(response){
    users.value = response.data
    console.log(users.value)
  })
}
const add_user = () => {
  is_file.value = false
  is_add.value = false
  if(validate_form(add_username.value, add_email.value, add_password.value, add_kind_name.value)) {
    const params = {'username': add_username.value, 'email': add_email.value, 'password': add_password.value, 'kind_name': add_kind_name.value}
    // console.log(JSON.stringify(params))
    const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
    axios.post('https://demo-fast-api-lms.vercel.app/add_user', params, config).then(function(response){
      console.log(response.data)
      if(response.data.success){
        is_add.value = true
        success_name.value = add_username.value
      }else
        error_msgs.value = [response.data.error_msgs]
    })
  }
}
const onFileChange = (fileObject) => {
  let file = fileObject.target.files[0]
  fileusers.value = []
  const reader = new FileReader()
  reader.onload = (e) => {
    const csvData = e.target.result
    // console.log(csvData)
    let lines = csvData.split('\n')
    let data = lines.filter(function(s){return s != ''})
    // console.log(data)
    data.forEach(f => {
      let readusers = f.split(',')
      if(readusers.length != 4) {
        error_msgs.value.push("登録されたcsvファイルのデータが間違っています．修正して，再度登録をお願いします．");
        return
      }
      let user = {
        username: readusers[0],
        email: readusers[1],
        password: readusers[2],
        kind_name: readusers[3].replace('\r', '')
      }
      // console.log(user)
      fileusers.value.push(user);
    })
  }
  reader.readAsText(file)
  console.log(fileusers.value)
}
const add_fileusers = () => {
  if(fileusers.value.length == 0){error_msgs.value.push("csvファイルが選択されていません．ファイルを登録した後に，ボタンを押してください．")}
  else{
    // console.log(fileusers.value)
    const params = []
    for(let fileuser of fileusers.value){
      // console.log(fileuser)
      is_file.value = true
      let is_validation_success = validate_form(fileuser.username, fileuser.email, fileuser.password, fileuser.kind_name)
      // console.log(is_validation_success)
      if(is_validation_success)
        // add_user(fileuser.username, fileuser.email, fileuser.password, add_kind_id)
        params.push({username:fileuser.username, email:fileuser.email, password:fileuser.password, kind_name:fileuser.kind_name})
      else
        return
    }
    // console.log(JSON.stringify(params))
    const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
    axios.post('https://demo-fast-api-lms.vercel.app/add_users', params, config).then(function(response){
      console.log(response.data)
      if(response.data.success){
        is_add.value = true
        success_name.value = add_username.value
      }else
        error_msgs.value = [response.data.error_msgs]
    })
  }
}
const validate_form = (username, email, password, kind_name) => {
  error_msgs.value = []
  if(is_file.value){
    if(username.length == 0)
      error_msgs.value.push("ユーザ名が入力されていない箇所があります．ファイルを修正してください．")
    if(email.length == 0)
      error_msgs.value.push("メールアドレスが入力されていない箇所があります．ファイルを修正してください．")
    if(password.length == 0)
      error_msgs.value.push("パスワードが入力されていない箇所があります．ファイルを修正してください．")
    if(kind_name.length == 0)
      error_msgs.value.push("ユーザ種別が入力されていない箇所があります．ファイルを修正してください．")
    if(users.value.some(e => e.email == email))
      error_msgs.value.push(email + "：すでに登録されています．ファイルを修正してください．")
  }
  else{
    if(username.length == 0 || email.length == 0 || password.length == 0)
      error_msgs.value.push("入力されていない項目があります．登録したい情報を入力してください．\n")
    if(password != re_password.value)
      error_msgs.value.push("再入力されたパスワードが違います．パスワードが合っているか確認してください．\n")
    if(kind_name.length == 0)
      error_msgs.value.push("ユーザ種別が選択されていません．登録したいユーザーに合わせて選択してください．\n")
  }
  return error_msgs.value.length == 0
}

// created
get_users()
</script>

<template>
  <div>
    <h2>ユーザーの追加</h2>

    <pA_Error v-if='error_msgs.length' :message='"○エラー\n" + error_msgs.join("\n")' />
    <pA_Success v-if='!is_file && is_add' :message='success_name + "を登録しました．"' />
    <pA_Success v-if='is_file && is_add' message='CSVファイルからまとめて登録しました' />

    <div class='rounded-lg pa-8 bg-grey-lighten-3 text-no-wrap'>
      <v-form ref='add_user_form'>
        <pTF_Username v-model:username='add_username' complete='off'/>
        <pTF_Mail v-model:email='add_email' class='mt-4' />
        <pTF_Password v-model:password='add_password' class='mt-4' complete='off'/>
        <pTF_Password v-model:password='re_password' class='mt-4' label='パスワードの再入力' complete='off' name='re_password'/>
        <v-select :items='kind_names' v-model='add_kind_name' label='ユーザー種別の選択' class='mt-4'/>
      </v-form>
    </div>
    <v-row class='mt-5 align-center justify-space-around'>
      <v-btn depressed color='primary' @click='add_user()'>登録</v-btn>
    </v-row>

    <h3 class='my-5'>CSVファイルからまとめて登録</h3>
    CSVの形式
    <v-table>
      <thead>
        <tr>
          <th>ユーザー名</th>
          <th>メールアドレス</th>
          <th>パスワード</th>
          <th>ユーザー種別（学生, 教師）</th>
        </tr>
      </thead>
    </v-table>
    <v-row class='align-center justify-space-around mt-3'>
      <v-file-input class='mx-3' id='csv_files' accept='csv' @change="onFileChange"/>
    </v-row>
    <v-row class='align-center justify-space-around'>
      <v-btn depressed color="primary" @click="add_fileusers()">まとめて登録する</v-btn>
    </v-row>
  </div>
</template>