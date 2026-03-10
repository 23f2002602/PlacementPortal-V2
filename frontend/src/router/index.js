import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '@/views/auth/LoginView.vue'
import RegisterStudentView from '@/views/auth/RegisterStudentView.vue'
import RegisterCompanyView from '@/views/auth/RegisterCompanyView.vue'

import AdminLayout from "@/layouts/AdminLayout.vue"
import Dashboard from "@/views/admin/Dashboard.vue"
import Students from "@/views/admin/Students.vue"
import Companies from "@/views/admin/Companies.vue"
import Drives from "@/views/admin/Drives.vue"

const routes = [

  { path: '/login', name: 'Login', component: LoginView },

  { path: '/register/student', name: 'RegisterStudent', component: RegisterStudentView },

  { path: '/register/company', name: 'RegisterCompany', component: RegisterCompanyView },

  { path: '/', redirect: '/login' },

  { path: '/:pathMatch(.*)*', redirect: '/login' },

  {
    path: "/admin",
    component: AdminLayout,
    children: [

    { path: "", component: Dashboard },
    { path: "students", component: Students },
    { path: "companies", component: Companies },
    { path: "drives", component: Drives }
    ]
  }

]

const router = createRouter({

  history: createWebHistory(),

  routes

})

export default router