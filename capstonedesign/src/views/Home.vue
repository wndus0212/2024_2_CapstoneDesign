<template>
  <TopNav/>
  <div style="height: 120px;"></div>
  <MainContainer>
    <MyPortfolioWidget/>

    <div>
      <div style="display: flex;">
        <TreeMapWidget width="330px" height="350px"/>
        <SectionChartWidget width="330px" height="350px"/>
      </div>
      <RealTimeChartWidget/>
      <StockRankingWidget/>    
    </div>
  </MainContainer>
  <div>
    <h2>주식 데이터</h2>
    <ul>
      <li v-for="stock in stocks" :key="stock.id">
        날짜: {{ stock.stck_bsop_date }}, 시가: {{ stock.stck_oprc }}, 고가: {{ stock.stck_hgpr }},
        저가: {{ stock.stck_lwpr }}, 종가: {{ stock.stck_clpr }}, 거래량: {{ stock.acml_vol }}
      </li>
    </ul>
  </div>
  
</template>

<script>
import axios from 'axios'
import TopNav from '../components/Top/Top.vue'
import MainContainer from '@/components/MainContainer.vue';
import RealTimeChartWidget from '@/components/HomePage/RealTimeChartWidget/RealTimeChartWidget.vue';
import MyPortfolioWidget from '@/components/HomePage/MyPortfolioWidget/MyPortfolioWidget.vue';
import SectionChartWidget from '@/components/HomePage/SectionChartWidget/SectionChartWidget.vue';
import StockRankingWidget from '@/components/HomePage/StockRankingWidget/StockRankingWidget.vue';
import TreeMapWidget from '@/components/HomePage/TreeMapWidget/TreeMapWidget.vue';

export default {
  name: 'HomePage',
  components: {
    TopNav,
    MainContainer,
    RealTimeChartWidget,
    MyPortfolioWidget,
    SectionChartWidget,
    StockRankingWidget,
    TreeMapWidget
  },
  data() {
    return {
      stocks: [],  // API에서 받은 데이터를 저장할 변수
    };
  },
  created() {
    this.fetchStockData();  // 컴포넌트가 생성될 때 데이터 호출
  },
  methods: {
    fetchStockData() {
      axios
        .get("http://127.0.0.1:8000/stock/data/")  // Django에서 제공하는 API 호출
        .then(response => {
          this.stocks = response.data.output;  // 받아온 데이터를 stockData에 저장
        })
        .catch(error => {
          console.error("데이터를 불러오는데 실패했습니다:", error);
        });
    },
  },
}
</script>

<style>
  .small-widget{
    width: 330px;
    height: 350px;
  }
</style>
