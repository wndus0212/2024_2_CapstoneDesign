<template>
    <containerBox>
      <BoxTitle>
        내 포트폴리오
      </BoxTitle>
      <div style="display: flex;">
        <div>
          <div>
            위험 중립형
          </div>
          <div style="display: flex;">
            <div>
              10,000,000
            </div>
            <div>
              (+0.05%)
            </div>
          </div>
        </div>
        <PortfolioPieChart/>
      </div>
      <PortfolioChart/>
      <Box/>
    </containerBox>
</template>
<script>
import containerBox from '@/components/Box.vue'
import BoxTitle from '@/components/BoxTitle.vue';
import PortfolioPieChart from '@/components/MyPage/PortfolioPieChart.vue';
import PortfolioChart from '@/components/MyPage/PortfolioChart.vue';
import Box from '@/components/Box.vue';

export default {
    name:'MyPortfolioWidget',
    components:{
        containerBox,
        BoxTitle,
        PortfolioPieChart,
        PortfolioChart,
        Box
    }
}
</script>
<style>
    
</style>