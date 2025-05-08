<script setup>
import { ref } from 'vue'
import axios from 'axios'

const nickname = ref('')
const loading = ref(false)
const error = ref('')
const emit = defineEmits(['nickname-updated'])

const rules = [
  v => !!v || 'ニックネームを入力してください',
  v => (v && v.length <= 8) || 'ニックネームは8文字以内で入力してください'
]

const updateNickname = async () => {
  if (!nickname.value) return
  
  loading.value = true
  error.value = ''

  try {
    const params = {
      nickname: nickname.value
    }
    const config = {
      headers: { 'Content-Type': 'application/json' },
      withCredentials: true
    }
    
    await axios.post('http://localhost:8000/set_nickname', params, config)
    emit('nickname-updated', nickname.value)
  } catch (e) {
    console.error('Error setting nickname:', e)
    error.value = 'ニックネームの設定に失敗しました'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-card class="pa-4" flat>
    <v-card-text>
      <h3 class="text-h6 mb-4">ニックネームを設定</h3>
      <p class="text-body-1 mb-6">
        他のユーザーに表示される名前を設定してください。
      </p>
      
      <v-form @submit.prevent="updateNickname">
        <v-text-field
          v-model="nickname"
          label="ニックネーム"
          :rules="rules"
          :error-messages="error"
          variant="outlined"
          class="mb-4"
          maxlength="8"
          counter
        ></v-text-field>

        <v-btn color="primary" block
          :loading="loading"
          :disabled="!nickname"
          @click="updateNickname"
          class="mt-4"
        >
          設定する
        </v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.v-card {
  max-width: 400px;
  margin: 0 auto;
}
</style> 