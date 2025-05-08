<script setup>
import axios from 'axios'
import { ref, watch } from 'vue'

import tt_EditWeekInfo from '@/components/templates/teachers/EditWeeks/EditWeekInfo/tt_EditWeekInfo.vue'
import tt_EditWeekImage from '@/components/templates/teachers/EditWeeks/EditWeekInfo/tt_EditWeekImage.vue'
import tt_EditWeekKeyword from '@/components/templates/teachers/EditWeeks/EditWeekInfo/tt_EditWeekKeyword.vue'

const props = defineProps({
  course_id: {type: Number, required: true},
  week_id: {type: Number, required: true},
})
const type = ref('')


</script>

<template>
  <div>
    <h2 class='mx-4'>詳細編集</h2>
    <v-container class='pa-2 justify-center'>
      <v-row>
        <v-col cols='2'>
          <v-tabs 
            v-model='type'
            direction='vertical'
            bg-color='grey-lighten-3'
            slider-color='secondary'
            slider-size='5'
            class='mb-3'
          >
            <v-tab value='info'     class='bg-primary'><h3>コース情報</h3></v-tab>
            <v-tab value='image'    class='bg-primary'><h3>画像</h3></v-tab>
            <v-tab value='keyword'  class='bg-primary'><h3>キーワード</h3></v-tab>
            <v-tab value='material' class='bg-primary'><h3>関連教材</h3></v-tab>
          </v-tabs>
        </v-col>
        <v-col cols='10'>
          <v-tabs-window v-model='type'>
            <v-tabs-window-item value='info'>
              <tt_EditWeekInfo :course_id='course_id' :week_id='week_id'/>
            </v-tabs-window-item>
            <v-tabs-window-item value='image'>
              <tt_EditWeekImage :course_id='course_id' :week_id='week_id'/>
            </v-tabs-window-item>
            <v-tabs-window-item value='keyword'>
              <tt_EditWeekKeyword />
            </v-tabs-window-item>
          </v-tabs-window>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>