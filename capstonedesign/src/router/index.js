import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/Home.vue';
import DetailPage from '../views/Detail.vue';
import MyPage from '../views/Mypage.vue';
import MyPortfolio from '@/views/MyPage/MyPortfolio.vue';
import AddPortfolio from '@/views/MyPage/ManagePortfolio.vue';
import StockDetail from '@/views/StockDetail.vue';

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/Detail', name: 'Detail', component: DetailPage},
  { path: '/detail/:stockCode', name: 'StockDetail', component: StockDetail, props: true},
  { path: '/Mypage', name: 'MyPage', component: MyPage,
    redirect: '/Mypage/MyPortfolio',
    children:[
      {
        path: 'MyPortfolio', 
        component: MyPortfolio
      },
      {
        path: 'AddPortfolio', 
        component: AddPortfolio
      }
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
