<script setup>
import axios from 'axios'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import tc_Header from '@/components/templates/common/tc_Header.vue'
import tc_UserInfo from '@/components/templates/common/tc_UserInfo.vue'
import tc_SessionError from '@/components/templates/common/tc_SessionError.vue'
import { markdownToHtml } from '@/components/methods/markdown.js'
import { processDate } from '@/components/methods/display_format'

// variable
const router = useRouter()
const session_error = ref(false)
const user_info = ref({})
const notifications = ref([])
const dialog = ref(false)
const emit = defineEmits(["update:dialog"])
const editDialog = ref(false)
const successDialog = ref(false)
const selectedNotification = ref({
  id: null,
  title: '',
  content: '',
  start_date_time: '',
  end_date_time: '',
  user_kind_id: null,
  sender: ''
})
const deleteDialog = ref(false)
const itemToDelete = ref(null)
const detailDialog = ref(false)
const selectedDetailNotification = ref(null)

const userKindOptions = [
  { text: '学生', value: 3 },
  { text: '教師', value: 2 }
]

// 新規作成・編集用の変数
const newNotification = ref({
  title: '',
  content: '',
  start_date_time: '',
  end_date_time: '',
  sender: '',
  user_kind_id: null
})

const formData = computed({
  get: () => {
    return selectedNotification.value || newNotification.value
  },
  set: (value) => {
    if (selectedNotification.value) {
      selectedNotification.value = value
    } else {
      newNotification.value = value
    }
  }
})

// function
const get_user_info = () => {
  axios.get('http://localhost:8000/home_profile', {withCredentials: true})
    .then(response => {
      user_info.value = response.data
    })
    .catch(error => {
      if(error.response?.status == 401) {
        session_error.value = true
      }
    })
}

const get_notifications = () => {
  axios.get('http://localhost:8000/announcements_list_all', {withCredentials: true})
    .then(response => {
      notifications.value = response.data
      console.log('All notifications loaded:', notifications.value)
    })
    .catch(error => {
      console.error('Error loading notifications:', error)
    })
}

const createNotification = async () => {
  try {
    const notificationData = {
      title: newNotification.value.title,
      content: newNotification.value.content,
      start_date_time: newNotification.value.start_date_time,
      end_date_time: newNotification.value.end_date_time,
      sender: newNotification.value.sender,
      user_kind_id: newNotification.value.user_kind_id,
      is_active: true
    }
    
    await axios.post('http://localhost:8000/announcements', 
      notificationData,
      { 
        headers: {'Content-Type': 'application/json'},
        withCredentials: true 
      }
    )
    
    // モーダルを閉じる
    dialog.value = false
    
    // フォームをリセット
    newNotification.value = {
      title: '',
      content: '',
      start_date_time: '',
      end_date_time: '',
      sender: '',
      user_kind_id: null
    }
    
    // お知らせ一覧を再取得
    get_notifications()
    
  } catch (error) {
    console.error('Error creating notification:', error)
  }
}

const updateNotification = async () => {
  try {
    const config = {
      headers: { 'Content-Type': 'application/json' },
      withCredentials: true
    }
    
    const response = await axios.put(
      `http://localhost:8000/announcements/${selectedNotification.value.id}`, 
      {
        title: selectedNotification.value.title,
        content: selectedNotification.value.content,
        start_date_time: selectedNotification.value.start_date_time,
        end_date_time: selectedNotification.value.end_date_time,
        user_kind_id: selectedNotification.value.user_kind_id
      },
      config
    )

    if (response.data.success) {
      successDialog.value = true
      setTimeout(() => {
        successDialog.value = false
        editDialog.value = false
        get_notifications()
      }, 1000)
    }
  } catch (error) {
    console.error('Error:', error)
  }
}

const deleteNotification = async (notification) => {
  if (confirm('このお知らせを削除してもよろしいですか？')) {
    try {
      await axios.delete(
        `http://localhost:8000/announcements/${notification.id}`,
        { withCredentials: true }
      )
      await get_notifications()
    } catch (error) {
      console.error('お知らせの削除に失敗しました:', error)
    }
  }
}

const editNotification = (notification) => {
  selectedNotification.value = { ...notification }
  editDialog.value = true
}

const resetForm = () => {
  newNotification.value = {
    title: '',
    content: '',
    start_date_time: '',
    end_date_time: '',
    sender: user_info.value.username || '',
    user_kind_id: null
  }
}

const deleteItem = (item) => {
  itemToDelete.value = item
  deleteDialog.value = true
}

const confirmDelete = async () => {
  try {
    await axios.delete(`http://localhost:8000/announcements/${itemToDelete.value.id}`, {
      withCredentials: true
    })
    deleteDialog.value = false
    get_notifications()
  } catch (error) {
    console.error('Error deleting announcement:', error)
  }
}

const showNotificationDetail = (item) => {
  selectedDetailNotification.value = item
  detailDialog.value = true
}

// created
get_user_info()
get_notifications()

// 新しい日付フォーマット関数
const formatCustomDate = (date) => {
  if (date == null) return '未設定'
  const datetime = new Date(date)
  const year = datetime.getFullYear()
  const month = ('00' + (datetime.getMonth()+1)).slice(-2)
  const day = ('00' + datetime.getDate()).slice(-2)
  const hour = ('00' + datetime.getHours()).slice(-2)
  const minute = ('00' + datetime.getMinutes()).slice(-2)
  return year + '/' + month + '/' + day + ' ' + hour + ':' + minute
}

// ユーザー種別の表示用関数を追加
const formatUserKind = (kind_id) => {
  switch (kind_id) {
    case 2:
      return '教師'
    case 3:
      return '学生'
    default:
      return '未設定'
  }
}

// ヘッダー定義を更新
const headers = ref([
  { title: 'タイトル', align: 'start', key: 'title' },
  { title: '開始日時', align: 'start', key: 'start_date_time',
    value: item => formatCustomDate(item.start_date_time) },
  { title: '終了日時', align: 'start', key: 'end_date_time',
    value: item => formatCustomDate(item.end_date_time) },
  { title: '送信日時', align: 'start', key: 'send_date_time',
    value: item => formatCustomDate(item.send_date_time) },
  { title: '対象', align: 'start', key: 'user_kind_id',
    value: item => formatUserKind(item.user_kind_id) },
  { title: '操作', align: 'end', key: 'actions', sortable: false }
])

// editItem関数を追加
const editItem = (item) => {
  console.log('Edit item clicked:', item)
  selectedNotification.value = { ...item }
  editDialog.value = true
}

</script>

<template>
  <v-app>
    <tc_Header />
    <v-main>
      <v-container>
        <h2>お知らせ管理</h2>
        <v-row class="d-flex justify-end mb-4">
          <v-btn color="primary" @click="dialog = true">
            新規作成
          </v-btn>
        </v-row>

        <v-data-table :headers="headers" :items="notifications">
          <template v-slot:item.title="{ item }">
            <span 
              @click="showNotificationDetail(item)"
              style="cursor: pointer; color: blue; text-decoration: underline;"
            >
              {{ item.title }}
            </span>
          </template>
          <template v-slot:item.start_date_time="{ item }">
            {{ formatCustomDate(item.start_date_time) }}
          </template>
          <template v-slot:item.end_date_time="{ item }">
            {{ formatCustomDate(item.end_date_time) }}
          </template>
          <template v-slot:item.send_date_time="{ item }">
            {{ formatCustomDate(item.send_date_time) }}
          </template>
          <template v-slot:item.user_kind_id="{ item }">
            {{ formatUserKind(item.user_kind_id) }}
          </template>
          <template v-slot:item.actions="{ item }">
            <v-icon size="small" class="me-2" @click="editItem(item)">
              mdi-pencil
            </v-icon>
            <v-icon size="small" @click="deleteItem(item)">
              mdi-delete
            </v-icon>
          </template>
        </v-data-table>

        <!-- 新規作成用ダイアログ -->
        <v-dialog v-model="dialog" max-width="800px">
          <v-card>
            <v-card-title>新規お知らせの作成</v-card-title>
            <v-card-text>
              <v-form @submit.prevent>
                <v-text-field
                  v-model="newNotification.title"
                  label="タイトル"
                  required
                ></v-text-field>
                <v-textarea
                  v-model="newNotification.content"
                  label="本文"
                  required
                ></v-textarea>
                <v-text-field
                  v-model="newNotification.start_date_time"
                  label="開始日時"
                  type="datetime-local"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="newNotification.end_date_time"
                  label="終了日時"
                  type="datetime-local"
                  required
                ></v-text-field>
                <v-select
                  v-model="newNotification.user_kind_id"
                  :items="userKindOptions"
                  item-title="text"
                  item-value="value"
                  label="対象ユーザー"
                  required
                ></v-select>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue-darken-1" variant="text" @click="setDialog = false">キャンセル</v-btn>
              <v-btn color="blue-darken-1" variant="text" @click="createNotification">作成</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- 編集用ダイアログ -->
        <v-dialog v-model="editDialog" max-width="800px" persistent>
          <v-card>
            <v-card-title>お知らせの編集</v-card-title>
            <v-card-text>
              <v-form @submit.prevent>
                <v-text-field
                  v-model="selectedNotification.title"
                  label="タイトル"
                  required
                ></v-text-field>
                <v-textarea
                  v-model="selectedNotification.content"
                  label="本文"
                  required
                ></v-textarea>
                <v-text-field
                  v-model="selectedNotification.start_date_time"
                  label="開始日時"
                  type="datetime-local"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="selectedNotification.end_date_time"
                  label="終了日時"
                  type="datetime-local"
                  required
                ></v-text-field>
                <v-select
                  v-model="selectedNotification.user_kind_id"
                  :items="userKindOptions"
                  item-title="text"
                  item-value="value"
                  label="対象ユーザー"
                  required
                ></v-select>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue-darken-1" variant="text" @click="editDialog = false">キャンセル</v-btn>
              <v-btn color="blue-darken-1" variant="text" @click="updateNotification">更新</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- 削除確認イアログ -->
        <v-dialog v-model="deleteDialog" max-width="400px">
          <v-card>
            <v-card-title>削除の確認</v-card-title>
            <v-card-text>
              このお知らせを削除してもよろしいですか？
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="grey" @click="deleteDialog = false">キャンセル</v-btn>
              <v-btn color="error" @click="confirmDelete">削除</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- 成功メッセージダイアログ -->
        <v-dialog v-model="successDialog" transition="dialog-top-transition" persistent>
          <v-row class="d-flex align-start justify-center">
            <v-sheet class="rounded-lg">
              <v-sheet class="my-5 mx-15">
                <h3 class="d-flex justify-center align-end">更新しました</h3>
              </v-sheet>
            </v-sheet>
          </v-row>
        </v-dialog>

        <!-- お知らせ詳細表示用モーダル -->
        <v-dialog v-model="detailDialog" max-width="600px">
          <v-card v-if="selectedDetailNotification">
            <v-card-title class="text-h6 bg-grey-lighten-3 d-flex justify-space-between align-center pa-4">
              お知らせ詳細
              <v-btn icon="mdi-close" size="small" @click="detailDialog = false"></v-btn>
            </v-card-title>
            <v-card-text class="pa-4">
              <v-container>
                <v-row no-gutters class="mb-2">
                  <v-col cols="2" class="text-subtitle-2 text-grey-darken-1">表示期間</v-col>
                  <v-col cols="10">
                    {{ formatCustomDate(selectedDetailNotification.start_date_time) }} ～ 
                    {{ formatCustomDate(selectedDetailNotification.end_date_time) }}
                  </v-col>
                </v-row>

                <v-row no-gutters class="mb-2">
                  <v-col cols="2" class="text-subtitle-2 text-grey-darken-1">タイトル</v-col>
                  <v-col cols="10">{{ selectedDetailNotification.title }}</v-col>
                </v-row>

                <v-row no-gutters class="mb-2">
                  <v-col cols="2" class="text-subtitle-2 text-grey-darken-1">本文</v-col>
                  <v-col cols="10">
                    <div v-html="markdownToHtml(selectedDetailNotification.content)" class="notification-content"></div>
                  </v-col>
                </v-row>

                <v-row no-gutters class="mb-2">
                  <v-col cols="2" class="text-subtitle-2 text-grey-darken-1">発信者</v-col>
                  <v-col cols="10">{{ selectedDetailNotification.sender }}</v-col>
                </v-row>

                <v-row no-gutters class="mb-2">
                  <v-col cols="2" class="text-subtitle-2 text-grey-darken-1">対象</v-col>
                  <v-col cols="10">{{ formatUserKind(selectedDetailNotification.user_kind_id) }}</v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn color="grey" variant="text" @click="detailDialog = false">閉じる</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-container>
    </v-main>
  </v-app>
</template>

<style scoped>
.notification-item {
  border-bottom: 1px solid #e0e0e0;
  padding: 8px 16px;
}

.notification-card {
  max-height: 500px;
  display: flex;
  flex-direction: column;
}

.notification-list-container {
  overflow-y: auto;
  max-height: calc(60px * 5);
  padding: 0;
}

.v-dialog {
  margin: 0;
}

.notification-content {
  line-height: 1.4;
  white-space: pre-wrap;
  margin-top: 4px;
}
</style>
