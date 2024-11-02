<template>
    <containerBox>
      <BoxTitle>
        내 포트폴리오
      </BoxTitle>

      <select style="margin: 10px 0px; height: 35px; width: 180px; font-size: 20px;">
        <option>포트폴리오 1</option>
      </select>

      <div style="display: flex;">
        <div>
          <div style="font-size: 24px; margin-top: 20px;">
            위험 중립형
          </div>
          <div style="display: flex; font-size: 35px;">
            <div>
              10,000,000
            </div>
            <div style="font-size: 15px;">
              (+0.05%)
            </div>
          </div>
        </div>
        <PortfolioPieChartSmall/>
      </div>
      <PortfolioChartSmall/>
      <div style="border-radius: 5px; border: 1px black solid; padding: 5px;">

      </div>
    </containerBox>
</template>
<script>
import containerBox from '@/components/Box.vue'
import BoxTitle from '@/components/BoxTitle.vue';
import PortfolioPieChartSmall from './PortfolioPieChartSmall.vue';
import PortfolioChartSmall from './PortfolioChartSmall.vue';

export default {
    name:'MyPortfolioWidget',
    components:{
        containerBox,
        BoxTitle,
        PortfolioPieChartSmall,
        PortfolioChartSmall,
    }
}
</script>
<style>
    
</style>