<template>
    <containerBox>
      <BoxTitle>
        실시간 차트
      </BoxTitle>
      <ButtonContainer>
        <SmallButton text="종합주가지수"/>
        <SmallButton text="원자재"/>
        <SmallButton text="채권"/>
      </ButtonContainer>
      <div style="display: flex; justify-content: space-between;">
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
import ButtonContainer from '@/components/ButtonContainer.vue';

export default {
    name:'RealTimeChartWidget',
    components:{
        containerBox,
        BoxTitle,
        KOSPIChart,
        KOSDAQRealTimeChart,
        NASDAQRealTimeChart,
        DAWRealTimeChart,
        SmallButton,
        ButtonContainer
    }
}
</script>
<style>
    
</style>