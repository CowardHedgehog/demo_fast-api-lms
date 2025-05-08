<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import tc_UserInfo from '@/components/templates/common/tc_UserInfo.vue'
import tc_SessionError from '@/components/templates/common/tc_SessionError.vue'
import { markdownToHtml } from '@/components/methods/markdown.js'
import { processDate } from '@/components/methods/display_format'
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'

dayjs.extend(utc)
dayjs.extend(timezone)
dayjs.tz.setDefault('Asia/Tokyo')

// propsの定義を追加
const props = defineProps({
  user_info: {
    type: Object,
    required: true
  }
})

// variable
const router = useRouter()
const session_error = ref(false)
const notifications = ref([])
const dialog = ref(false)
const selectedNotification = ref(null)

// function
const get_notifications = () => {
  axios.get('http://localhost:8000/announcements_list', {withCredentials: true}).then(function(response){
    const currentTime = dayjs.tz()
    
    // is_activeがtrueで、かつ現在時刻が開始日時と終了日時の間にあるお知らせのみをフィルタリング
    notifications.value = response.data.filter(notification => {
      const startTime = dayjs.tz(notification.start_date_time)
      const endTime = dayjs.tz(notification.end_date_time)
      return notification.is_active && currentTime.isAfter(startTime) && currentTime.isBefore(endTime)
    })
    
    console.log('Filtered notifications:', notifications.value)
  }).catch(function(error){
    console.error('Error loading notifications:', error)
  })
}

const showNotification = async (notification) => {
  selectedNotification.value = notification
  dialog.value = true
  
  if (!notification.is_read) {
    try {
      await axios.post(
        `http://localhost:8000/announcements/${notification.id}/read`,
        {},
        { withCredentials: true }
      )
      console.log(`お知らせID: ${notification.id}を既読にしました`)
      
      notification.is_read = true
      
      await get_notifications()
      
    } catch (error) {
      console.error('既読処理に失敗しました:', error)
    }
  }
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('ja-JP', {
    month: '2-digit',
    day: '2-digit',
    weekday: 'short'
  })
}

// created
get_notifications()
</script>

<template>
  <v-responsive>
    <v-container class="notification-container px-0">
      <v-card class="notification-card">
        <v-card-title class="text-h5 bg-grey-lighten-3 py-3">
          お知らせ
        </v-card-title>
        <v-card-text class="notification-list-container">
          <v-list>
            <v-list-item
              v-for="notification in notifications"
              :key="notification.id"
              @click="showNotification(notification)"
              class="notification-item"
            >
              <v-row align="center" no-gutters>
                <v-col cols="2" class="text-caption text-grey-darken-1">
                  {{ formatDate(notification.send_date_time) }}
                </v-col>
                <v-col cols="8">
                  {{ notification.title }}
                </v-col>
                <v-col cols="2" class="text-caption text-grey-darken-1">
                  {{ notification.sender }}
                </v-col>
              </v-row>
            </v-list-item>
          </v-list>
        </v-card-text>
      </v-card>

      <!-- モーダルダイアログ -->
      <v-dialog v-model="dialog" max-width="600">
        <v-card v-if="selectedNotification">
          <v-card-title class="text-h6 bg-grey-lighten-3 d-flex justify-space-between align-center pa-4">
            メッセージ 確認
            <v-btn icon="mdi-close" size="small" @click="dialog = false"></v-btn>
          </v-card-title>
          <v-card-text class="pa-4">
            <v-container>
              <v-row no-gutters class="mb-2">
                <v-col cols="2" class="text-subtitle-2 text-grey-darken-1">表示期間</v-col>
                <v-col cols="9">
                  {{ processDate(selectedNotification.start_date_time) }} ～ {{ processDate(selectedNotification.end_date_time) }}
                </v-col>
              </v-row>

              <v-row no-gutters class="mb-2">
                <v-col cols="2" class="text-subtitle-2 text-grey-darken-1">タイトル</v-col>
                <v-col cols="9">{{ selectedNotification.title }}</v-col>
              </v-row>

              <v-row no-gutters class="mb-2">
                <v-col cols="2" class="text-subtitle-2 text-grey-darken-1">本文</v-col>
                <v-col cols="9">
                  <div v-html="markdownToHtml(selectedNotification.content)" class="notification-content"></div>
                </v-col>
              </v-row>

              <v-row no-gutters class="mb-2">
                <v-col cols="2" class="text-subtitle-2 text-grey-darken-1">発信者</v-col>
                <v-col cols="9">{{ selectedNotification.sender }}</v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions class="pa-4">
            <v-spacer></v-spacer>
            <v-btn color="grey" variant="text" @click="dialog = false">閉じる</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

    </v-container>
  </v-responsive>
  <tc_SessionError v-if='session_error'/>
</template>

<style scoped>
.notification-container {
  max-width: 100%;
}
.notification-item {
  border-bottom: 1px solid #e0e0e0;
  cursor: pointer;
  padding: 8px 16px;
}

.notification-item:hover {
  background-color: #f5f5f5;
}

.v-row {
  width: 100%;
}

:deep(.v-list-item__content) {
  padding: 8px 0;
}

.notification-content {
  line-height: 1.4;
  white-space: pre-wrap;
  margin-top: 4px;
}

:deep(.v-list-item) {
  padding: 12px 0;
}

:deep(.v-list-item-title) {
  margin-bottom: 4px;
  font-weight: 500;
}

:deep(.v-list-item-subtitle) {
  color: rgba(0, 0, 0, 0.87) !important;
}

.notification-card {
  width: 100%;
  max-width: 100%;
  max-height: 500px;
  display: flex;
  flex-direction: column;
}

.notification-list-container {
  overflow-y: auto;
  max-height: calc(60px * 5); /* 5つ分のお知らせの高さ */
  padding: 0;
}

.v-dialog {
  margin: 0;
}
</style>
