<template>
  <TopNav/>
  <div style="height: 120px;"></div>
  <MainContainer>
    <TrendingSectorWidget/>
    <RealTimeChartWidget/>
    <StockRankingWidget/> 

    <!--<SectorChartWidget/>-->
    
  </MainContainer>

  
</template>

<script>
import TopNav from '../components/Top/Top.vue'
import MainContainer from '@/components/MainContainer.vue';
import RealTimeChartWidget from '@/components/HomePage/RealTimeChartWidget/RealTimeChartWidget.vue';
//import SectorChartWidget from '@/components/HomePage/SectorChartWidget copy/SectorChartWidget .vue';
import StockRankingWidget from '@/components/HomePage/StockRankingWidget/StockRankingWidget.vue';
import TrendingSectorWidget from '@/components/HomePage/TrendingSector/TrendingSectorWidget.vue';

export default {
  name: 'HomePage',
  components: {
    TopNav,
    MainContainer,
    RealTimeChartWidget,
    StockRankingWidget,
    //SectorChartWidget,
    TrendingSectorWidget
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
