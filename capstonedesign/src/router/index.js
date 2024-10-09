import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/Home.vue';
import DetailPage from '../views/Detail.vue';
import ContentsPage from '../views/Contents.vue';
import MyPage from '../views/Mypage.vue';

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/Detail', name: 'Detail', component: DetailPage },
  { path: '/Contents', name: 'Contents', component: ContentsPage },
  { path: '/Mypage', name: 'MyPage', component: MyPage}
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
