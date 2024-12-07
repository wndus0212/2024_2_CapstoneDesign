<template>
  <div>
    <apexchart 
      type="donut" 
      :options="chartOptions" 
      :series="series" 
      :width="450"
      :height="400"
    />
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts';

export default {
  components: {
    apexchart: VueApexCharts
  },
  props: {
    stocks: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      series: [], // 주식 비율 데이터
      chartOptions: { // Donut 차트 옵션
        chart: {
          type: 'donut',
        },
        labels: [], // 종목 이름
        responsive: [
          {
            breakpoint: 480,
            options: {
              chart: {
                width: 200,
              },
              legend: {
                position: 'bottom',
              },
            },
          },
        ],
        legend: {
          position: 'top', // 범례 위치
        },
      },
    };
  },
  watch: {
    stocks: {
      immediate: true,
      handler(newStocks) {
        // stocks 데이터를 기반으로 series와 labels를 생성
        this.series = newStocks.map(stock => stock.allocation); // 주식 수량
        this.chartOptions.labels = newStocks.map(stock => stock.symbol); // 주식 이름
      },
    },
  },
};
</script>

<style scoped>
/* 필요에 따라 스타일 추가 */
</style>
