<script setup>
import { processDate } from '@/components/methods/display_format'

const props = defineProps({
  subject: {type: Object, required: true}
})

</script>

<template>
  <v-card min-height='175' class='mx-auto mt-3 bg-grey-lighten-3'>
    <template v-slot:title>
      {{ subject.subject_name }}
    </template>
    <v-divider/>
    <v-card-text>
      対象期間：{{ subject.period }}<br>
      作成日時：{{ processDate(subject.created) }}<br>
      作成者：{{ subject.username }}
    </v-card-text>
  </v-card>
</template>