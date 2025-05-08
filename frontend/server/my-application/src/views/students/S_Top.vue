<script setup>
import axios from 'axios'
import { ref, onMounted, onUnmounted,computed } from 'vue'
import { useRouter } from 'vue-router'
import ts_Header from '@/components/templates/students/ts_Header.vue'
import ts_SelectHome from '@/components/templates/students/ts_SelectHome.vue'
import tc_SessionError from '@/components/templates/common/tc_SessionError.vue'
import pC_CourseSelect from '@/components/parts/cards/pC_CourseSelect.vue'
import pC_Announcements from '@/components/parts/cards/pC_Announcements.vue'
import tc_SetNickname from '@/components/templates/common/tc_SetNickname.vue'
import tc_UpdatePassword from '@/components/templates/common/tc_UpdatePassword.vue'
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale,PointElement,LineElement,plugins, scales, Ticks } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale,PointElement,LineElement)

const session_error = ref(false)
const user_info = ref({})
const completedGoals = ref([])
const router = useRouter()
const props = defineProps({
  create: {type: Boolean, default: false},
  course_id : {
    type: Number,
    required: true
  }
})
const course_id = ref([])
const courses = ref([])
const gmenu = ref(false)
const name = ref()
const nickname = ref()
const login = ref()
const progresses = ref([])
const progress = ref(0)
const high_pointer = ref([])
const rank_menu = ref(false)

const pointlist = ref([
  {content: "ログインをする", point:'1'},
  {content: "目標を設定する", point: '3'},
  {content: "演習問題を解く", point:'10'},
  {content: "累計10日間ログインする", point:'10'}
])
const points = ref(0)
const pmenu = ref(false)

const newGoal = ref({
  details: '', 
});
const goals = ref([]);
const notgoal = ref([]);
const dialog = ref(false);

const welcome_dialog = ref(true)
const current_step = ref(0)
const nicknameUpdated = ref(false)
const passwordUpdated = ref(false)

const handleNicknameUpdate = (nickname) => {
  nicknameUpdated.value = true;
  name.value = nickname;
  current_step.value++;
}

const handlePasswordUpdate = () => {
  passwordUpdated.value = true;
  current_step.value++;
}

const steps = [
  {
    title: 'ようこそ',
    description: 'このアプリケーションでは、技術者のための数理などの数理系科目の学習を行えます。',
    icon: 'mdi-school'
  },
  {
    title: 'ニックネーム設定',
    description: '他のユーザーに表示される名前を設定します。',
    icon: 'mdi-account'
  },
  {
    title: 'パスワード設定',
    description: 'セキュリティのため、初回ログイン時にパスワードの変更をお願いします。',
    icon: 'mdi-lock'
  },
  {
    title: 'ポイントシステム',
    description: '学習を進めることでポイントが獲得でき、ランキングで他のユーザーと競うことができます。',
    icon: 'mdi-star'
  },
  {
    title: '目標設定',
    description: '自分の目標を設定し、達成状況を管理できます。',
    icon: 'mdi-flag'
  },
  {
    title: '学習を始める',
    description: '科目選択から自分の学習したい科目を選択して、始めよう!',
    icon: 'mdi-school'
  }
]

const get_courses = () => {
  axios.get('http://localhost:8000/get_courses', {withCredentials: true}).then(function(response){
    courses.value = response.data
  })
}
const move_course = (course_id) => router.push({name: 'S_Course', params: {course_id: course_id}})
const move_score = (course_id) => router.push({name: 'S_CourseScore', params: {course_id: course_id}})
const move_syllabus_info = (course_id) => router.push({name: 'S_SyllabusInfo', params: {course_id: course_id}})

const addGoal = () => {
  notgoal.value.push({ ...newGoal.value, completed: false });
  console.log('Goals:', goals.value);

  const params = {
    details: newGoal.value.details,
  };

  const config = {headers: { 'Content-Type': 'application/json' },withCredentials: true};
  axios.post('http://localhost:8000/add_goal', params, config)
    .then(response => {
      console.log('Response:', response.data);
    })
    .catch(error => {
      if (error.response) {
        console.error('Error:', error.response.data);
      } else {
        console.error('Error:', error.message);
      }
    });

  resetNewGoal();
  dialog.value = false;
};

const resetNewGoal = () => {
  newGoal.value = { details: '' };
};

const toggleCompletion = (index) => {
  const goal = notgoal.value[index];
  goal.completed = !goal.completed;
  const params = {
    goal_id: goal.goal_id,
    completed : goal.completed
  };
  const config = {headers: { 'Content-Type': 'application/json' },withCredentials: true};
  axios.post('http://localhost:8000/toggle_completed', params,config,)
};

const deletegoal = (index) => {
  const goal = notgoal.value[index];
  const params = {goal_id : goal.goal_id}
  const config = {headers: { 'Content-Type': 'application/json' },withCredentials: true};
  axios.delete('http://localhost:8000/delete_goal', { data: params, ...config })
  notgoal.value.splice(index, 1)
}

const goaltoggleCompletion = (index) => {
  const goal = completedGoals.value[index];
  goal.completed = !goal.completed;
  const params = {
    goal_id: goal.goal_id,
    completed : goal.completed
  };
  const config = {headers: { 'Content-Type': 'application/json' },withCredentials: true};
  axios.post('http://localhost:8000/toggle_completed', params,config,)
};

const fetch_goal = () =>{
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  try{
    axios.get('http://localhost:8000/get_goal',config, { withCredentials: true }).then(response => {
      goals.value = response.data
    })
  }catch (error) {
    console.error('Failed to fetch goals:', error.response?.data || error.message);
  }
}

const fetch_not_goal = () =>{
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  axios.get('http://localhost:8000/get_not_goal',config, { withCredentials: true }).then(response => {
    notgoal.value = response.data
  })
}
const openpoint = () =>{
  pmenu.value = true
}
const openrank = () =>{
  rank_menu.value = true
}

const fetch_point = () => {
  const config = {headers: { 'Content-Type': 'application/json' },withCredentials: true};
  axios.get('http://localhost:8000/get_point', config, { withCredentials: true }).then(response => {
    points.value = response.data
  })
}
let intervalId = null;

const startPolling = () => {
  intervalId = setInterval(() => {
    fetch_point();
  }, 5000);
};

const stopPolling = () => {
  if (intervalId) {
    clearInterval(intervalId);
    intervalId = null;
  }
};

const fetch_high_pointer = () =>{
  const config = {headers: { 'Content-Type': 'application/json' },withCredentials: true};
  axios.get('http://localhost:8000/get_high_pointer', config, { withCredentials: true }).then(response => {
    high_pointer.value = response.data;
    console.log(high_pointer.value)
  })
}

const opengoals = () => {
  completedGoals.value = [];
  for (let goal of goals.value) {
    if (goal.completed) {
      completedGoals.value.push(goal);
    }
  }
  gmenu.value = true;
};

const fetch_user_name = () => {
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  axios.get('http://localhost:8000/user_name', config, { withCredentials: true }).then(response => {
  name.value =  response.data
  })
}

const fetch_login_day = () => {
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  axios.post('http://localhost:8000/login_num',config, { withCredentials: true })
    .then(response => {
      login.value = response.data
    })
    .catch(error => {
      console.error('ログイン日数の取得に失敗しました:', error)
      if (error.response?.status === 401) {
        console.error('認証エラー')
        session_error.value = true
      } else if (error.response?.status === 500) {
        console.error('サーバーエラー')
      } else {
        console.error('予期せぬエラー', error.message)
      }
    })
}

const fetch_progress = () => {
  axios.get('http://localhost:8000/get_courses', { withCredentials: true }).then(response => {
    course_id.value =  response.data.map(course => course.course_id);
    const progressPromises = course_id.value.map(course_id => 
      axios.get(`http://localhost:8000/get_progress/${course_id}`, { withCredentials: true })
    );
    Promise.all(progressPromises)
      .then(responses => {
        const total = ref(0.0)
        const index = ref(0.0)
        progresses.value = responses.map(response => response.data);
        if (progresses.value.length > 0) {
          progresses.value.forEach(score=>{
            total.value += score
            index.value += 1;
          })
          progress.value = parseFloat(((total.value / index.value)).toFixed(2)); 
        } else {
          progress.value = 0;
        }
      })
      .catch(error => {
        console.error('進捗の取得に失敗しました:', error);
      });
  })
}

const chartdata = computed(() => ({
  labels:high_pointer.value.slice(0,10).map((user) => user.mail),
  datasets: [
  {
    label:'ポイント',
    data: high_pointer.value.slice(0,10).map((user) => user.point),
    backgroundColor: high_pointer.value.slice(0,10).map((_, index) => {
      switch (index) {
        case 0:
          return "#D0A900"; // 1位（金色）
        case 1:
          return "#C0C0C0"; // 2位（銀色）
        case 2:
          return "#CD7F32"; // 3位（銅色）
        default:
          return "#6495ED";
      }}),
    borderRadius: 5,
    borderWidth: 2
  }
  ]
}));

const chartOptions = {
    responsive: true,
  indexAxis: "y",
    scales: {
    x: { 
      beginAtZero: true,
      grid: {
        color: 'rgba(0, 0, 0, 0.1)' 
      }
    },
    y: { 
      beginAtZero: true,
      ticks: {
        font: {
          weight: 'bold'
        }
      }
    }
    },
    plugins: {
      legend: { display: false },
      tooltip: {
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      titleColor: '#333',
      titleFont: { weight: 'bold' },
      bodyColor: '#666',
      borderColor: '#ddd',
      borderWidth: 1,
      padding: 10,
      displayColors: false,
        callbacks: {
          label: function (tooltipItem) {
            const sortedUsers = [...high_pointer.value].sort((a, b) => b.point - a.point);
            const user = sortedUsers[tooltipItem.dataIndex];
          let rank = tooltipItem.dataIndex + 1;
          return `${rank}位: ${user.mail}\nポイント: ${user.point}pt`;
        }
      }
    }
  }
}

const showWelcomeDialog = computed(() => {
  const config = {headers: { 'Content-Type': 'application/json' },withCredentials: true};
  axios.get('http://localhost:8000/get_nickname',config,{ withCredentials: true }).then(response =>
    nickname.value = response.data
  )
  if(nickname.value === "" && welcome_dialog.value){
    console.log(true)
    return true
  }
  else{
    console.log(false)
    return false
  }
})

const arrangedRanking = () => {
  const rowSize = 10;
  const maxColumns = 3;
  let columns = Array.from({ length: maxColumns }, () => []);

  let rank = 1;
  let previousPoint = null;

  const rankedUsers = high_pointer.value.map((user, index) => {
    if (previousPoint !== null && user.point !== previousPoint) {
      rank = index + 1;
    }
    previousPoint = user.point;
    return { ...user, rank };
    });

  rankedUsers.forEach((user, index) => {
    const colIndex = Math.floor(index / rowSize);
    if (colIndex < maxColumns) {
      columns[colIndex].push(user);
    }
  });

  return columns;
};

const home_profile = () => {
  axios.get('http://localhost:8000/home_profile', { withCredentials: true }).then(response => {
    user_info.value = response.data
  }).catch(error => {
    if (error.response?.status === 401) {
      session_error.value = true
    } else {
      console.log(error.response)
    }
  })
}

const fetch_data = () =>{
  fetch_goal()
  get_courses()
  fetch_user_name()
  fetch_login_day()
  fetch_not_goal()
  fetch_progress()
  fetch_point()
  fetch_high_pointer()
}

onMounted(() => {
  startPolling();
});

onUnmounted(() => {
  stopPolling();
});
fetch_data()
home_profile()
</script>

<template>
  <div>
    <v-dialog v-model="showWelcomeDialog" persistent width="800">
      <v-card class="welcome-card">
        <v-card-title class="welcome-title text-center pa-4">
          <h2>学習管理システムへようこそ</h2>
        </v-card-title>
        <v-stepper v-model="current_step" class="welcome-stepper">
          <v-stepper-header>
            <template v-for="(step, index) in steps" :key="index">
              <v-stepper-item
                :value="index"
                :complete="current_step > index || (index === 1 && nicknameUpdated) || (index === 2 && passwordUpdated)"
              >
                <v-icon>{{ step.icon }}</v-icon>
              </v-stepper-item>
              <v-divider
                v-if="index < steps.length - 1"
                :key="'divider-' + index"
              ></v-divider>
            </template>
          </v-stepper-header>

          <v-stepper-window>
            <v-stepper-window-item
              v-for="(step, index) in steps"
              :key="index"
              :value="index"
            >
              <v-card-text class="text-center pa-6" style="max-height: 400px; overflow-y: auto;">
                <template v-if="index === 1">
                  <tc_SetNickname @nickname-updated="handleNicknameUpdate" />
                </template>
                <template v-else-if="index === 2">
                  <tc_UpdatePassword :user_info="user_info" @password-updated="handlePasswordUpdate" />
                </template>
                <template v-else>
                  <v-icon size="64" color="primary" class="mb-4">{{ step.icon }}</v-icon>
                  <h3 class="text-h5 mb-4">{{ step.title }}</h3>
                  <p class="text-body-1">{{ step.description }}</p>
                </template>
              </v-card-text>
            </v-stepper-window-item>
          </v-stepper-window>
        </v-stepper>

        <v-card-actions class="welcome-actions pa-4">
          <v-spacer></v-spacer>
          <v-btn
            v-if="current_step > 0"
            color="grey"
            variant="text"
            @click="current_step--"
          >
            戻る
          </v-btn>
          <v-btn
            color="primary"
            @click="current_step < steps.length - 1 ? current_step++ : (welcome_dialog = false, current_step = 0)"
            :disabled="(current_step === 1 && !nicknameUpdated) || (current_step === 2 && !passwordUpdated)"
          >
            {{ current_step < steps.length - 1 ? '次へ' : '始める' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <ts_Header :user_info="user_info" />
    <v-main>
      <v-container>
        <v-responsive :max-width="1200" class="mx-auto">
          <v-container>
            <ts_SelectHome location="test2" />
            <v-row>
              <v-container class="pt-5">
                <div class="icon-container">
                  <div class="icon-item">
                    <div class="icon2">
                      <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path d="M12,2A10,10 0 1,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 1,1 4,12A8,8 0 0,1 12,4M12,6A6,6 0 1,0 18,12A6,6,0 0,0 12,6Z" />
                      </svg>
                      <p class="name">{{ nickname }}</p>
                      <div class="points-display">
                        <v-icon class="coin-icon">mdi-star-four-points</v-icon>
                        <span class="points">{{ points }}points</span>
                        <v-tooltip location="top">
                          <template v-slot:activator="{ props }">
                            <v-btn v-bind="props" @click="openpoint" class="p-list-btn" icon>
                              <v-icon class="p-list-icon">mdi-list-box-outline</v-icon>
                            </v-btn>
                          </template>
                          ポイントリスト
                        </v-tooltip>
                        <v-tooltip location="top">
                          <template v-slot:activator="{ props }">
                            <v-btn v-bind="props" @click="openrank" class="r-list-btn" icon>
                              <v-icon class="p-list-icon">mdi-crown</v-icon>
                            </v-btn>
                          </template>
                          ポイントランキング
                        </v-tooltip>

                        <v-dialog class = "g-dialog" v-model = 'pmenu'max-width="600">
                        <v-card class = "g-card">
                          <v-card-title class = "g-card-title"><h3><b>ポイントリスト</b></h3></v-card-title>
                          <v-card-text>
                            <v-list>
                              <v-list-item v-for="(content, index) in pointlist" :key="index" class="p-list-item">
                                <div style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
                                  <div style="flex: 0 0 50px; text-align: center;">
                                    <v-icon color="primary" style="font-size: 24px;">mdi-clipboard-check-outline</v-icon>
                                  </div>
                                  <div style="flex: 1; text-align: center; display: flex; justify-content: center; align-items: center;">
                                    <b style="font-size: 17px; line-height: 1;">{{ content.content }}</b>
                                  </div>
                                  <div style="flex: 0 0 100px; text-align: center; position: relative;">
                                    <v-badge 
                                      :content="`${content.point} pt`" 
                                      color="primary" 
                                      overlap 
                                      style="position: relative; top: 5px;"
                                    >
                                      <v-icon color="secondary" style="font-size: 20px;">mdi-star-four-points</v-icon>
                                    </v-badge>
                                  </div>
                                </div>
                              </v-list-item>
                            </v-list>
                          </v-card-text>
                          <v-card-actions>
                            <v-btn class ="g-btn" text color="primary" @click="pmenu = false">閉じる</v-btn>
                          </v-card-actions>
                        </v-card>
                      </v-dialog>

                        <v-dialog v-model ='rank_menu'  max-width="1600px" max-height="900px">
                          <v-card class="rank-card">
                            <v-card-title class="rank-card-title">
                              <v-icon color="amber" size="32" class="mr-2">mdi-crown</v-icon>
                              ポイントランキング
                            </v-card-title>
                            <v-divider></v-divider>
                            <v-card-text class="rank-card-content">
                              <v-container>
                                <v-row>
                                  <v-col cols="6">
                                    <div class="chart-container">
                                      <h3 class="chart-title">
                                        <v-icon color="primary" class="mr-2">mdi-chart-bar</v-icon>
                                        Top10 ポイントリスト
                                      </h3>
                                    <Bar 
                                      v-if="high_pointer.length" 
                                      :data="chartdata" 
                                      :options="chartOptions" 
                                        class="rank-chart"
                                      />
                                      <div class="user_point">
                                        <v-icon color="primary" size="24" class="mr-2">mdi-account-star</v-icon>
                                        <h2>{{ nickname }}のポイントは{{ points }}pt</h2>
                                      </div>
                                    </div>
                                  </v-col>

                                  <v-col cols="6">
                                    <v-container class="rank-list-container">
                                      <h3 class="chart-title">
                                        <v-icon color="primary" class="mr-2">mdi-format-list-numbered</v-icon>
                                        ランキングリスト
                                      </h3>
                                      <v-row no-gutters class="rank-columns">
                                        <v-col v-for="(column, colIndex) in arrangedRanking()" :key="colIndex" cols="4">
                                          <v-container class="column-container">
                                            <v-row no-gutters>
                                              <v-col v-for="(user, rowIndex) in column" :key="rowIndex" cols="12">
                                                <v-card :class="['rank-item', {'rank-item-top': user.rank <= 3}]">
                                                  <v-avatar size="24" class="mr-2">
                                                    <v-icon v-if="user.rank === 1" color="amber darken-2" size="20">mdi-crown</v-icon>
                                                    <v-icon v-else-if="user.rank === 2" color="grey lighten-1" size="20">mdi-crown</v-icon>
                                                    <v-icon v-else-if="user.rank === 3" color="brown darken-2" size="20">mdi-crown</v-icon>
                                                    <span v-else class="rank-number">{{ user.rank }}</span>
                                                  </v-avatar>
                                                  <div class="rank-user-info">
                                                    <div class="rank-user-name">{{ user.mail }}</div>
                                                    <div class="rank-user-points">{{ user.point }} pt</div>
                                                  </div>
                                                </v-card>
                                              </v-col>
                                            </v-row>
                                          </v-container>
                                        </v-col>
                                      </v-row>
                                    </v-container>
                                  </v-col>
                                </v-row>
                              </v-container>
                            </v-card-text>
                            <v-card-actions class="rank-card-actions">
                              <v-btn class="close-btn" color="primary" @click="rank_menu = false">
                                <v-icon left>mdi-close</v-icon>
                                閉じる
                              </v-btn>
                            </v-card-actions>
                          </v-card>
                        </v-dialog>
                        </div>
                      </div>

                    <div class="progress">
                      <div class="p1">
                        <v-progress-circular :model-value="progress" :size="120" :width="15" color="primary">
                          {{ progress }}%
                        </v-progress-circular>
                        <h3>学習進捗率</h3>
                      </div>
                      <div class="p1">
                        <v-progress-circular :model-value="login" :size="120" :width="15" color="secondary">
                          {{ login }}日
                        </v-progress-circular>
                        <h3>累計ログイン日数</h3>
                      </div>
                    </div>
                  </div>

                  <div class="bar">
                    <v-btn @click = "opengoals" class = "btn" color = "primary">
                      <v-icon class="mr-2">mdi-flag-checkered</v-icon>
                      <span><b>達成した目標</b></span>
                    </v-btn>
                    <v-dialog class ="g-dialog" v-model="gmenu" max-width="600">
                      <v-card class = 'g-card'>
                        <!--<v-card-title class = "g-card-title"><h3><b><u>達成した目標</u></b></h3></v-card-title>-->
                        <v-card-text>
                          <v-list>
                            <v-list-item v-for="(goal, index) in completedGoals" :key="index" class="g-completed-goal">
                              <div style="display: flex; justify-content: space-around; align-items: center;">
                                <v-icon color="blue" size="20">mdi-trophy</v-icon>
                                <div class = "g-goal">
                                  <b>{{ goal.details }}</b>
                                </div>
                                <v-btn class="custom-btn" @click="goaltoggleCompletion(index)">
                                  <v-icon size="16" class="btn-icon">
                                    {{ goal.completed ? "mdi-check-circle" : "mdi-circle-outline" }}
                                  </v-icon>
                                  {{ goal.completed ? "達成" : "未達成" }}
                                </v-btn>
                              </div>
                            </v-list-item>
                          </v-list>
                          <h4 v-if = "completedGoals.length > 0"class="d-flex align-center justify-end">{{ completedGoals.length }}つの目標を達成したよ！</h4>
                          <h5 v-if = "completedGoals.length == 0"><v-icon>mdi-pin</v-icon>目標達成したら追加されるよ</h5>
                          <h5 v-if = "completedGoals.length <= 5"><v-icon>mdi-pin</v-icon>この調子で学習を続けよう</h5>
                          <h5 v-if = "completedGoals.length > 5"><v-icon>mdi-pin</v-icon>これでテストもばっちり！</h5>
                        </v-card-text>
                        <v-card-actions>
                          <v-btn class = " g-btn" text color="primary" @click="gmenu = false">閉じる</v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>

                      <v-btn class="btn" color="secondary" @click="dialog = true">
                        <v-icon class="mr-2">mdi-arrow-down</v-icon>
                        <b>目標を設定しよう</b>
                      </v-btn>
                    <v-dialog v-model="dialog" max-width="400">
                      <v-card class="dialog-card" elevation="3">
                        <v-card-title class="text-h6">
                          目標設定
                        </v-card-title>
                        <v-divider></v-divider>
                        <v-card-text>
                          <v-form>
                            <v-textarea
                              label="目標を入力してください"
                              v-model="newGoal.details"
                              outlined
                              dense
                              clearable
                              rows="3"
                              placeholder="例：第1回の演習問題を全て解く"
                              hide-details="auto"
                              class="mt-2"
                            ></v-textarea>
                          </v-form>
                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn
                            text
                            color="grey darken-1"
                            @click="dialog = false"
                          >
                            <v-icon left>mdi-close</v-icon>
                            キャンセル
                          </v-btn>
                          <v-btn
                            color="primary"
                            @click="addGoal"
                            :disabled="!newGoal.details"
                          >
                            <v-icon left>mdi-check</v-icon>
                            保存
                          </v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>

                    <v-list class="scrollable-list">
                      <v-list-item v-for="(goal, index) in notgoal" :key="index" class="goal-card" elevation="2">
                        <v-row>
                          <v-col cols="1" class="d-flex align-center justify-center">
                            <v-icon :class="{'completed-icon': goal.completed, 'pending-icon': !goal.completed}">
                              {{ goal.completed ? 'mdi-check-circle' : 'mdi-progress-clock' }}
                            </v-icon>
                          </v-col>
                          <v-col cols="8">
                            <div class="goal-details">
                              <p class="goal-title"><b>{{ goal.details }}</b></p>
                            </div>
                          </v-col>
                          <v-col cols="3" class="d-flex align-center justify-end">
                            <div class="button-group">
                              <v-btn small :color="goal.completed ? 'green' : 'primary'" class="goal-btn" @click="toggleCompletion(index)">
                                {{ goal.completed ? "目標達成" : "未達成" }}
                              </v-btn>
                              <v-btn small color="primary" class="goal-btn" @click = "deletegoal(index)">
                                削除
                              </v-btn>
                            </div>
                          </v-col>
                        </v-row>
                      </v-list-item>
                    </v-list>
                  </div>

                  <div class="button-container">
                    <h2>科目選択</h2>
                    <v-row>
                      <v-col cols='6' v-for='course in courses' :key='course.course_id' class='pb-4'>
                        <pC_CourseSelect :create='user_info.create' :course='course' @move_course='move_course' @move_score='move_score' @move_syllabus_info='move_syllabus_info'/>
                      </v-col>
                    </v-row>
                  </div>
                  <div class = "an-container">
                    <pC_Announcements :user_info='user_info' ></pC_Announcements>
                  </div>
                </div>
              </v-container>
            </v-row>
          </v-container>
        </v-responsive>
      </v-container>
    </v-main>
  </div>
</template>


<style scoped>
.g-goal{
  flex-grow: 1;
}
.icon-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: flex-start;
  gap: 30px;
  padding: 10px;
}
.an-container {
  width: 100%;
  max-width: 1200px;
}
.icon-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 550px;
  background: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 20px;
}
.icon2 {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}
.icon {
  width: 60px;
  height: 60px;
  fill: #1976D2;
}

.name {
  font-size: 20px;
  font-weight: bold;
}
.points-display {
  display: flex;
  align-items: center;
  font-size: 20px;
  color: #94ce0e;
  gap: 8px;
  margin-left: 14px;
}
.coin-icon {
  font-size: 25px;
  color: #94ce0e;
}
.points {
  font-weight: bold;
}
.progress {
  display: flex;
  justify-content: space-around;
  width: 100%;
  margin-top: 20px;
  gap: 40px;
}

.p1 {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 10px;
}

.bar {
  display: flex;
  flex-direction: column;
  margin-top: 8px;
  gap: 20px;
  width: 100%;
}

.btn {
  margin-bottom: 2px;
  width: 100%;
  height: 40px;
  font-size: 16px;
}
.v-list {
  width: 100%;
  margin-top: 20px;
  margin-right: 10px;
}

.g-card {
  max-width: 90%;
}
.g-card-title {
  font-size: 20px;
  text-align: center;
  padding: 14px;
}
.g-completed-goal {
  background: linear-gradient(90deg, #e8ecf5, #c8d0e6);
  margin-bottom: 8px;
  overflow-y: auto;
  padding: 10px;
  border-left: solid 10px #2d8fdd;
  border-bottom: solid 2px #dadada;
  text-align: center;
}
.g-btn {
  border-radius: 24px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: bold;
}
.custom-btn {
  background-color: #e3f2fd;
  color: #1565c0;
  border-radius: 8px;
  padding:14px;
  font-weight: bold;
  display: flex;
  align-items: center;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}
.p-list-item{
  border-radius: 8px;
  padding: 10px 15px;
  margin-bottom: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background: whitesmoke;
  border-left: solid 8px ;
  border-right: solid 8px;
  padding: 0 0.5em;
  position: relative;
  line-height: 2.5;
  text-align: center;
}
.scrollable-list {
  max-height: 170px;
  margin-top: 0px;
  overflow-y: auto;
  border: 1px solid #ddd;
  padding: 13px;
  border-radius: 8px;
  background-color: #f9f9f9;
}
.goal-card {
  margin-bottom: 10px;
  border-radius: 8px;
  background-color: white;
  padding: 12px;
}
.goal-details {
  margin-left: 8px;
}
h4.d-flex {
  font-size: 1.2rem;
  color: #4c95af;
  font-weight: bold;
  text-align: center;
  margin: 10px 0;
}
h5 {
  font-size: 1rem;
  gap:10px;
  color: #9e9e9e;
  text-align: right;
  margin-top: 5px;
}
.p-list-btn, .r-list-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  box-shadow: none;
  padding: 4px;
  margin-left: 8px;
  height: 40px;
  width: 40px;
}
.p-list-icon {
  font-size: 45px;
  color: #94ce0e;
}
.button-group {
  display: flex;
  gap: 8px;
  min-width: 180px;
  justify-content: flex-end;
}
.goal-btn {
  min-width: 80px !important;
  width: 80px !important;
  height: 32px !important;
  font-size: 14px;
  margin: 0 4px;
}
.goal-title {
  display: block;
  font-size: 17px;
  max-width: 215px; 
  word-break: break-word;
  margin-top: 7px;
}
.pending-icon{
  font-size: 30px;
  margin-left: 12px;
}
.completed-icon{
  font-size: 30px;
  margin-left: 12px;
}
.card-custom {
  width: 220px;
  height: 50px;
  margin: 8px;
  background: linear-gradient(145deg, #ffffff, #f5f7fa);
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card-custom:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.rank-list-container {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: calc(100vh - 250px);
  max-height: 590px;
  overflow-y: auto;
}

.rank-list-title {
  text-align: center;
  padding: 14px;
  font-size: 20px;
  margin-bottom: 16px;
  color: #333;
}

.rank-columns {
  gap: 12px;
  padding: 0 8px;
}

.column-container {
  padding: 4px;
}

.rank-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  margin: 6px 0;
  border-radius: 8px;
  background:#f9f8f8;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  height: 36px;
  width: 100%;
  transition: all 0.2s ease;
}

.rank-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.rank-item-top {
  background: linear-gradient(135deg, #ffffff, #fff8e1);
  border-left: 3px solid #ffd700;
}

.rank-number {
  font-weight: bold;
  color: #666;
  font-size: 0.85rem;
}

.rank-user-info {
  display: grid;
  grid-template-columns: 1fr 70px;
  align-items: center;
  gap: 8px;
  width: 100%;
  margin-left: 8px;
}

.rank-user-name {
  font-weight: 500;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 0.9rem;
  padding-right: 4px;
}

.rank-user-points {
  font-weight: bold;
  color: #1976D2;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.85rem;
  text-align: center;
  justify-self: end;
}

.rank-card {
  border-radius: 16px;
  overflow: hidden;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.rank-card-title {
  background: linear-gradient(135deg, #1976D2, #64B5F6);
  color: white;
  padding: 20px;
  font-size: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.rank-card-content {
  padding: 20px;
}

.chart-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.chart-title {
  color: #1976D2;
  font-size: 20px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.rank-chart {
  margin-bottom: 20px;
}

.user_point {
  display: flex;
  justify-content: center; 
  align-items: center; 
  text-align: center;
  padding: 25px;
  margin: 30px auto;
  background: linear-gradient(145deg, #ffffff, #f0f0f0);
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  width: 90%; 
  border-left: 5px solid #1976D2;
}

.user_point h2 {
  color: #333;
  font-size: 1.4rem;
  font-weight: bold;
  margin: 0;
}

.rank-card-actions {
  padding: 16px;
  background: #f5f7fa;
  border-top: 1px solid #e0e0e0;
  position: sticky;
  bottom: 0;
  display: flex;
  justify-content: center;
}

.close-btn {
  min-width: 120px;
  border-radius: 20px;
  text-transform: none;
  font-weight: 500;
}

@media (max-width: 1600px) {
  .rank-list-container {
    padding: 12px;
    width: 680px;
    height: 500px;
  }

  .rank-item {
    height: 40px;
    padding: 3px;
    margin: 4px 0;
    width: 185px;
  }

  .rank-user-info {
    grid-template-columns: 1fr 65px;
    gap: 3px;
  }

  .rank-user-name {
    font-size: 0.8rem;
  }

  .rank-user-points {
    font-size: 0.85rem;
    padding: 2px 6px;
  }
}

@media (max-width: 1400px) {
  .rank-list-container {
    padding: 12px;
    width: 550px;
    height: auto;
    min-height: 450px;
    max-height: 500px;
  }

  .rank-item {
    height: 40px;
    padding: 3px;
    margin: 4px 0;
    width: 150px;
  }

  .rank-user-info {
    grid-template-columns: 1fr 60px;
    gap: 3px;
  }

  .rank-user-name {
    font-size: 0.75rem;
  }

  .rank-user-points {
    font-size: 0.8rem;
    padding: 2px 4px;
  }
}

@media (max-width: 1200px) {
  .rank-card > .v-card-text {
    padding: 12px;
  }

  .rank-list-container {
    width: 450px;
    max-height: none;
    width: auto;
    height: auto;
    padding: 8px;
  }

  .rank-item {
    height: 36px;
    padding: 2px;
    margin: 3px 0;
    width: 170px;
  }

  .rank-user-info {
    grid-template-columns: 1fr 55px;
    gap: 2px;
  }

  .rank-user-name {
    font-size: 0.7rem;
  }

  .rank-user-points {
    font-size: 0.75rem;
    padding: 2px 3px;
  }

  .v-row > .v-col-6 {
    flex: 0 0 100%;
    max-width: 100%;
  }

  .chart-container {
    margin-bottom: 16px;
  }
}

.welcome-card {
  border-radius: 16px;
  overflow: hidden;
}

.welcome-title {
  background: linear-gradient(135deg, #1976D2, #64B5F6);
  color: white;
}

.welcome-stepper {
  background: transparent;
}

.welcome-actions {
  background: #f5f7fa;
  border-top: 1px solid #e0e0e0;
}

@media (min-width: 1200px) {
  .icon-container {
    flex-direction: row;
  }

  .icon-item {
    flex: 1;
    min-width: 300px;
  }

  .bar {
    flex: 1;
    min-width: 300px;
  }
}
</style>