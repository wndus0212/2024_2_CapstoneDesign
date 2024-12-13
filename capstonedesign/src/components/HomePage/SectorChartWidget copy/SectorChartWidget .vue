<template>
  <containerBox>
    <BoxTitle>
      섹터 지수
    </BoxTitle>

    <!-- 버튼 컨테이너 -->
    <div style="display: flex; gap: 10px; margin-top: 10px;">
      <!-- 기간 선택 -->
      <SelectBox 
        :options="SelectPeriod" 
        v-model="selectedPeriod" 
        :width="150" />

      <!-- 간격 선택 -->
      <SelectBox 
        :options="SelectInterval" 
        v-model="selectedInterval" 
        :width="150" />
    </div>

    <!-- 로딩 중 표시 -->
    <div v-if="loading" style="text-align: center; color: gray; margin-top: 20px;">
      데이터 로딩 중입니다...
    </div>

    <!-- 차트 표시 -->
    <div v-if="!loading && chartData" style="display: flex; justify-content: space-between; flex-wrap: wrap; margin-top: 20px;">
      <RealTimeChart 
        :history="chartData" />
    </div>

    <div v-if="!loading && !chartData" style="text-align: center; color: gray; margin-top: 20px;">
      차트 데이터를 선택하세요.
    </div>
  </containerBox>
</template>

<script>
import axios from 'axios';
import containerBox from '@/components/Box.vue';
import BoxTitle from '@/components/BoxTitle.vue';
import RealTimeChart from './SectorChart.vue';
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
      selectedIndex: 'SPDR', // 기본 선택된 옵션
      selectedPeriod: '1mo', // 기본 선택 기간
      selectedInterval: '1d', // 기본 선택 간격
      chartData: null, // 차트 데이터
      loading: false, // 로딩 상태
      SelectPeriod: [
        { label: '1개월', value: '1mo' },
        { label: '6개월', value: '6mo' },
        { label: '1년', value: '1y' },
        { label: '5년', value: '5y' },
      ],
      SelectInterval: [
        { label: '일봉', value: '1d' },
        { label: '주봉', value: '1wk' },
        { label: '월봉', value: '1mo' }
      ]
    };
  },
  watch: {
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
    async updateChartData() {
      this.loading = true; // 로딩 상태 활성화
      this.chartData = null; // 이전 데이터 초기화

      const params = {
        period: this.selectedPeriod,
        interval: this.selectedInterval,
      };


      try {
        const response = await axios.get(`https://port-0-capstonedesign-m3vkxnzga0885b97.sel4.cloudtype.app/stock/index/sector/SPDR/`, { params });
        this.chartData = response.data['output'] || null;
      } catch (error) {
        console.error('차트 데이터를 가져오는 데 실패했습니다:', error);
        this.chartData = null;
      } finally {
        this.loading = false; // 로딩 상태 비활성화
      }

    }
  }
};
</script>

<style>
/* 컨테이너 스타일 */
.containerBox {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}

/* 버튼 컨테이너 스타일 */
.ButtonContainer {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

/* 로딩 상태 텍스트 */
div[style*="text-align: center; color: gray"] {
  font-size: 16px;
  font-weight: bold;
}
</style>
