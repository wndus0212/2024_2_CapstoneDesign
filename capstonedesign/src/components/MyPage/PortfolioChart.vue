<template>
    <div>
      <apexchart 
        type="area" 
        :options="chartOptions" 
        :series="series" 
        :width="850"
        :height="400"
      />
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import VueApexCharts from 'vue3-apexcharts'
  export default {
    conponents:{
      apexchart:VueApexCharts
    },
    props:{
      portfolioId: {
        type: Number,
        required: true,
      },
    },
    data() {
      return {
        series: [],
        chartOptions: {
            chart: {
                type: 'area',
                stacked: false,
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
                text: 'Stock Price Movement',
                align: 'left'
            },
            yaxis: {
                labels: {
                    formatter: function (val) {
                    return (val);
                    },
                },
                title: {
                    text: 'Price'
                },
            },
            tooltip: {
                shared: false,

            },
            legend:{
                show: true,
                position: 'bottom'
            }
        }
      };
    },
    mounted(){
      this.fetchPortfolioHistory()
    },
    watch: {
      portfolioId() {
        this.fetchPortfolioHistory(); // addedStock이 업데이트되면 차트 데이터 업데이트
      },
    },
    methods:{
      fetchPortfolioHistory() {
        const token = localStorage.getItem("token");

        // 로딩 시작
        this.loading = true;
        console.log(this.portfolioId)
        axios.get(`http://127.0.0.1:8000/portfolio/history/${this.portfolioId}/`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        })
        .then(response => {
          const data = response.data.output;
          // portfolio_value를 y값으로, date를 x값으로 설정하여 series 데이터 생성
          const seriesData = data.map(item => ({
            x: item.Date,  // x는 밀리초 단위의 타임스탬프
            y: Number(item.portfolio_value)
          }));
          console.log(seriesData)
          // ApexCharts의 시리즈에 데이터 추가
          this.series = [{
            name: 'Portfolio Value',
            data: seriesData
          }];
          console.log("chart",seriesData)
        })
        .catch(error => {
          console.error(error);
        })
        .finally(() => {
          // 로딩 종료
          this.loading = false;
        });
      },
    }
  };
  </script>
  