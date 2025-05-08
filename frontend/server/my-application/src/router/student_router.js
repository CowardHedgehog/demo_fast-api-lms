export const s_root = [
    /*{
        path: '/Home',
        name: 'S_Home',
        component: () => import('@/views/students/S_Home.vue')
    },*/{
        path: '/Home',
        name: 'S_Home',
        component: () => import('@/views/students/S_Top.vue'),
        // props: (route) => ({course_id: Number(route.params.course_id)})
    },{
        path: '/UserSetting',
        name: 'S_UserSetting',
        component: () => import('@/views/students/S_UserSetting.vue')
    },{
        path: '/UpdatePassword',
        name: 'S_UpdatePassword',
        component: () => import('@/views/students/S_UpdatePassword.vue')
    },{
        path: '/Course/:course_id',
        name: 'S_Course',
        component: () => import('@/views/students/S_Course.vue'),
        props: (route) => ({course_id: Number(route.params.course_id)})
    },{
        path: '/:course_id/Week/:week_id/:page',
        name: 'S_Week',
        component: () => import('@/views/students/S_Week.vue'),
        props: (route) => ({course_id: Number(route.params.course_id), week_id: Number(route.params.week_id), page: Number(route.params.page)})
    },{
        path: '/:course_id/Week/:week_id/Flow/:flow_id',
        name: 'S_Flow',
        component: () => import('@/views/students/S_Flow.vue'),
        props: (route) => ({course_id: Number(route.params.course_id), week_id: Number(route.params.week_id), flow_id: Number(route.params.flow_id)})
    },{
        path: '/:course_id/:week_id/:flow_id/FlowSession/:flow_session_id/:page',
        name: 'S_FlowSession',
        component: () => import('@/views/students/S_FlowSession.vue'),
        props: (route) => ({course_id: Number(route.params.course_id), week_id: Number(route.params.week_id), flow_id: Number(route.params.flow_id), flow_session_id: Number(route.params.flow_session_id), page: Number(route.params.page)})
    },{
        path: '/:course_id/:week_id/:flow_id/FlowCompletion/:flow_session_id',
        name: 'S_FlowCompletion',
        component: () => import('@/views/students/S_FlowCompletion.vue'),
        props: (route) => ({course_id: Number(route.params.course_id), week_id: Number(route.params.week_id), flow_id: Number(route.params.flow_id), flow_session_id: Number(route.params.flow_session_id)})
    },{
        path: '/Profile/:course_id',
        name: 'S_Profile',
        component: () => import('@/views/students/S_Profile.vue'),
        props: (route) => ({course_id: Number(route.params.course_id)})
    },{
        path: '/WeekFlows/:course_id/:week_id',
        name: 'S_WeekFlows',
        component: () => import('@/views/students/S_WeekFlows.vue'),
        props: (route) => ({course_id: Number(route.params.course_id), week_id: Number(route.params.week_id)})
    },{
        path: '/SyllabusInfo/:course_id',
        name: 'S_SyllabusInfo',
        component: () => import('@/views/students/S_SyllabusInfo.vue'),
        props: (route) => ({course_id: Number(route.params.course_id)})
    },{
        path: '/UserScore/:course_id',
        name: 'S_CourseScore',
        component: () => import('@/views/students/S_Course_Score.vue'),
        props: (route) => ({course_id: Number(route.params.course_id)})
    }
]