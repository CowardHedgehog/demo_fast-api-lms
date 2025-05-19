import { createRouter, createWebHistory } from 'vue-router'
import { c_root } from './common_router'
import { s_root } from './student_router'
import { t_root } from './teacher_router'
// import { test_root } from './test_router.js'

// const routes = [...c_root, ...s_root, ...t_root, ...test_root]
const routes = [...c_root, ...s_root, ...t_root]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  router['referrer'] = from
  next()
})

export default router