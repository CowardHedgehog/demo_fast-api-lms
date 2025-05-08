<script setup>
import axios from 'axios'
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const props = defineProps({
  course_id: Number,
  week_id: Number
})
const week_name = ref()
const week_num = ref()
const order = ref()
const update_answer = ref()

// function
const get_week = () => {
  axios.get(`http://localhost:8000/get_week/${props.week_id}`, {withCredentials: true}).then(function(response){
    // console.log(response.data)
    week_name.value = response.data.week_name
    week_num.value = response.data.week_num
    order.value = response.data.order
    update_answer.value = response.data.update_answer
  })
}
const update_week = () => {
  const params = {
    week_id: props.week_id,
    week_name: week_name.value,
    week_num: week_num.value,
    order: order.value
  }
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  axios.post(`http://localhost:8000/update_week`, params, config).then(function(response){
    console.log(response.data)
    get_week()
  })
}
const delete_week = () => {
  const params = {
    week_id: props.week_id
  }
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  axios.post(`http://localhost:8000/delete_week`, params, config).then(function(response){
    console.log(response.data)
    router.push({name: 'T_Course', params: {course_id: props.course_id}})
  })
}

// created
get_week()
</script>

<template>
  <v-container class='bg-grey-lighten-2 rounded-lg'>
    <v-card>
      <v-card-title class='ma-4'><b><u>コンテンツ情報の編集</u></b></v-card-title>
      <v-card-text>
        <v-form>
          <v-container fluid>
            <v-row>
              <v-col lg='2'>
                <v-card class='bg-grey-lighten-2 d-flex justify-center align-center' height='100%'>
                  <v-card-title>コンテンツ名</v-card-title>
                </v-card>
              </v-col>
              <v-col lg='10'>
                <v-row>
                  <v-col cols='8'>
                    <v-card class='d-flex justify-center align-center' variant='text'>
                      <v-text-field
                        v-model='week_name'
                        label='例）数列の和'
                        :disabled = 'update_answer'
                      />
                    </v-card>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>

            <v-row>
              <v-col lg='2'>
                <v-card class='bg-grey-lighten-2 d-flex justify-center align-center' height='100%'>
                  <v-card-title>回</v-card-title>
                </v-card>
              </v-col>
              <v-col lg='10'>
                <v-row class='d-flex align-center'>
                  <v-col cols='2'>
                    <v-card class='d-flex justify-center align-center' variant='text'>
                      第
                      <v-text-field
                        v-model='week_num'
                        label='例）1'
                        class='mx-2'
                      />
                      回
                    </v-card>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>

            <v-row>
              <v-col lg='2'>
                <v-card class='bg-grey-lighten-2 d-flex justify-center align-center' height='100%'>
                  <v-card-title>並び順</v-card-title>
                </v-card>
              </v-col>
              <v-col lg='10'>
                <v-row>
                  <v-col cols='2'>
                    <v-card class='d-flex justify-center align-center' variant='text'>
                      <v-text-field
                        v-model='order'
                        label='例）1'
                      />
                    </v-card>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
      <v-row class='mb-5 align-center d-flex flex-row justify-center'>
        <v-btn class='bg-primary mx-5' @click='update_week()'>更新</v-btn>
        <v-btn class='bg-red mx-5' @click='delete_week()'>削除</v-btn>
      </v-row>
    </v-card>
  </v-container>
</template>