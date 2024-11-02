<template>
    <div style="width: 100%; display: flex; justify-content: center;">
      <apexchart 
        type="donut" 
        :options="chartOptions" 
        :series="series" 
        :width="250"
        :height="300"
      />
    </div>
  </template>
  
  <script>
  import VueApexCharts from 'vue3-apexcharts';
  
  export default {
    components: {
      apexchart: VueApexCharts // Typo 수정
    },
    data() {
      return {
        // series를 배열 형태로 수정
        series: [44, 55, 13, 43, 22], // Donut chart는 단순 배열 형태로 설정
        chartOptions: { // chartOptions 정의
          chart: {
            type: 'donut', // Donut 차트 타입 설정
            width: 300
          },
          labels: ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'], // labels 정의
          responsive: [{
            breakpoint: 480,
            options: {
              chart: {
                width: 200
              },
              legend: {
                position: 'bottom'
              }
            }
          }],
          legend: {
            show: false
          }
        }
      };
    }
  };
  </script>
  
  <style scoped>
  </style>
  