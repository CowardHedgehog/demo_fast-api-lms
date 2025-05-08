<script setup>
// import
import { computed } from 'vue'
//import pDatePicker from '@/components/parts/others/pDatePicker.vue'

// variable
const props = defineProps({
  date: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    defalut: ''
  },
  rule: Number,
})
const emit = defineEmits(["update:date"])
// rules 0:start 1:end
const rules = [[
    v => !!v || '開始日は必須です.',
    v => {
      if(!v) return true
      const pattern = /\d{4}-\d{2}-\d{2}/
      if(!pattern.test(v))
        return '入力形式が不正です. 例: 2022-02-04'
      return true
    },
    v => {
      if(!v) return true
      const pattern = /\d{4}-\d{2}-\d{2}/
      if(pattern.test(v)){
        const date_time_splited = v.split(" ")
        const date_splited = date_time_splited[0].split("-")
        if (date_splited[0] > 2100 || date_splited[0] < 2000)
          return "年は2000~2100の間で入力してください. " 
      }
      return true
    },
    v => {
      if(!v) return true
      const pattern = /\d{4}-\d{2}-\d{2}/
      if(pattern.test(v)){
        const date_time_splited = v.split(" ")
        const date_splited = date_time_splited[0].split("-")
        if (date_splited[1] > 12 || date_splited[1] < 1)
          return "月は1~12の間で入力してください. " 
      }
      return true
    },
    v => {
      if(!v) return true
      const pattern = /\d{4}-\d{2}-\d{2}/
      if(pattern.test(v)){
        const date_time_splited = v.split(" ")
        const date_splited = date_time_splited[0].split("-")
        if (date_splited[1] == 2){
          if (date_splited[0]%400==0){
            if (date_splited[2] > 29 || date_splited[2] < 0)
              return "日の値が不正です. " 
          }else if(date_splited[0]%100==0){
            if (date_splited[2] > 28 || date_splited[2] < 1)
              return "日の値が不正です. "
          }else if(date_splited[0]%4==0){
            if (date_splited[2] > 29 || date_splited[2] < 1)
              return "日の値が不正です. "
          }else{
            if (date_splited[2] > 28 || date_splited[2] < 1)
              return "日の値が不正です. "
          }
        }
        else if (["1","3","5","7","8","10","12"].includes(date_splited[1])){
          if (date_splited[2] > 31 || date_splited[2] < 1)
            return "日の値が不正です. " 
        }else{
          if (date_splited[2] > 30 || date_splited[2] < 1)
            return `日の値が不正です.` 
        }
      }
      return true
    },
  ],[
    v => {
      if(!v) return true
      const pattern = /\d{4}-\d{2}-\d{2}/
      if(!pattern.test(v))
        return '入力形式が不正です. 例: 2022-02-04 '
      return true
    },
    v => {
      if(!v) return true
      const pattern = /\d{4}-\d{2}-\d{2}/
      if(pattern.test(v)){
        const date_splited = v.split("-")
        if (date_splited[0] > 2100 || date_splited[0] < 2000)
          return "年は2000~2100の間で入力してください. " 
      }
      return true
    },
    v => {
      if(!v) return true
      const pattern = /\d{4}-\d{2}-\d{2}/
      if(pattern.test(v)){
        const date_splited = v.split("-")
        if (date_splited[1] > 12 || date_splited[1] < 1)
          return "月は1~12の間で入力してください. " 
      }
      return true
    },
    v => {
      if(!v) return true
      const pattern = /\d{4}-\d{2}-\d{2}/
      if(pattern.test(v)){
        const date_splited = v.split("-")
        if (date_splited[1] == 2){
          if (date_splited[0]%400==0){
            if (date_splited[2] > 29 || date_splited[2] < 0)
              return "日の値が不正です. " 
          }else if(date_splited[0]%100==0){
            if (date_splited[2] > 28 || date_splited[2] < 1)
              return "日の値が不正です. "
          }else if(date_splited[0]%4==0){
            if (date_splited[2] > 29 || date_splited[2] < 1)
              return "日の値が不正です. "
          }else{
            if (date_splited[2] > 28 || date_splited[2] < 1)
              return "日の値が不正です. "
          }
        }
        else if (["1","3","5","7","8","10","12"].includes(date_splited[1])){
          if (date_splited[2] > 31 || date_splited[2] < 1)
            return "日の値が不正です. " 
        }else{
          if (date_splited[2] > 30 || date_splited[2] < 1)
            return `日の値が不正です.` 
        }
      }
      return true
    },
  ]
]

// function
const setDate = computed({
  get: () => props.date,
  set: (newVal) => emit('update:date', newVal)
})

// created

</script>

<template>
  <v-col>
    <v-text-field :rules="rules[rule]" :label=label bg-color='white' v-model='setDate'>
      <template v-slot:append-outer>
        <pDatePicker v-model:date='setDate' />
      </template>
    </v-text-field>
  </v-col>
</template>