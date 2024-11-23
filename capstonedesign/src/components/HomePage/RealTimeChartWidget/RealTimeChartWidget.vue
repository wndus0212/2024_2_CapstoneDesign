<template>
  <containerBox>
    <BoxTitle>
      주가지수
    </BoxTitle>

    <!-- 주가지수 선택 -->
    <SelectBox 
      :options="SelectIndex" 
      v-model="selectedIndex" 
      width="200px" 
      @change="updateChartData" />

    <div style="display: flex;">
      <!-- 기간 선택 -->
      <SelectBox 
        :options="SelectPeriod" 
        v-model="selectedPeriod" 
        width="150px" 
        @change="updateChartData" />

      <!-- 간격 선택 -->
      <SelectBox 
        :options="SelectInterval" 
        v-model="selectedInterval" 
        width="150px" 
        @change="updateChartData" />
    </div>
    
    <div v-if="chartData" style="display: flex; justify-content: space-between; flex-wrap: wrap">
      <!-- 조건부 렌더링: chartData가 있을 경우에만 차트를 렌더링 -->
      <RealTimeChart 
        :history="chartData" 
        :chartname="selectedIndex?.label || 'No Selection'"/>
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
      selectedIndex: '^KS11', // 기본 선택된 옵션 (label과 value로 유지)
      selectedPeriod: '1mo', // 기본 선택 기간
      selectedInterval: '1d', // 기본 선택 간격
      chartData: null, // 차트 데이터
      SelectIndex: [
        { label: 'KOSPI', value: '^KS11' },
        { label: 'KOSDAQ', value: '^KQ11' },
        { label: 'SP500', value: '^GSPC' },
        { label: 'NASDAQ', value: '^IXIC' },
        { label: 'DJI', value: '^DJI' }
      ],
      SelectPeriod: [
        { label: '1개월', value: '1mo' },
        { label: '6개월', value: '6mo' },
        { label: '1년', value: '1y' },
        { label: '5년', value: '5y' },
        { label: '전체', value: 'max' }
      ],
      SelectInterval: [
        { label: '일봉', value: '1d' },
        { label: '주봉', value: '1wk' },
        { label: '월봉', value: '1mo' }
      ]
    };
  },
  watch: {
    selectedIndex() {
      this.updateChartData();
    },
    selectedPeriod() {
      this.updateChartData();
    },
    selectedInterval() {
      this.updateChartData();
    }
  },
  mounted() {
    this.updateChartData(); // 초기 데이터 로드
  },
  methods: {
    updateChartData() {
      console.log("Updating chart data:", {
        selectedIndex: this.selectedIndex,
        selectedPeriod: this.selectedPeriod,
        selectedInterval: this.selectedInterval
      });

      if (this.selectedIndex && this.selectedIndex) {
        this.fetchStockIndexHistory();
      } else {
        console.warn("No valid selected index. Chart data not updated.");
        this.chartData = null;
      }
    },
    fetchStockIndexHistory() {
      const selectedIndexValue = this.selectedIndex; // selectedIndex의 value 값
      axios
        .get(`http://127.0.0.1:8000/stock/index/index/${selectedIndexValue}/`, {
          params: {
            start: "",
            end: "",
            period: this.selectedPeriod,
            interval: this.selectedInterval,
          },
        })
        .then(response => {
          // API 응답에서 차트 데이터 처리
          this.chartData = response.data['output'] || null;
        })
        .catch(error => console.error("종목 히스토리를 가져오는 데 실패했습니다:", error));
    }
  }
};
</script>

<style>
/* 스타일 추가 가능 */
</style>
