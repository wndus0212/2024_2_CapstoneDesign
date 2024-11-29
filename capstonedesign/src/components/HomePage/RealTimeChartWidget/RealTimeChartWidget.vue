<template>
  <Box width="1280px">
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
    
    <div v-if="chartData" style="display: flex; justify-content: space-between; flex-wrap: nowrap;">
      <!-- 조건부 렌더링: chartData가 있을 경우에만 차트를 렌더링 -->
      <div 
        v-for="(data, index) in chartData" 
        :key="index" 
        style="display: flex; margin: 10px;">
        <RealTimeChart 
          :history="data.history" 
          :chartname="data.label"
          :diff="data.diff"
          :period="selectedPeriod" />

      </div>
    </div>
    <div v-else style="text-align: center; color: gray; margin-top: 20px;">
      차트 데이터 로딩중.
    </div>
  </Box>
</template>

<script>
import axios from 'axios';
import Box from '@/components/Box.vue';
import BoxTitle from '@/components/BoxTitle.vue';
import RealTimeChart from './RealTimeChart.vue';
import SelectBox from '@/components/SelectBox.vue';

export default {
  name: 'RealTimeChartWidget',
  components: {
    Box,
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
        { label: '1일', value: '1d' },
        { label: '1개월', value: '1mo' },
        { label: '1년', value: '1y' },
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
        // history 데이터 요청
        const historyRequest = axios.get(`http://127.0.0.1:8000/stock/index/index/${index.value}/`, {
          params: {
            period: this.selectedPeriod,
            interval: '1d',
          },
        }).then(response => {
          if (!response.data.output) {
            console.log(response)
            throw new Error(`Output is missing for ${index.label}`);
          }
          return {
            label: index.label,
            history: response.data.output || [],
          };
          
        });

        // current 데이터 요청 (다른 API에서)
        const diffRequest = axios.get(`http://127.0.0.1:8000/stock/stock_diff/${index.value}/`) // 예시 URL
          .then(response => {
            if (!response.data) {
              console.log(response);
              throw new Error(`Current price missing for ${index.label}`);
              
            }
            console.log(response.data.output)
            return response.data.output || 0;
          });

        // 두 요청을 병합하여 처리
        return Promise.all([historyRequest, diffRequest]).then(([historyData, currentPrice]) => {
          return {
            label: index.label,
            history: historyData.history,
            diff: currentPrice,
          };
        }).catch(error => {
          console.error(`Error fetching data for ${index.label}:`, error);
          return { label: index.label, history: [], diff: 0 }; // 실패 시 기본값
        });
      });

      Promise.allSettled(requests)
        .then(results => {
          this.chartData = results
            .filter(result => result.status === 'fulfilled')
            .map(result => result.value);

          if (this.chartData.length === 0) {
            console.warn('모든 요청이 실패했습니다.');
            this.chartData = null;
          }
        })
        .catch(error => {
          console.error('Error processing index data:', error);
          this.chartData = null;
        });

        console.log(this.chartData)
    }


  }
};
</script>

<style>
/* 필요시 스타일 추가 */
</style>
