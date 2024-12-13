<template>
  <div>
    <SelectBox :options="periodOptions" v-model="selectedPeriod"/>
    <SmallButton text="백테스트 시작" @click="fetchBacktest"/>
    <!-- 로딩 중 메시지 -->
    <div v-if="loading">로딩 중...</div> 
    <!-- 로딩이 끝났으면 차트 표시 -->
    <div v-else>
      
      <apexchart v-if="series.length > 0"
        type="line" 
        :options="chartOptions" 
        :series="series" 
        :width="850"
        :height="400"
      />
    </div>
  </div>
</template>

<script>
import SmallButton from '@/components/SmallButton.vue';
import axios from 'axios';
import VueApexCharts from 'vue3-apexcharts';
import SelectBox from '../SelectBox.vue';

export default {
  components: {
    SmallButton,
    apexchart: VueApexCharts,
    SelectBox
  },
  props: {
    portfolioId: {
      type: Number,
      required: true,
    }
  },
  data() {
    return {
      series: [], // 차트 데이터
      periodOptions: [
          { label: '1년', value: '1y' },
          { label: '5년', value: '5y' },
          { label: '전체', value: 'max' },
      ],
      selectedPeriod: "5y",
      chartOptions: {
        chart: {
          type: 'line',
          height: 350,
          zoom: {
            type: 'x',
            enabled: true,
            autoScaleYaxis: true
          },
          toolbar: {
            autoSelected: 'zoom'
          },
        },
        dataLabels: {
          enabled: false
        },
        markers: {
          size: 0,
        },
        title: {
          text: 'Portfolio Value Over Time',
          align: 'left'
        },
        xaxis: {
          type: 'datetime',  // 날짜를 x축으로 설정
        },
        yaxis: {
          labels: {
            formatter: function (val) {
              return (val / 1000000).toFixed(0);  // 단위는 백만 단위로 포맷
            },
          },
          title: {
            text: 'Portfolio Value'
          },
        },
        tooltip: {
          shared: false,
          y: {
            formatter: function (val) {
              return (val / 1000000).toFixed(0);  // 백만 단위로 포맷
            }
          }
        },
        legend: {
          show: true,
          position: 'bottom'
        }
      },
      loading: false, // 로딩 상태 추가
    };
  },
  methods: {
    // 백테스트 데이터 가져오기
    fetchBacktest() {
      const token = localStorage.getItem("token");

      // 로딩 시작
      this.loading = true;

      axios.get(`https://web-capstonedesignfront-m3vkxnzga0885b97.sel4.cloudtype.app/portfolio/backtest/${this.portfolioId}/${this.selectedPeriod}/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
      .then(response => {
        const data = response.data.output;
        console.log(data)
        // portfolio_value를 y값으로, date를 x값으로 설정하여 series 데이터 생성
        const seriesData = data.map(item => ({
          x: new Date(item.date).getTime(),  // x는 밀리초 단위의 타임스탬프
          y: item.portfolio_value
        }));

        // ApexCharts의 시리즈에 데이터 추가
        this.series = [{
          name: '포트폴리오 주가(만원)',
          data: seriesData
        }];
        
        console.log("Backtest Data:", data);
      })
      .catch(error => {
        console.error(error);
      })
      .finally(() => {
        // 로딩 종료
        this.loading = false;
      });
    },
    
    // 포트폴리오 주식 목록 가져오기
    fetchPortfolioStocks(newPortfolioId) {
      if (!newPortfolioId) {
        this.portfolioStocks = [];
        return;
      }

      const token = localStorage.getItem("token");
      axios.get(`https://web-capstonedesignfront-m3vkxnzga0885b97.sel4.cloudtype.app/portfolio/portfolios/stock_list/${newPortfolioId}/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
      .then(response => {
        this.portfolioStocks = response.data;
        console.log("Fetched portfolio stocks:", this.addedStock);
      })
      .catch(error => {
        console.error(error);
      });
    },
  }
};
</script>
