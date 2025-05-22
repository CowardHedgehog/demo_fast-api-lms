<script setup>
// import
import axios from 'axios'
import { ref ,computed} from 'vue'
import {Bar, Line} from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale,PointElement,LineElement,plugins, scales, Ticks } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale,PointElement,LineElement)
import {useTheme} from 'vuetify'

const theme = useTheme()
const ascTimeSort = (a,b) =>{
  return a >b ? 1: -1
}

const props = defineProps({
  course_id : {
    type: Number,
    required: true
  }
})
const data = ref([])
const line_data = ref([]);
const scores = ref([]);
const names = ref([]);

const extractGrades = (data) => {
  const localScores = [];
  const localNames = [];

  const findMaxGrades = (obj, contextPath = '') => {
    if (Array.isArray(obj)) {
      let maxGrade = -Infinity;
      obj.forEach(subItem => {
        if (typeof subItem === 'object' && subItem !== null) {
          if (subItem.hasOwnProperty('flow_session_grade')) {
            if (subItem.flow_session_grade > maxGrade) {
              maxGrade = subItem.flow_session_grade;
            }
          } else {
            findMaxGrades(subItem, contextPath);
          }
        }
      });
      if (maxGrade !== -Infinity) {
        localScores.push(maxGrade.toFixed(1));
        localNames.push(contextPath);
      }
    } else if (typeof obj === 'object' && obj !== null) {
      Object.entries(obj).forEach(([key, value]) => findMaxGrades(value, contextPath ? `${contextPath} > ${key}` : key));
    }
  };

  findMaxGrades(data);
  scores.value = localScores;
  names.value = localNames;
};

const line_extractGrades = (data) => {
  const localline_data = []

  if (Array.isArray(data)) {
    data.forEach((content) => {
      if (typeof content === 'object' && content !== null) {
        Object.keys(content).forEach((lesson) => {
          if (Array.isArray(content[lesson])) {
            content[lesson].forEach((exercise) => {
              if (typeof exercise === 'object' && exercise !== null) {
                Object.keys(exercise).forEach((problem) => {
                  if (Array.isArray(exercise[problem])) {
                    exercise[problem].forEach((session) => {
                      if (session && session.finish_date_time) {
                        const date = new Date(session.finish_date_time);
                        const grade = session.flow_session_grade;

                        localline_data.push({
                          problem: problem, 
                          date: date, 
                          grade: grade.toFixed(1)
                        });
                      }
                    });
                  }
                });
              }
            });
          }
        });
      }
    });
  }
  localline_data.sort((a, b) => ascTimeSort(a.date, b.date));
  line_data.value = localline_data;
}

const get_student_score = async () => {
  try {
    const response = await axios.get(`https://demo-fast-api-lms.vercel.app/get_flow_session_student_score/${props.course_id}`, { withCredentials: true });
    if (response.data) {
      data.value = response.data;
      extractGrades(data.value);
      line_extractGrades(data.value);
    }
  } catch (error) {
    console.error("Error fetching student score:", error);
  }
};

get_student_score();  

const chartdata = computed(() => ({
  labels:names.value,
    datasets: [
    {
      label:'得点率',
      data: scores.value,
      backgroundColor: [theme.global.current.value.colors.primary],
      hoverBackgroundColor:[theme.global.current.value.colors.secondary],
    }
  ]
}));
const chartOptions = {
    responsive: true,
    scales: {
      y: {
        suggestedMin: 0,
        suggestedMax: 100
      }
    },
    plugins: {
      title: {
        display: true,
        text: '演習問題ごとの得点',
        color: 'black',
        position: 'top',
        align: 'center',
        font: {
          weight: 'bold',
          size:25,
        },
        padding: 8,
        fullSize: true,
      }
    }
}

const lineChartdata = computed(() => ({
  labels: line_data.value.map(item => item.date.toISOString().substring(0, 10)),
  datasets: [
    {
      label:'得点率',
      data: line_data.value.map(item => item.grade),
      borderColor: [theme.global.current.value.colors.primary],
      fill: false,
      meta:line_data.value,
      pointRadius: 6
    }
  ]
}));
const line_chartOptions = {
    responsive: true,
    scales: {
      y: {
        suggestedMin: 0,
        suggestedMax: 100,
      }
    },
    plugins: {
      tooltip: {
        callbacks: {
          label: function(context) {
            const problem = context.dataset.meta[context.dataIndex]?.problem || 'No problem';
            const grade = context.raw || '0'; 

            return `${problem}: ${grade}%`;
          }
        }
      },
      title: {
        display: true,
        text: '演習問題得点率の推移',
        color: 'black',
        position: 'top',
        align: 'center',
        font: {
          weight: 'bold',
          size:25,
        },
        padding: 8,
        fullSize: true,
      }
    }
}

// variable
const user_info = ref({})
const session_error = ref(false)

// function
const home_profile = () => {
  axios.get('https://demo-fast-api-lms.vercel.app/home_profile', {withCredentials: true}).then(function(response){
    user_info.value = response.data
  }).catch(
    function(error){
      if(error.response?.status == 401) { session_error.value = true }
      else{console.log(error.response)}
    }
  )
}

// created
home_profile()
</script>

<template>
  <div>
    <div class = 'bar'>
      <Bar :data = 'chartdata' :options = 'chartOptions'/>
    </div>
  
    <div class = 'line'>
      <Line :data="lineChartdata" :options = 'line_chartOptions'/>
    </div>
  </div>
</template>

<style scoped>

div {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 10px;
}

.bar, .line {
  width: 100%;
  margin: 20px 0;
  padding: 10px;
  border-radius: 10px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
}

.line {
  margin-top: 30px;
}

.bar {
  margin-bottom: 30px;
}

</style>