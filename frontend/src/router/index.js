import { createRouter, createWebHistory } from 'vue-router'

import Landing from '@/pages/Landing.vue';
import CompanyDashboard from "@/pages/CompanyDashboard.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: "/", component: Landing},
    {path: '/login', component: () => import("@/pages/Login.vue") },
    {path: '/register', component: () => import("@/pages/Register.vue") },
    {path: '/admin/dashboard', component: () => import("@/pages/AdminDashboard.vue") },
    {path: '/student/dashboard', component: () => import("@/pages/StudentDashboard.vue") },
    {path: '/company/dashboard', component: () => import("@/pages/CompanyDashboard.vue") },

  ],
});

export default router
 