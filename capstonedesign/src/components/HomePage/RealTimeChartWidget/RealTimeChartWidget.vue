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
        <KOSDAQRealTimeChart/>
        <NASDAQRealTimeChart/>
        <DAWRealTimeChart/>
      </div>
      
    </containerBox>
</template>
<script>
import containerBox from '@/components/Box.vue'
import BoxTitle from '@/components/BoxTitle.vue';
import KOSPIChart from './KOSPIRealTimeChart.vue';
import KOSDAQRealTimeChart from './KOSDAQRealTimeChart.vue';
import NASDAQRealTimeChart from './NASDAQRealTimeChart.vue';
import DAWRealTimeChart from './DAWRealTimeChart.vue';
import SmallButton from '@/components/SmallButton.vue';

export default {
    name:'RealTimeChartWidget',
    components:{
        containerBox,
        BoxTitle,
        KOSPIChart,
        KOSDAQRealTimeChart,
        NASDAQRealTimeChart,
        DAWRealTimeChart,
        SmallButton
    }
}
</script>
<style>
    
</style>