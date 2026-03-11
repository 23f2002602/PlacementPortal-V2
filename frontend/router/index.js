import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/auth/LoginView.vue'

const routes = [
  { path: '/login', name: 'Login', component: LoginView },

  { path: '/', redirect: '/login' },

  { path: '/:pathMatch(.*)*', redirect: '/login' },

  {
  path: "/student",
  component: StudentLayout,
  children: [
    { path: "", component: () => import("@/views/student/AvailableDrives.vue") },
    { path: "drives", component: () => import("@/views/student/Drives.vue") }, // ADDED THIS
    { path: "applications", component: () => import("@/views/student/MyApplications.vue") },
    { path: "profile", component: () => import("@/views/student/Profile.vue") }
  ]
},

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router