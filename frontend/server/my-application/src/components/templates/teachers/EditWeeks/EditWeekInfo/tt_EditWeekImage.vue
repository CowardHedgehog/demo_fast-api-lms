<script setup>
import axios from 'axios'
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import pD_AddImage from '../../../../parts/dialogs/pD_AddImage.vue'

const router = useRouter()
const props = defineProps({
  course_id: Number,
  week_id: Number
})

const add_image = ref(false)
const images = ref([])

// function
const get_images = () => {
    axios.get(`http://localhost:8000/get_images/${props.week_id}`, {withCredentials: true}).then(function(response){
    // console.log(response.data)
    images.value = response.data
    console.log(images.value)
  })
}

const delete_image = (id) => {
  axios.delete(`http://localhost:8000/image/${id}`, {withCredentials: true}).then(function(response){
    console.log(response.data)
    get_images()
  })
}

// created
get_images()
</script>

<template>
  <v-container class='bg-grey-lighten-2 rounded-lg'>
    <pD_AddImage v-model:dialog='add_image' :week_id='props.week_id' @reloadImg='get_images'/>
    <v-card>
      <v-card-title class='ma-4'><b><u>画像</u></b></v-card-title>
      <v-btn class='d-flex justify-end mx-auto mr-15' color='primary' @click='add_image=true; console.log(add_image);'>追加</v-btn>
      <v-card-text>
        <v-row align="center" justify="center" dense>
          <v-col v-for='image in images' :key='image.id' cols='12' md='6'>
            <v-card class='mx-auto' variant='outlined'>
              <v-img :src='`http://localhost:8000/get_image/${image.id}`' width='200' height="200" class="mx-auto" />
              <v-divider thickness="3"></v-divider>
              <v-card-subtitle class='text-black d-flex justify-center'>{{ image.name }}</v-card-subtitle>
              <v-card-actions class='d-flex justify-center'>
                <v-btn color='warning' @click='delete_image(image.id)'><v-icon>mdi-delete</v-icon></v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>