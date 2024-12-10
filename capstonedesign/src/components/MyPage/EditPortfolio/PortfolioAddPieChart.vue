<template>
  <div style="display: flex; justify-content: center;">
    <div>
      <apexchart 
        type="donut" 
        :options="chartOptions" 
        :series="series" 
        :width="450"
        :height="400"
      />
    </div>
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts';
import axios from 'axios';

export default {
  components: {
    apexchart: VueApexCharts
  },
  props: {
    addedStock: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      stocks: [], // 주식 데이터
      series: [], // 주식 가격 비율
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
        dataLabels: {
          enabled: true, // 데이터 레이블 표시
        },
        legend: {
          position: 'top', // 범례 위치
        },
      },
      exchangeRate: 1, // 기본 환율 (1:1로 설정)
    };
  },
  mounted() {
    // 컴포넌트가 마운트되면 addedStock 데이터를 stocks에 할당
    this.stocks = this.addedStock;
    this.fetchCurrencyRate(); // 환율 가져오기
  },
  watch: {
    addedStock(newStock) {
      this.stocks = newStock;
      this.updateChartData(); // addedStock이 업데이트되면 차트 데이터 업데이트
    },
  },
  methods: {
    // 환율 가져오기
    async fetchCurrencyRate() {
      try {
        // API 호출하여 환율 가져오기
        const response = await axios.get('http://127.0.0.1:8000/stock/currency/');
        this.exchangeRate = response.data.output[0]['Close']; // 환율 적용
        this.updateChartData(); // 환율이 적용되었으므로 차트 데이터 업데이트
      } catch (error) {
        console.error("환율 가져오기 실패:", error);
      }
    },
    
    // 차트 데이터 업데이트
    updateChartData() {
      // 먼저 환율을 적용하여 가격을 변환한 후 totalPrice 계산
      const convertedStocks = this.stocks.map(stock => {
        let price = parseFloat(stock.prices);
        // 심볼이 .KQ나 .KS로 끝나지 않으면 환율 적용
        if (!stock.symbols.endsWith('.KQ') && !stock.symbols.endsWith('.KS')) {
          price *= this.exchangeRate;
          
        }
        price *= stock.allocation
        return { ...stock, convertedPrice: price }; // 환율이 적용된 가격 추가
      });

      // 환율 적용된 가격으로 totalPrice 계산
      const totalPrice = convertedStocks.reduce((sum, stock) => sum + stock.convertedPrice, 0);
      
      // 비율 계산
      this.series = convertedStocks.map(stock => (stock.convertedPrice / totalPrice) * 100);
      
      // 차트의 라벨을 종목 이름으로 설정
      this.chartOptions.labels = convertedStocks.map(stock => stock.names); 
    },
  },
};
</script>

<style scoped>
/* 스타일링 관련 코드 */
</style>
