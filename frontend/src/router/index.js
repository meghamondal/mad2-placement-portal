import { createRouter, createWebHistory } from 'vue-router'

import Landing from '@/pages/Landing.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: "/", component: Landing},
    {path: '/login', component: () => import("@/pages/Login.vue") },
    {path: '/register', component: () => import("@/pages/Register.vue") },
  ],
});

export default router
