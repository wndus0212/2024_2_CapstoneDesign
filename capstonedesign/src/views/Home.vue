<template>
  <TopNav/>
  <div style="height: 120px;"></div>
  <MainContainer>
    <div>
      <MyPortfolioWidget/>
      <StockRankingWidget/> 
    </div>
    
    <div>
      <RealTimeChartWidget/>
         
    </div>
  </MainContainer>

  
</template>

<script>
import TopNav from '../components/Top/Top.vue'
import MainContainer from '@/components/MainContainer.vue';
import RealTimeChartWidget from '@/components/HomePage/RealTimeChartWidget/RealTimeChartWidget.vue';
import MyPortfolioWidget from '@/components/HomePage/MyPortfolioWidget/MyPortfolioWidget.vue';
import StockRankingWidget from '@/components/HomePage/StockRankingWidget/StockRankingWidget.vue';

export default {
  name: 'HomePage',
  components: {
    TopNav,
    MainContainer,
    RealTimeChartWidget,
    MyPortfolioWidget,
    StockRankingWidget,
  },
  data() {
    return {

    };
  },
  created() {
  },
  methods: {

  },
}
</script>

<style>
  .small-widget{
    width: 330px;
    height: 350px;
  }
</style>
