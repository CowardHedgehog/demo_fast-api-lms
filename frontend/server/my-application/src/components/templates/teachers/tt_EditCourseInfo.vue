<script setup>
import axios from 'axios'
import { ref, watch } from 'vue'
import { splitDate, combineDate } from '@/components/methods/display_format.js'
import { useRouter } from 'vue-router'

const router = useRouter()
const props = defineProps({
  course_id: Number
})
const course_name = ref('')
const start_date_time = ref([...Array(5)])
const end_date_time = ref([...Array(5)])
const weeks = ref()
const update_answer = ref()
const delete_answer = ref()
const dialog = ref()

const get_course = () => {
  axios.get(`https://demo-fast-api-lms.vercel.app/get_course_info/${props.course_id}`, {withCredentials: true}).then(function(response){
    console.log(response.data)
    course_name.value = response.data.course_name
    start_date_time.value = splitDate(response.data.start_date_time)
    end_date_time.value = splitDate(response.data.end_date_time)
    weeks.value = response.data.weeks
    update_answer.value = response.data.update_answer
    delete_answer.value = response.data.delete_answer
  })
}
const update_course = () => {
  const params = {
    course_id: props.course_id,
    course_name: course_name.value,
    start_date_time: combineDate(start_date_time.value[0], start_date_time.value[1], start_date_time.value[2], start_date_time.value[3], start_date_time.value[4]),
    end_date_time: combineDate(end_date_time.value[0], end_date_time.value[1], end_date_time.value[2], end_date_time.value[3], end_date_time.value[4]),
    weeks: weeks.value
  }
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  console.log(params)
  axios.post(`https://demo-fast-api-lms.vercel.app/update_course`, params, config).then(function(response){
    console.log(response.data)
    dialog.value = response.data.success
    get_course()
    setTimeout(() => {
      dialog.value = false
    }, 1000)
  })
}
const delete_course = () => {
  const params = {
    course_id: props.course_id,
  }
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  console.log(params)
  axios.post(`https://demo-fast-api-lms.vercel.app/delete_course`, params, config).then(function(response){
    console.log(response.data)
    router.push({name: 'T_Home'})
  })
}

// created
get_course()

</script>

<template>
  <div>
    <h2>コース情報の編集</h2>
    <v-dialog v-model='dialog' transition='dialog-top-transition' content-class='dialog' persistent>
      <v-row class='d-flex align-start justify-center'>
        <v-sheet class='rounded-lg'>
          <v-sheet class='my-5 mx-15'>
            <h3 class='d-flex justify-center align-end'>更新しました</h3>
          </v-sheet>
        </v-sheet>
      </v-row>
    </v-dialog>

    <v-container class='mt-3 bg-grey-lighten-2 rounded-lg'>
      <v-card>
        <v-card-text>
          <v-form>
            <v-container fluid>
              <v-row>
                <v-col lg='2'>
                  <v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                    <v-card-title>コース名</v-card-title>
                  </v-card>
                </v-col>
                <v-col lg='10'>
                  <v-row>
                    <v-col cols='8'>
                      <v-card class='d-flex justify-center align-center' variant='text'>
                        <v-text-field
                          v-model='course_name'
                          label='例）線形代数学_1AA1'
                          :disabled = '!update_answer'
                        />
                      </v-card>
                    </v-col>
                  </v-row>
                </v-col>
              </v-row>

              <v-row class='my-3'>
                <v-col lg='2'>
                  <v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                    <v-card-title>表示開始日時</v-card-title>
                  </v-card>
                </v-col>
                <v-col lg='10'>
                  <v-row class='d-flex align-center'>
                    <v-col cols='2'><v-card class='d-flex justify-center align-center' variant='text'>
                      <v-text-field
                        v-model='start_date_time[0]'
                        label='例）2024'
                        :disabled = '!update_answer'
                      />
                    </v-card></v-col>
                    年
                    <v-col cols='1'><v-card class='d-flex justify-center align-center' variant='text'>
                      <v-text-field
                        v-model='start_date_time[1]'
                        label='4'
                        :disabled = '!update_answer'
                      />
                    </v-card></v-col>
                    月
                    <v-col cols='1'><v-card class='d-flex justify-center align-center' variant='text'>
                      <v-text-field
                        v-model='start_date_time[2]'
                        label='1'
                        :disabled = '!update_answer'
                      />
                    </v-card></v-col>
                    日
                  </v-row>
                  <v-row class='d-flex align-center'>
                    <v-col cols='2'><v-card class='d-flex justify-center align-center' variant='text'>
                      <v-text-field
                        v-model='start_date_time[3]'
                        label='例）00'
                        :disabled = '!update_answer'
                      />
                    </v-card></v-col>
                    時
                    <v-col cols='2'><v-card class='d-flex justify-center align-center' variant='text'>
                      <v-text-field
                        v-model='start_date_time[4]'
                        label='00'
                        :disabled = '!update_answer'
                      />
                    </v-card></v-col>
                    分
                  </v-row>
                </v-col>
              </v-row>

              <v-row class='my-3'>
                <v-col lg='2'>
                  <v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                    <v-card-title>表示終了日時</v-card-title>
                  </v-card>
                </v-col>
                <v-col lg='10'>
                  <v-row class='d-flex align-center'>
                    <v-col cols='2'><v-card class='d-flex justify-center align-center' variant='text'>
                      <v-text-field
                        v-model='end_date_time[0]'
                        label='例）2025'
                        :disabled = '!update_answer'
                      />
                    </v-card></v-col>
                    年
                    <v-col cols='1'><v-card class='d-flex justify-center align-center' variant='text'>
                      <v-text-field
                        v-model='end_date_time[1]'
                        label='3'
                        :disabled = '!update_answer'
                      />
                    </v-card></v-col>
                    月
                    <v-col cols='1'><v-card class='d-flex justify-center align-center' variant='text'>
                      <v-text-field
                        v-model='end_date_time[2]'
                        label='31'
                        :disabled = '!update_answer'
                      />
                    </v-card></v-col>
                    日
                  </v-row>
                  <v-row class='d-flex align-center'>
                    <v-col cols='2'><v-card class='d-flex justify-center align-center' variant='text'>
                      <v-text-field
                        v-model='end_date_time[3]'
                        label='例）23'
                        :disabled = '!update_answer'
                      />
                    </v-card></v-col>
                    時
                    <v-col cols='2'><v-card class='d-flex justify-center align-center' variant='text'>
                      <v-text-field
                        v-model='end_date_time[4]'
                        label='59'
                        :disabled = '!update_answer'
                      />
                    </v-card></v-col>
                    分
                  </v-row>
                </v-col>
              </v-row>

              <v-row class='my-3'>
                <v-col lg='2'>
                  <v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                    <v-card-title>回数</v-card-title>
                  </v-card>
                </v-col>
                <v-col lg='10'>
                  <v-row>
                    <v-col cols='2'>
                      <v-card class='d-flex justify-center align-center' variant='text'>
                        <v-text-field
                          v-model='weeks'
                          label='例）15'
                          :disabled = '!update_answer'
                        />
                        回
                      </v-card>
                    </v-col>
                  </v-row>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </v-card-text>
        <v-row class='mb-5 d-flex align-center justify-center'>
          <v-btn v-if='update_answer' class='bg-primary' @click='update_course()'>更新</v-btn>
          <v-btn v-if='delete_answer' class='bg-red mx-5' @click='delete_course()'>削除</v-btn>
        </v-row>
      </v-card>
    </v-container>
  </div>
</template>

<style>
.dialog {
  top: 0;
}
</style>