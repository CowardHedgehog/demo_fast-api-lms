export const t_root = [
  {
    path: '/t/Home',
    name: 'T_Home',
    component: () => import('@/views/teachers/T_Home.vue')
  },{
    path: '/t/Subject/:subject_id',
    name: 'T_Subject',
    component: () => import('@/views/teachers/T_Subject.vue'),
    props: (route) => ({subject_id: Number(route.params.subject_id)})
  },{
    path: '/t/Course/:course_id',
    name: 'T_Course',
    component: () => import('@/views/teachers/T_Course.vue'),
    props: (route) => ({course_id: Number(route.params.course_id)})
  },{
    path: '/t/RegisterWeek/:course_id',
    name: 'T_RegisterWeek',
    component: () => import('@/views/teachers/T_RegisterWeek.vue'),
    props: (route) => ({course_id: Number(route.params.course_id)})
  },{
    path: '/t/SyllabusInfo/:course_id',
    name: 'T_SyllabusInfo',
    component: () => import('@/views/teachers/T_SyllabusInfo.vue'),
    props: (route) => ({course_id: Number(route.params.course_id)})
  },{
    path: '/t/CourseTaking/:course_id',
    name: 'T_CourseTaking',
    component: () => import('@/views/teachers/T_CourseTaking.vue'),
    props: (route) => ({course_id: Number(route.params.course_id)})
  },{
    path: '/t/:course_id/Week/:week_id/:page',
    name: 'T_Week',
    component: () => import('@/views/teachers/T_Week.vue'),
    props: (route) => ({course_id: Number(route.params.course_id), week_id: Number(route.params.week_id), page: Number(route.params.page)})
  },{
    path: '/t/:course_id/Week/:week_id/Flow/:flow_id',
    name: 'T_Flow',
    component: () => import('@/views/teachers/T_Flow.vue'),
    props: (route) => ({course_id: Number(route.params.course_id), week_id: Number(route.params.week_id), flow_id: Number(route.params.flow_id)})
  },{
    path: '/t/:course_id/:week_id/:flow_id/FlowSession/:flow_session_id/:page',
    name: 'T_FlowSession',
    component: () => import('@/views/teachers/T_FlowSession.vue'),
    props: (route) => ({course_id: Number(route.params.course_id), week_id: Number(route.params.week_id), flow_id: Number(route.params.flow_id), flow_session_id: Number(route.params.flow_session_id), page: Number(route.params.page)})
  },{
    path: '/t/:course_id/:week_id/:flow_id/FlowCompletion/:flow_session_id',
    name: 'T_FlowCompletion',
    component: () => import('@/views/teachers/T_FlowCompletion.vue'),
    props: (route) => ({course_id: Number(route.params.course_id), week_id: Number(route.params.week_id), flow_id: Number(route.params.flow_id), flow_session_id: Number(route.params.flow_session_id)})
  },{
    path: '/t/:course_id/EditWeek/:week_id',
    name: 'T_EditWeek',
    component: () => import('@/views/teachers/T_EditWeek.vue'),
    props: (route) => ({course_id: Number(route.params.course_id), week_id: Number(route.params.week_id)})
  },{
    path: '/t/AddUser',
    name: 'T_AddUser',
    component: () => import('@/views/teachers/T_AddUser.vue')
  },{
    path: '/t/EditCourseInfo/:course_id',
    name: 'T_EditCourseInfo',
    component: () => import('@/views/teachers/T_EditCourseInfo.vue'),
    props: (route) => ({course_id: Number(route.params.course_id)})
  },{
    path: '/t/RegisterCourse/:subject_id',
    name: 'T_RegisterCourse',
    component: () => import('@/views/teachers/T_RegisterCourse.vue'),
    props: (route) => ({subject_id: Number(route.params.subject_id)})
  },{
    path: '/t/UserSetting',
    name: 'T_UserSetting',
    component: () => import('@/views/teachers/T_UserSetting.vue')
  },{
    path: '/t/UpdatePassword',
    name: 'T_UpdatePassword',
    component: () => import('@/views/teachers/T_UpdatePassword.vue')
  },{
    path: '/t/CourseScore/:course_id',
    name: 'T_CourseScore',
    component: () => import('@/views/teachers/T_CourseScore.vue'),
    props:(route) => ({course_id: Number(route.params.course_id)})
  },{
    path: '/t/AnnouncementManagement',
    name: 'T_AnnouncementManagement',
    component: () => import('@/views/teachers/T_AnnouncementManagement.vue'),
    meta: { requiresAuth: true } // ログイン必須のページとして設定
  }
]