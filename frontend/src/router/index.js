import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '@/views/auth/LoginView.vue'
import RegisterStudentView from '@/views/auth/RegisterStudentView.vue'
import RegisterCompanyView from '@/views/auth/RegisterCompanyView.vue'

import AdminLayout from "@/layouts/AdminLayout.vue"
import StudentLayout from "@/layouts/StudentLayout.vue"
import CompanyLayout from "@/layouts/CompanyLayout.vue"
import Students from "@/views/admin/Students.vue"
import Companies from "@/views/admin/Companies.vue"
import Drives from "@/views/admin/Drives.vue"
import Placements from "@/views/admin/Placements.vue"
import Applications from "@/views/admin/Applications.vue"
import Dashboard from "@/views/admin/Dashboard.vue"

import Home from '@/views/Home.vue'

const routes = [
  { path: '/', name: 'Landing', component: () => import('@/views/LandingView.vue') },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register/student', name: 'RegisterStudent', component: RegisterStudentView },
  { path: '/register/company', name: 'RegisterCompany', component: RegisterCompanyView },

  { path: '/:pathMatch(.*)*', redirect: '/' },

  {
    path: "/admin",
    component: AdminLayout,
    children: [
      { path: "", component: Dashboard },
      { path: "students", component: Students },
      { path: "companies", component: Companies },
      { path: "drives", component: Drives },
      { path: "placements", component: Placements },
      { path: "applications", component: Applications }
    ]
  },
  {
    path: "/student",
    component: StudentLayout,
    children: [
      { path: "", component: () => import("@/views/student/AvailableDrives.vue") },
      // ADD THIS LINE:
      { path: "drives", component: () => import("@/views/student/Drives.vue") }, 
      { path: "applications", component: () => import("@/views/student/MyApplications.vue") },
      { path: "profile", component: () => import("@/views/student/Profile.vue") }
    ]
  },
  {
    path: "/company",
    component: CompanyLayout,
    children: [
      { path: "", component: () => import("@/views/company/Drives.vue") },
      { path: "profile/edit", component: () => import("@/views/company/EditProfile.vue") },
      { path: "drives/create", component: () => import("@/views/company/CreateDrive.vue") },
      { path: "drive/:id/edit", component: () => import("@/views/company/EditDrive.vue") },
      { path: "drive/:id/applicants", component: () => import("@/views/company/DriveApplicants.vue") }
    ]
  }

]

const router = createRouter({

  history: createWebHistory(),

  routes

})

export default router