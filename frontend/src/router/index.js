import { createRouter, createWebHistory } from 'vue-router'

import Landing from '@/pages/Landing.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: "/", component: Landing},
    {path: '/login', component: () => import("@/pages/Login.vue") },
    {path: '/register', component: () => import("@/pages/Register.vue") },
    {path: '/admin/dashboard', component: () => import("@/pages/AdminDashboard.vue") },
    {path: '/student/dashboard', component: () => import("@/pages/StudentDashboard.vue") },
    {path: '/company/dashboard', component: () => import("@/pages/CompanyDashboard.vue") },
    {path: '/register', component: () => import("@/pages/Register.vue") },
    {path: '/student/register', component: () => import("@/pages/StudReg.vue") },
    {path: '/company/register', component: () => import("@/pages/CompReg.vue") },
    {path: '/pendingComp', component: () => import("@/pages/PendingComp.vue") },
    {path: '/pendingPd', component: () => import("@/pages/PendingPd.vue") },
    {path: '/pd_list', component: () => import("@/pages/PdList.vue") },
    {path: '/app_list', component: () => import("@/pages/AppList.vue") },
    {path: '/short_app_list', component: () => import("@/pages/ShortAppList.vue") },
    {path: '/app_intw', component: () => import("@/pages/InterviewSchedule.vue") },
    {path: '/student/pd_list', component: () => import("@/pages/StudPdlist.vue") },
    {path: '/student/app_list', component: () => import("@/pages/StudAppStatus.vue") },
    {path: '/intw_details', component: () => import("@/pages/StudIntwDetails.vue") },
    {path: '/offer_letter', component: () => import("@/pages/StudOfferLetter.vue") },

  ],
});

export default router
 