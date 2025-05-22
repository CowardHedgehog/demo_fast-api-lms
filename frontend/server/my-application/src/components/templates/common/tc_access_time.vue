<script setup>
import axios from 'axios'
import { ref, onMounted, onBeforeUnmount } from 'vue'
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'

dayjs.extend(utc)
dayjs.extend(timezone)
dayjs.tz.setDefault('Asia/Tokyo')

const props = defineProps({
    page: {type: String, default: "none"},
    details: {type: String, default: ""}
})

const s_time = ref()
const e_time = ref()
const date = ref()
const time = ref()

const postAccessTime = () => {
    const params = {
        "date": date.value,
        "page": props.page,
        "time": time.value,
        "details": props.details
    }
    const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
    console.log(params)
    axios.post('https://demo-fast-api-lms.vercel.app/add_access_history', params, config).then(function(response){
    console.log(response.data)
})}

onMounted(() => {
    s_time.value = dayjs.tz().format('YYYY/MM/DD HH:mm:ss')
    date.value = dayjs.tz().format('YYYY-MM-DD')
    // console.log("time_開始",s_time.value)
})

onBeforeUnmount (() => {
    e_time.value = dayjs.tz()
    time.value = e_time.value.diff(s_time.value, 'second')
    // console.log(e_time.value, time.value)
    postAccessTime()
})
</script>

<template>
</template>