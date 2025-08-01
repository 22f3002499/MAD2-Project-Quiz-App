import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {name:"login" , path : "/login/" , component : () => import('@/views/common/LoginView.vue') , meta : {guest : true}},
  {name:"register" , path : "/register/" , component : () => import('@/views/user/RegisterView.vue') , meta : {guest : true}},
  {name:"userHome" ,path : "/" , component : () => import('@/views/user/HomeView.vue') , meta : {authRequired: true} , roles:['user']},
  {name:"begin-quiz" ,path : "/begin-quiz/:quizId/" , component : () => import('@/views/user/BeginQuizView.vue') , meta : {authRequired: true}},
  {name:"userScores" ,path : "/scores/" , component : () => import('@/views/user/ScoresView.vue') , meta : {authRequired: true}},
  {name:"userStats" ,path : "/stats/" , component : () => import('@/views/user/StatsView.vue') , meta : {authRequired: true}},

  {name:"adminHome",path : "/admin/" , component : () => import('@/views/admin/HomeView.vue') , meta : {authRequired: true} , roles:['admin']},
  {name:"adminSubjects",path : "/admin/subjects/" , component : () => import('@/views/admin/AdminSubjectView.vue') , meta : {authRequired: true} , roles:['admin']},
  {name:"adminQuizzes",path : "/admin/quizzes/" , component : () => import('@/views/admin/AdminQuizView.vue') , meta : {authRequired: true} , roles:['admin']},

  // {path : "/admin" , component : () => import('@/views/AdminView.vue') , meta : {authRequired: true , roles : ['admin']}},
]
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.guest && auth.isAuthenticated) return '/'
  if (to.meta.authRequired && !auth.isAuthenticated) return '/login/'
  if (to.meta.roles && !auth.hasAnyRole(to.meta.roles)) return '/'
})

export default router


