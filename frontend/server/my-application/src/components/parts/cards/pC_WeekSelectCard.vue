<script setup>
// import

// variable
const props = defineProps({
  create: {type: Boolean, default: false},
  week: {type: Object, required: true},
  update_answer: {type: Boolean, default: false}
})
const emit = defineEmits(['move_week', 'move_flow', 'move_preview', 'move_edit', 'move_score'])

// function
const move_week = (week_id) => emit('move_week', week_id)
const move_flow = (week_id) => emit('move_flow', week_id)
const move_preview = (week_id) => emit('move_preview', week_id)
const move_edit = (week_id) => emit('move_edit', week_id)
const move_score = (week_id) => emit('move_score', week_id)

// created
</script>

<template>
  <div>
    <v-card min-height='175' class='mx-auto mt-5 bg-grey-lighten-3'>
      <template v-slot:title>
        {{ week.week_name }}
      </template>
      <v-divider/>
      <v-card-text>
        第{{ week.week_num }}回
      </v-card-text>
      
      <div v-if='create'>
        <v-card-actions>
          <v-row class='d-flex flex-row justify-space-between pb-3'>
            <v-col cols='4'>
              <v-btn block depressed text='プレビュー' class='mt-2 mx-3 bg-primary' @click='move_preview(week.week_id)'/>
            </v-col>
            <v-col cols='4'>
              <v-btn :disabled='!update_answer' block depressed text='編集' class='mt-2 bg-primary' @click='move_edit(week.week_id)'/>
            </v-col>
            <v-col cols='4'>
              <v-btn block depressed text='学習状況確認' class='mt-2 mx-n3 bg-primary' @click='move_score(week.week_id)'/>
            </v-col>
          </v-row>
        </v-card-actions>
      </div>
      <div v-else>
        <v-card-actions>
          <v-row class='d-flex flex-row justify-space-between mx-3 pb-3'>
            <v-col cols='6'>
              <v-btn block depressed text='学習を始める' class='mt-2 bg-primary' @click='move_week(week.week_id)'/>
            </v-col>
            <v-col cols='6'>
              <v-btn block depressed text='演習問題' class='mt-2 bg-primary' @click='move_flow(week.week_id)'/>
            </v-col>
          </v-row>
        </v-card-actions>
      </div>
    </v-card>
  </div>
</template>