<script setup>
// import
import { ref } from 'vue'

// variable
const props = defineProps({
  create: {type: Boolean, default: false},
  weeks: {type: Object, required: true},
  update_answer: {type: Boolean, default: false}
})
const emit = defineEmits(['move_week', 'move_flow', 'move_preview', 'move_edit', 'move_score'])

const groupBy = ref([{
  title: `回`,
  key: 'week_num',
  order: 'asc'
}])
const s_headers = ref([
  {title: '内容', align: 'start', key: 'week_name', width: '700'},
  {title: '教科書コンテンツ', align: 'center', key: 'week', width: '175'},
  {title: '演習問題', align: 'center', key: 'flow', width: '175'},
])
const t_headers = ref([
  {title: '内容', align: 'start', key: 'week_name', width: '600'},
  {title: 'プレビュー', align: 'center', key: 'preview', width: '175'},
  {title: '編集', align: 'center', key: 'edit', width: '175'},
  {title: '学習状況確認', align: 'center', key: 'score', width: '175'},
])

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
    <div v-if='create'>
      <v-data-table :headers='t_headers' :items='weeks' :group-by='groupBy' hide-default-footer items-per-page='30'>
        <template v-slot:group-header = '{ item, columns, toggleGroup, isGroupOpen }'>
          <tr>
            <td :colspan='columns.length'>
              <v-btn :icon='isGroupOpen(item) ? "$expand" : "$next"' size='small' variant='text' @click='toggleGroup(item)' />
              第{{ item.value }}回
            </td>
          </tr>      
        </template>
        <template v-slot:item.preview="{ item }">
          <v-btn class='bg-primary' @click="move_preview(item.week_id)">プレビュー</v-btn>
        </template>
        <template v-slot:item.edit="{ item }">
          <v-btn :disabled='!update_answer' class='bg-primary' @click="move_edit(item.week_id)">編集</v-btn>
        </template>
        <template v-slot:item.score="{ item }">
          <v-btn class='bg-primary' @click="move_score(item.week_id)">学習状況確認</v-btn>
        </template>
      </v-data-table>
    </div>
    <div v-else>
      <v-data-table :headers='s_headers' :items='weeks' :group-by='groupBy' hide-default-footer items-per-page='30'>
        <template v-slot:group-header = '{ item, columns, toggleGroup, isGroupOpen }'>
          <tr>
            <td :colspan='columns.length'>
              <v-btn :icon='isGroupOpen(item) ? "$expand" : "$next"' size='small' variant='text' @click='toggleGroup(item)' />
              第{{ item.value }}回
            </td>
          </tr>      
        </template>
        <template v-slot:item.week="{ item }">
          <v-btn class='bg-primary' @click="move_week(item.week_id)">学習を始める</v-btn>
        </template>
        <template v-slot:item.flow="{ item }">
          <v-btn class='bg-primary' @click="move_flow(item.week_id)">演習問題</v-btn>
        </template>
      </v-data-table>
    </div>
  </div>
  
  
</template>
