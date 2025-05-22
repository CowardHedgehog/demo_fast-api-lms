<script setup>
import { ref, computed, reactive } from 'vue'
import axios from 'axios'

const props = defineProps({
  dialog: {type: Boolean, default:false},
  week_id: Number
})

const file = reactive({
  imgdata: null,
  name: '',
  week_id: props.week_id
})

const img_data = ref(null)

const emit = defineEmits(["update:dialog"])
const reloadImages = () => {emit('reloadImg')}
const setDialog = computed({
  get: () => props.dialog,
  set: (newVal) => emit('update:dialog', newVal)
})

const drawImage = (src) => {
  const canvas = document.getElementById('main')
  const ctx = canvas.getContext('2d')
  ctx.clearRect(0, 0, 300, 300)
  const image = new Image()
  image.src = src
  image.onload = () => {
    ctx.drawImage(image, 0, 0, 300, 300)
  }
}

const readFile = () => {
  if (img_data.length == 0) return
  const fileReader = new FileReader()
  fileReader.onload = () => {drawImage(fileReader.result)}
  fileReader.readAsDataURL(img_data.value)
}

const add_image = () => {
  const fileReader = new FileReader()
  fileReader.onload = () => {
    let result = ""
    let int8_array = new Uint8Array(fileReader.result)
    var i, str, num = int8_array.length
    for(i = 0; i < num; i++){
      if(int8_array[i] < 0x10) str = "0" + int8_array[i].toString(16)
      else str = int8_array[i].toString(16)
      result += "\\x" + str
    }
    file.imgdata = result
    const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
    console.log(file)
    axios.post('https://demo-fast-api-lms.vercel.app/image', file, config).then(function(response){
      console.log(response.data)
      setDialog.value = false
    reloadImages()
    })
  }
  fileReader.readAsArrayBuffer(img_data.value)
}


</script>

<template>
  <v-dialog v-model='setDialog'>
    <v-sheet width='1200' class='mx-auto'>
      <v-sheet class='my-10 mx-10 justify-center'>
        <v-row>
          <v-col cols='8'>
            <v-file-input v-model='img_data' accept='image/png, image/jpeg' @update:modelValue='readFile' label='画像ファイルを選択してください'></v-file-input>
            <v-text-field v-model='file.name' label='画像名' class='mt-5'></v-text-field>
          </v-col>
          <v-col cols='4'>
            <canvas id='main' height='300'></canvas>
          </v-col>
        </v-row>
        <v-btn class='d-flex justify-end mx-auto mr-15 mt-10' color='primary' @click='add_image'>追加</v-btn>
      </v-sheet>
    </v-sheet>
  </v-dialog>
</template>