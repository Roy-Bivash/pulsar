import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/pages/home/Home.vue';
import ChatPage from '@/pages/chat/Chat.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/chat/:id',
    name: 'Chat',
    component: ChatPage,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;