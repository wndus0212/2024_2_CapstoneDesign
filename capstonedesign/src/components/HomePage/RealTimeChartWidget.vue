<template>
    <containerBox>
      <BoxTitle>
        실시간 차트
      </BoxTitle>
      <div style="display: flex;">
        <RealTimeChart/>
        <RealTimeChart/>
        <RealTimeChart/>
        <RealTimeChart/>
      </div>
      
    </containerBox>
</template>
<script>
import containerBox from '@/components/Box.vue'
import BoxTitle from '@/components/BoxTitle.vue';
import RealTimeChart from './RealTimeChart.vue';
export default {
    name:'RealTimeChartWidget',
    components:{
        containerBox,
        BoxTitle,
        RealTimeChart
    }
}
</script>
<style>
    
</style>