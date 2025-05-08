<script setup>
// import
import { computed } from 'vue'
// import pDatePicker from '@/components/parts/others/pDatePicker.vue'

// variable
const props = defineProps({
  time: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    defalut: ''
  },
  rule: Number,
})
const emit = defineEmits(["update:time"])
// rules 0:start 1:end
const rules = [[
    v => !!v || '開始時間は必須です.',
    v => {
      if(!v) return true
      const pattern = /\d{2}:\d{2}:\d{2}/
      if(!pattern.test(v))
        return '入力形式が不正です. 例: 13:30:30'
      return true
    },
    v => {
      if(!v) return true
      const pattern = /\d{2}:\d{2}:\d{2}/
      if(pattern.test(v)){
        const time_splited = v.split(":")
        if (time_splited[0] > 23 || time_splited[0] < 0)
          return "時は0~23の間で入力してください. " 
      }
      return true
    },
    v => {
      if(!v) return true
      const pattern = /\d{2}:\d{2}:\d{2}/
      if(pattern.test(v)){
        const time_splited = v.split(":")
        if (time_splited[1] > 59 || time_splited[1] < 0)
          return "分は0~59の間で入力してください. " 
      }
      return true
    },
    v => {
      if(!v) return true
      const pattern = /\d{2}:\d{2}:\d{2}/
      if(pattern.test(v)){
        const time_splited = v.split(":")
        if (time_splited[2] > 59 || time_splited[2] < 0)
          return "秒は0~59の間で入力してください. " 
      }
      return true
    },
  ],[
      v => {
        if(!v) return true
        const pattern = /\d{2}:\d{2}:\d{2}/
        if(!pattern.test(v))
          return '入力形式が不正です. 例: 13:30:30 '
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const time_splited = v.split(":")
          if (time_splited[0] > 23 || time_splited[0] < 0)
            return "時は0~23の間で入力してください. " 
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const time_splited = v.split(":")
          if (time_splited[1] > 59 || time_splited[1] < 0)
            return "分は0~59の間で入力してください. " 
        }
        return true
      },
      v => {
        if(!v) return true
        const pattern = /\d{2}:\d{2}:\d{2}/
        if(pattern.test(v)){
          const time_splited = v.split(":")
          if (time_splited[2] > 59 || time_splited[2] < 0)
            return "秒は0~59の間で入力してください. " 
        }
        return true
      },
    ]
]

// function
const setTime = computed({
  get: () => props.time,
  set: (newVal) => emit('update:time', newVal)
})

// created

</script>

<template>
  <v-col>
    <v-text-field :rules="rules[rule]" :label=label bg-color='white' v-model='setTime' error-count='10'>
      <template v-slot:append-outer>
        <!--pDate v-model:time='setTime' /-->
      </template>
    </v-text-field>
  </v-col>
</template>