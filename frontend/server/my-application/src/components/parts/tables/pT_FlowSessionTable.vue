<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { processDate } from '@/components/methods/display_format'

// variable
const router = useRouter()
const props = defineProps({
  create:           {type: Boolean, default: false},
  course_id:        {type: Number, required: true},
  week_id:          {type: Number, required: true},
  flow_id:          {type: Number, required: true},
  restart_session:  {type: Boolean},
  move:             {type: Function}
})
const cnt = ref(1)
const flow_sessions = ref({})

// function
const get_flow_sessions = () => {
  axios.get(`https://demo-fast-api-lms.vercel.app/get_flow_sessions/${props.flow_id}`, {withCredentials: true}).then(function(response){
  flow_sessions.value = response.data
  // console.log(flow.value)
  })
}
const restart_flow_session = (flow_session_id) => {
  if(props.create){ router.push({name:'T_FlowSession', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id, flow_session_id: flow_session_id, page: 1}})}
  else{             router.push({name:'S_FlowSession', params: {course_id: props.course_id, week_id: props.week_id, flow_id: props.flow_id, flow_session_id: flow_session_id, page: 1}})}
}

// created
get_flow_sessions()
</script>

<template>
  <div v-if='flow_sessions && flow_sessions.length != 0'>
    <h3 class='mb-3'>演習問題の履歴</h3>
    <v-table class='text-center' density="comfortable" fixed-header>
      <thead>
        <th>#</th>
        <th>開始時刻</th>
        <th>終了時刻</th>
        <th>テスト解答済み</th>
        <th>正答率</th>
        <th>再開</th>
      </thead>
      <tbody>
        <tr v-for='(flow_session, index) in flow_sessions' :key='flow_session.id'>
          <td>{{ index + 1 }}</td>
          <td>{{ processDate(flow_session.start_date_time) }}</td>
          <td>{{ processDate(flow_session.finish_date_time) }}</td>
          <td>
            <div v-if='flow_session.is_finished'>解答済</div>
            <div v-else>未解答</div>
          </td>
          <td>{{ flow_session.flow_session_grade.toFixed(1) }}%</td>
          <td><v-btn class='bg-primary' v-if='restart_session || !flow_session.is_finished' @click='restart_flow_session(flow_session.id)'>再開</v-btn></td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>