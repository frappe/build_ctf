import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
  },
  {
    path: '/cBSZTcX5OScQtKOScyahY9o3ShRcWDK6VqlBJl6CV2ZtB',
    name: 'Auth',
    component: () => import('@/pages/Auth.vue'),
  }
]

let router = createRouter({
  history: createWebHistory('/frontend'),
  routes,
})

export default router
