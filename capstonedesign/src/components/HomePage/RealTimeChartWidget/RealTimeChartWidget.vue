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
        <DAWRealTimeChart history="history"/>
      </div>
      
    </containerBox>
</template>
<script>
import axios from 'axios';
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
  },
  data() {
    return {
      stock: '',
      history: '',
      selectedPeriod: '1mo', // 기본값
      selectedInterval: '1d' // 기본값
    };
  },
  mounted() {
      console.log("코드:",this.Code);
      this.fetchStockDetails();
      this.fetchStockHistory();
  },
  methods: {
      fetchStockHistory() {
          // 선택한 기간과 간격을 URL 파라미터로 전달
          axios
              .get(`http://127.0.0.1:8000/stock/history/^KS11/`, {
                  params: {
                      start: '',
                      end: '',
                      period: this.selectedPeriod,
                      interval: this.selectedInterval
                  }
              })
              .then(response => {
                  this.history = response.data['output'];
              })
              .catch(error => console.error("종목 히스토리를 가져오는 데 실패했습니다:", error));
      }
  }
}
</script>
<style>
    
</style>