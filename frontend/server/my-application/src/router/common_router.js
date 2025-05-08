export const c_root = [
  {
    path: '/',
    name: 'Root',
    redirect: function() {
      return "/Login"
    }
  },{ // 共通ページ
    path: '/Login',
    name: 'C_Login',
    component: () => import('@/views/common/C_Login.vue')
  },
]