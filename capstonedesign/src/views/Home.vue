<template>
  <TopNav/>
  <MainContainer>
    <RealTimeChartWidget/>
    <TreeMapWidget class="small-widget"/>
    <SectionChartWidget class="small-widget"/>
    <StockRankingWidget/>
    <InterestedStockWidget/>
    <ETFWidget/>
    <MyPortfolioWidget/>
  </MainContainer>
</template>

<script>
import TopNav from '../components/Top/Top.vue'
import MainContainer from '@/components/MainContainer.vue';
import RealTimeChartWidget from '@/components/HomePage/RealTimeChartWidget.vue';
import ETFWidget from '@/components/HomePage/ETFWidget.vue';
import InterestedStockWidget from '@/components/HomePage/InterestedStockWidget.vue';
import MyPortfolioWidget from '@/components/HomePage/MyPortfolioWidget.vue';
import SectionChartWidget from '@/components/HomePage/SectionChartWidget.vue';
import StockRankingWidget from '@/components/HomePage/StockRankingWidget.vue';
import TreeMapWidget from '@/components/HomePage/TreeMapWidget.vue';

export default {
  name: 'HomePage',
  components: {
    TopNav,
    MainContainer,
    RealTimeChartWidget,
    ETFWidget,
    InterestedStockWidget,
    MyPortfolioWidget,
    SectionChartWidget,
    StockRankingWidget,
    TreeMapWidget
  }
}
</script>

<style>
  .small-widget{
    width: 18%;
  }
</style>
