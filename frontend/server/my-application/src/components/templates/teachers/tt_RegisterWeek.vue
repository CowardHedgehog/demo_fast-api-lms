<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import pA_Error from '@/components/parts/alerts/pA_Error.vue'
import pTF_WeekName from '@/components/parts/text-fields/pTF_WeekName.vue'
import pTF_Number from '@/components/parts/text-fields/pTF_Number.vue'
import pB_Btn from '@/components/parts/btns/pB_Btn.vue'

// variable
const props = defineProps({
  course_id: {type: Number, required: true}
})
const router = useRouter()
const message = ref("○ エラー")
const error_msgs = ref([])
const weekName = ref("線形代数学_第1週")
const order = ref()
const week_num = ref()
const files = ref()

// function
const validate_form = () => {
  error_msgs.value = []
  if(files.value.length == 0) error_msgs.value.push('登録するコースのフォルダを選択してください. ')
  if(error_msgs.value.length > 0) error_msgs.value.forEach(function(m) {message.value = message.value + "\n　・" + m})
  return error_msgs.value.length == 0
}
const register_week = () => {
  if(validate_form()) {
    const params = {
      'week_name': weekName.value,
      'week_num': week_num.value,
      'order': order.value,
      'course_id': props.course_id,
      'week_files': files.value
    }
    const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
    axios.post(`http://localhost:8000/register_week`, params, config).then(function(response){
      console.log(response.data)
      if(response.data.success) move_to_course()
      else {
        error_msgs.value = [response.data.error_msg]
        if(error_msgs.value.length > 0) error_msgs.value.forEach(function(m) {message.value = message.value + "\n　・" + m})
      }
    })
  }
}
const onFileChange = (fileObjects) => {
  files.value = []
  const cfiles = fileObjects.target.files
  const fileForUpload = []
  for(let file of cfiles){
    let filePath = file.webkitRelativePath
    let fileReader = new FileReader()
    console.log("file type: " + file.type)
    if(file.type.indexOf('image') != -1){
      fileReader.onload = function(e) {
        let result = ""
        let int8_array = new Uint8Array(e.target.result)
        var i, str, num = int8_array.length
        for(i = 0; i < num; i++){
          if(int8_array[i] < 0x10) str = "0" + int8_array[i].toString(16)
          else str = int8_array[i].toString(16)
          result += "\\x" + str
        }
        console.log(result)
        fileForUpload.push({file_path: filePath, file_text: result})
      }
      fileReader.readAsArrayBuffer(file)
    }else{
      fileReader.onload = function(e) {
        console.log(e.target.result)
        fileForUpload.push({file_path: filePath, file_text: e.target.result})
      }
      fileReader.readAsText(file)
    }
  }
  files.value = fileForUpload
}
const move_to_course = () => router.push({name: 'T_Course', params: {course_id: props.course_id}})
// created

</script>

<template>
  <div>
    <pA_Error :message='message' v-if='error_msgs.length > 0'/>
    <div class='pa-8 mt-6 rounded-lg bg-grey-lighten-3 text-no-wrap'>
      <pTF_WeekName v-model:week_name='weekName' />
      <v-row class='align-center justify-space-around'>
        <pTF_Number v-model:num='week_num' label='第○週、第○回' hint='数値のみを入力してください'/>
        <pTF_Number v-model:num='order' label='並び順' hint='数値のみを入力してください　昇順でコンテンツが並びます'/>
      </v-row>
      <v-row class='align-center justify-space-around'>
        <input id='image' @change='onFileChange' type='file' webkitdirectory>
      </v-row>
      <v-row class='align-center justify-space-around mt-8'>
        <pB_Btn text='コースを登録' @func='register_week'/>
      </v-row>
    </div>
  </div>
</template>