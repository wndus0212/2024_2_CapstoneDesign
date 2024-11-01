<template>
  <TopNav/>
  <div style="height: 120px;"></div>
  <MainContainer>
    <MyPortfolioWidget/>

    <div>
      <div style="display: flex;">
        <TreeMapWidget class="small-widget"/>
        <SectionChartWidget class="small-widget"/>
      </div>
      <RealTimeChartWidget/>
      <StockRankingWidget/>    
    </div>
  </MainContainer>
  
  
</template>

<script>
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
  }
}
</script>

<style>
  .small-widget{
    width: 330px;
    height: 350px;
  }
</style>
