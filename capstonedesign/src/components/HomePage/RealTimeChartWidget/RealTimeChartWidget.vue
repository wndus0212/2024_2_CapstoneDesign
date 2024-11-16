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
        <DAWRealTimeChart :history="KOSPI"/>
        <DAWRealTimeChart :history="KOSDAQ"/>
        <DAWRealTimeChart :history="NASDAQ"/>
        <DAWRealTimeChart :history="DIJ"/>
      </div>
      
    </containerBox>
</template>
<script>
import axios from 'axios';
import containerBox from '@/components/Box.vue'
import BoxTitle from '@/components/BoxTitle.vue';
import DAWRealTimeChart from './RealTimeChart.vue';
import SmallButton from '@/components/SmallButton.vue';
import ButtonContainer from '@/components/ButtonContainer.vue';

export default {
  name:'RealTimeChartWidget',
  components:{
      containerBox,
      BoxTitle,
      DAWRealTimeChart,
      SmallButton,
      ButtonContainer
  },
  data() {
    return {
      DIJ: '',
      KOSPI:'',
      KOSDAQ:'',
      NASDAQ:'',
      SP500:'',

    };
  },
  mounted() {
      console.log("코드:",this.Code);
      this.fetchStockIndexHistory();
  },
  methods: {
      fetchStockIndexHistory() {
          // 선택한 기간과 간격을 URL 파라미터로 전달
          axios
            .get(`http://127.0.0.1:8000/stock/stock_index/DJI/`)
            .then(response => {
              this.DIJ = response.data['output'];
              console.log('dig log: ',this.DIJ)
            })
            .catch(error => console.error("종목 히스토리를 가져오는 데 실패했습니다:", error));

          axios
            .get(`http://127.0.0.1:8000/stock/stock_index/KQ11/`)
            .then(response => {
              this.KOSDAQ = response.data['output'];
            })
            .catch(error => console.error("종목 히스토리를 가져오는 데 실패했습니다:", error));

          axios
            .get(`http://127.0.0.1:8000/stock/stock_index/KS11/`)
            .then(response => {
              this.KOSPI = response.data['output'];
            })
            .catch(error => console.error("종목 히스토리를 가져오는 데 실패했습니다:", error));

          axios
            .get(`http://127.0.0.1:8000/stock/stock_index/IXIC/`)
            .then(response => {
              this.NASDAQ = response.data['output'];
            })
            .catch(error => console.error("종목 히스토리를 가져오는 데 실패했습니다:", error));

          axios
            .get(`http://127.0.0.1:8000/stock/stock_index/SP500/`)
            .then(response => {
              this.SP500 = response.data['output'];
            })
            .catch(error => console.error("종목 히스토리를 가져오는 데 실패했습니다:", error));
      }
  }
  
}
</script>
<style>
    
</style>