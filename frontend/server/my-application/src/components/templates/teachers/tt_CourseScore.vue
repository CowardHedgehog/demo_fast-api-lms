<script setup>

import axios from 'axios'
import { ref, computed } from 'vue'

const session_error = ref(false)
const user_info = ref({})

import { useTheme } from 'vuetify'
const colors = [
  '#0000dd', // 青
  '#dddd00', // 黄色
  '#aa0000', // 赤
  '#008000', // 緑
  '#ffa500', // オレンジ
  '#800080', // 紫
  '#aa00aa', // ピンク
  '#00ffff',//シアン
  '#98d98e',//若草
  '#a59aca',//すみれ
  '#762f07',//栗色
  '#bce2e8',//水色
  '#928c36',//鶯色
  '#f8b500',//山吹
  '#f6bfbc'
];
const theme = useTheme()

import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  course_id : {
    type: Number,
    required: true
  }
})
const apiResponseData = ref([]);
const showCheckboxes = ref(false);
const exerciseList = ref([]);
const selectedExercises = ref([]);

const extractGradesByExercise = (data) => {
  const gradesByExercise = {}
  data.forEach(content => {
    Object.values(content).forEach(exercises => {
      exercises.forEach(exercise => {
        Object.keys(exercise).forEach(exerciseName => {
          const grades = exercise[exerciseName].map(item => item.flow_session_grade)
          gradesByExercise[exerciseName] = grades
        })
      })
    })
  })

  return gradesByExercise
}

const get_teacher_score = async () => {
  try {
    const response =await axios.get(`https://demo-fast-api-lms.vercel.app/get_flow_session_teacher_score/${props.course_id}`, { withCredentials: true })
    console.log("APIのレスポンスデータ:", response.data)
    apiResponseData.value = response.data
  } catch (error) {
    console.error("学生の成績取得中にエラーが発生:", error)
  }
}

get_teacher_score()

const calculateStatistics = (grades) => {
  if (!grades || grades.length === 0) {
    return {
      average: undefined,
      max: undefined,
      min: undefined,
      median: undefined
    };
  }
  const average = grades.reduce((acc, curr) => acc + curr, 0) / grades.length
  const max = Math.max(...grades)
  const min = Math.min(...grades)
  const sortedGrades = [...grades].sort((a, b) => a - b)
  const middle = Math.floor(sortedGrades.length / 2)
  const median = sortedGrades.length % 2 === 0
    ? (sortedGrades[middle - 1] + sortedGrades[middle]) / 2
    : sortedGrades[middle]
  const count = grades.length

  return { average, max, min, median,count }
}

const exerciseStatistics = computed(() => {
  const gradesByExercise = extractGradesByExercise(apiResponseData.value)
  const stats = {}

  Object.keys(gradesByExercise).forEach(exerciseName => {
    stats[exerciseName] = calculateStatistics(gradesByExercise[exerciseName])
  })

  return stats
})

const ranges = [
  { min: 0, max: 15 },
  { min: 15, max: 30 },
  { min: 30, max: 45 },
  { min: 45, max: 60 },
  { min: 60, max: 75 },
  { min: 75, max: 90 },
  { min: 90, max: 101 }
]

const calculateRangeCounts = (grades) => {
  return ranges.map(range => {
    return grades.filter(value => value >= range.min && value < range.max).length
  })
}

const chartdata = computed(() => {
  const gradesByExercise = extractGradesByExercise(apiResponseData.value)
  
  const datasets = Object.keys(gradesByExercise).map((exerciseName, index) => {
    if (!exerciseList.value.includes(exerciseName)) {
      exerciseList.value.push(exerciseName);
    }
    return {
      label: exerciseName,
      data: calculateRangeCounts(gradesByExercise[exerciseName]),
      backgroundColor: colors[index % colors.length],
      hoverBackgroundColor: theme.global.current.value.colors.secondary,
    }
  })

  const filteredDatasets = selectedExercises.value.length > 0 ? datasets.filter(dataset => selectedExercises.value.includes(dataset.label)) : datasets;
  return {
    labels: ['0〜15', '15〜30', '30〜45', '45〜60', '60〜75', '75〜90', '90〜100'],
    datasets: filteredDatasets
  }
})

const chartOptions = ref({
  responsive: true,
  scales: {
    y: {
      suggestedMin: 0,
      suggestedMax: 30
    }
  },
  plugins: {
    title: {
      display: true,
      text: '演習問題 成績分布',
      color: 'black',
      position: 'top',
      align: 'center',
      font: {
        weight: 'bold',
        size: 30,
      },
      padding: 8,
      fullSize: true,
    }
  }
})

const home_profile = () => {
  axios.get('https://demo-fast-api-lms.vercel.app/home_profile', { withCredentials: true }).then(function(response){
    user_info.value = response.data
  }).catch(function(error){
    if(error.response?.status == 401) { session_error.value = true }
    else{ console.log(error.response) }
  })
}

home_profile()
</script>

<template>
  <div>
    <Bar :data="chartdata" :options="chartOptions" />
    <v-btn @click="showCheckboxes = !showCheckboxes" class="mb-4">
      {{'表示する演習問題をフィルタリング'}}
      <v-icon>mdi-arrow-right-thin</v-icon>
    </v-btn>
    <div class="status-container">
      <span v-if="selectedExercises.length > 0">
        選択中: {{ selectedExercises.join(', ') }}
      </span>
    </div>
    <v-dialog v-model="showCheckboxes" max-width="800px">
      <v-card>
        <v-card-title><h3>演習問題を選択</h3></v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols = "4" v-for="exercise in exerciseList">
              <v-checkbox :key="exercise" :label="exercise" :value="exercise" v-model="selectedExercises"></v-checkbox>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="showCheckboxes = false">閉じる</v-btn>
        </v-card-actions>
      </v-card>
  </v-dialog>

    <table border="6" class='tablec'>
    <tr>
      <th>演習問題</th>
      <th>平均値</th>
      <th>最大値</th>
      <th>最小値</th>
      <th>中央値</th>
      <th>データ数</th>
    </tr>
    <tr v-for="(stats, exerciseName) in exerciseStatistics" :key="exerciseName">
      <td>{{ exerciseName }}</td>
      <td v-if="typeof stats.average === 'number' && !isNaN(stats.average)">{{ stats.average.toFixed(1) }}%</td>
      <td v-else>-</td>
      <td v-if="typeof stats.max === 'number' && !isNaN(stats.max)">{{ stats.max.toFixed(1) }}%</td>
      <td v-else>-</td>
      <td v-if="typeof stats.min === 'number' && !isNaN(stats.min)">{{ stats.min.toFixed(1) }}%</td>
      <td v-else>-</td>
      <td v-if="typeof stats.median === 'number' && !isNaN(stats.median)">{{ stats.median.toFixed(1) }}%</td>
      <td v-else>-</td>
      <td v-if="typeof stats.median === 'number' && !isNaN(stats.count)">{{ stats.count }}</td>
      <td v-else>-</td>
    </tr>
    </table>
  </div>
</template>

<style scoped>
.tablec {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Helvetica', sans-serif;
  margin: 20px auto;
}

.tablec th, .tablec td {
  padding: 10px;
  text-align: center;
  border-left: 1px solid #ddd;
}

.tablec th:first-child, .tablec td:first-child {
  border-left: none;
}

.tablec th {
  background-color: #0b37d3;
  color: white;
  font-weight: bold;
}

.tablec td {
  background-color: #fafafa;
}

.tablec tr:hover td {
  background-color: #eee;
}
.mb-4 {
  display: block;
  margin: 20px auto;
  width: fit-content;
  padding: 5px 20px;
  background-color: transparent; 
  color: black;
  font-size: 16px;
  font-weight: bold;
  border: 2px solid #007bff; 
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}
.v-dialog .v-card {
  padding: 16px;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.v-card-title {
  font-size: 18px;
  font-weight: bold;
  text-align: center; 
  margin-bottom: 12px;
}

.v-card-text {
  display: flex;
  flex-direction: column;
  gap: 1px;
}
.status-container {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  margin: 20px 0;
  font-size: 16px;
  color: #333;
}
</style>
