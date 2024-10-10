<template>
    <containerBox>
      <BoxTitle>
        분야별 추세
      </BoxTitle>
      <SectionChart/>
    </containerBox>
</template>
<script>
import containerBox from '@/components/Box.vue'
import BoxTitle from '@/components/BoxTitle.vue';
import SectionChart from './SectionChart.vue';
export default {
    name:'SectionChartWidget',
    components:{
        containerBox,
        BoxTitle,
        SectionChart
    }
}
</script>
<style>
    
</style>