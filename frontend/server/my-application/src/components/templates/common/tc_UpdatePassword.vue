<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'
import pA_Success from '@/components/parts/alerts/pA_Success.vue'
import pA_Error from '@/components/parts/alerts/pA_Error.vue'
import pB_Btn from '@/components/parts/btns/pB_Btn.vue'
import pTF_Password from '@/components/parts/text-fields/pTF_Password.vue'

// variable
const props = defineProps({
  user_info: {type: Object, required: true}
})
const old_pswd = ref("")
const new_pswd = ref("")
const re_pswd = ref("")
const success = ref()
const success_message = ref("")
const error_message = ref("")
const loading = ref(false)
const emit = defineEmits(['password-updated'])

// function
const validate_form = () => {
  error_message.value = ""
  if(new_pswd.value != re_pswd.value) error_message.value = '再入力されたパスワードが違います．新しいパスワードと一致しているか確認してください．'
  if(old_pswd.value == new_pswd.value) error_message.value = '現在のパスワードと新しいパスワードが同じです．変更する場合は異なるパスワードを入力してください．'
  if(old_pswd.value.length == 0) error_message.value = '現在のパスワード欄が入力されていません．'
  if(new_pswd.value.length == 0) error_message.value = '新しいパスワード欄が入力されていません．'
  if(re_pswd.value.length == 0) error_message.value = '新しいパスワード（再入力）欄が入力されていません．'
  if(error_message.value.length != 0) success.value = false
  return error_message.value.length == 0
}
const update_password = async () => {
  if (!validate_form()) return
  loading.value = true
  error_message.value = ''

  try {
    const params = {
      "email": props.user_info.email,
      "old_password": old_pswd.value,
      "new_password": new_pswd.value
    }
    const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
    const response = await axios.post(`http://localhost:8000/update_password`, params, config)
    
    // APIからのレスポンスを確認
    if (response.data.success) {
      emit('password-updated')
      success.value = true
      success_message.value = "パスワードが更新されました。　　" + new_pswd.value
    } else {
      // APIからのエラーメッセージを表示
      success.value = false
      error_message.value = response.data.error_msg || 'パスワードの更新に失敗しました'
    }
  } catch (e) {
    console.error('Error updating password:', e)
    success.value = false
    error_message.value = 'パスワードの更新に失敗しました'
  } finally {
    loading.value = false
  }
}
const update_password_checked = () => {if(validate_form()) update_password()}
</script>

<template>
  <div>
    <h2>パスワードの更新</h2>
    <v-container>
      <pA_Error v-if='success === false && error_message != ""' :text='error_message'/>
      <pA_Success v-if='success === true && success_message != ""' :text='success_message'/>
      <v-responsive class='pa-8 bg-grey-lighten-3'>
        <pTF_Password class='pb-6' v-model:password='old_pswd' label='現在のパスワード'/>
        <pTF_Password class='pb-6' v-model:password='new_pswd' label='新しいパスワード'/>
        <pTF_Password class='pb-6' v-model:password='re_pswd' label='新しいパスワード（再入力）'/>
        <pB_Btn position='center' text='パスワードを変更する' @func='update_password_checked'/>
      </v-responsive>
    </v-container>
  </div>
</template>