<template>
    <containerBox>
      <BoxTitle>
        실시간 차트
      </BoxTitle>
      <div style="display:flex; gap: 10px">
        <SmallButton>
          종합주가지수
        </SmallButton>
        <SmallButton>
          원자재
        </SmallButton>
        <SmallButton>
          채권
        </SmallButton>
      </div>
      <div style="display: flex;">
        <KOSPIChart/>

      </div>
      
    </containerBox>
</template>
<script>
import containerBox from '@/components/Box.vue'
import BoxTitle from '@/components/BoxTitle.vue';
import KOSPIChart from './KOSPIRealTimeChart.vue';

import SmallButton from '@/components/SmallButton.vue';

export default {
    name:'RealTimeChartWidget',
    components:{
        containerBox,
        BoxTitle,
        KOSPIChart,

        SmallButton
    }
}
</script>
<style>
    
</style>