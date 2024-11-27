<template>
  <containerBox>
    <BoxTitle>
      주가지수
    </BoxTitle>

    <div style="display: flex;">
      <!-- 기간 선택 -->
      <SelectBox 
        :options="SelectPeriod" 
        v-model="selectedPeriod" 
        width="150px" 
        @change="updateChartData" />
    </div>
    
    <div v-if="chartData" style="display: flex; justify-content: space-between; flex-wrap: wrap;">
      <!-- 조건부 렌더링: chartData가 있을 경우에만 차트를 렌더링 -->
      <div 
        v-for="(data, index) in chartData" 
        :key="index" 
        style="flex: 1 1 calc(50% - 20px); margin: 10px;">
        <RealTimeChart 
          :history="data.history" 
          :chartname="data.label"
          :current="data.current" />
      </div>
    </div>
    <div v-else style="text-align: center; color: gray; margin-top: 20px;">
      차트 데이터를 선택하세요.
    </div>
  </containerBox>
</template>

<script>
import axios from 'axios';
import containerBox from '@/components/Box.vue';
import BoxTitle from '@/components/BoxTitle.vue';
import RealTimeChart from './RealTimeChart.vue';
import SelectBox from '@/components/SelectBox.vue';

export default {
  name: 'RealTimeChartWidget',
  components: {
    containerBox,
    BoxTitle,
    RealTimeChart,
    SelectBox
  },
  data() {
    return {
      selectedPeriod: '1mo', // 기본 선택 기간
      chartData: null, // 차트 데이터
      stockIndices: [
        { label: 'KOSPI', value: '^KS11' },
        { label: 'KOSDAQ', value: '^KQ11' },
        { label: 'SP500', value: '^GSPC' },
        { label: 'NASDAQ', value: '^IXIC' },
        { label: 'DJI', value: '^DJI' },
      ],
      SelectPeriod: [
        { label: '1개월', value: '1mo' },
        { label: '6개월', value: '6mo' },
        { label: '1년', value: '1y' },
        { label: '5년', value: '5y' },
        { label: '전체', value: 'max' }
      ]
    };
  },
  watch: {
    selectedPeriod: 'updateChartData'
  },
  mounted() {
    this.updateChartData(); // 초기 데이터 로드
  },
  methods: {
    updateChartData() {
      console.log("Updating chart data:", { selectedPeriod: this.selectedPeriod });
      this.fetchAllIndexData();
    },
    fetchAllIndexData() {
      const requests = this.stockIndices.map(index => {
        return axios
          .get(`http://127.0.0.1:8000/stock/index/index/${index.value}/`, {
            params: {
              period: this.selectedPeriod,
              interval: '1d',
            },
          })
          .then(response => ({
            label: index.label,
            history: response.data.output['Stock History'] || [],
            current: response.data.output['Current Price'] || 0
          }))
          .catch(error => {
            console.error(`Error fetching data for ${index.label}:`, error);
            return { label: index.label, history: [], current: 0 };
          });
      });

      Promise.all(requests)
        .then(results => {
          this.chartData = results; // 모든 주가지수 데이터를 저장
        })
        .catch(error => {
          console.error('Error fetching all index data:', error);
          this.chartData = null;
        });
    }
  }
};
</script>

<style>
/* 필요시 스타일 추가 */
</style>
