<script setup>
import tt_EditFlowPage from './EditFlowContent/tt_EditFlowPage.vue';

const props = defineProps({
    course_id: {type: Number, required: true},
    week_id: {type: Number, required: true},
})
</script>

<template>
    <div>
        <h2 class='mx-4'>演習問題編集</h2>
        <v-container class='pa-2 justify-center'>
            <tt_EditFlowPage :course_id='course_id' :week_id='week_id' />
        </v-container>
    </div>
</template>