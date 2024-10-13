<template>
    <div>
      <apexchart 
        :options="chartOptions" 
        :series="series" 
        width="700" 
        height="400" 
      />
    </div>
  </template>
  
  <script>
  import VueApexCharts from 'vue3-apexcharts'
  
  export default {
    components: {
      apexchart: VueApexCharts
    },
    data() {
      return {
        series: [
          {
            name: 'Net Profit',
            data: [44, 55, 57, 56, 61, 58, 63, 60, 66]
          },
          {
            name: 'Revenue',
            data: [76, 85, 101, 98, 87, 105, 91, 114, 94]
          },
          {
            name: 'Free Cash Flow',
            data: [35, 41, 36, 26, 45, 48, 52, 53, 41]
          }
        ],
        chartOptions: {
          chart: {
            height: 350,
            width: 500,
            type: 'bar',  // 바 차트로 설정
          },
          stroke: {
            width: [3, 1]
          },
          yaxis: {
            labels: {
              formatter: function (val) {
                return val.toFixed(0); // 포맷 간단화
              },
            },
            title: {
              text: 'Price'
            },
          },
          xaxis: {
            categories: ['2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028'], // 임의로 설정 (datetime 대신 카테고리로 변경)
          },
          tooltip: {
            shared: false,
            y: {
              formatter: function (val) {
                return val.toFixed(0) // 포맷 간단화
              }
            }
          },
          legend: {
            show: true,
            position: 'bottom'
          },
          plotOptions: {
            bar: {
              horizontal: false,
              columnWidth: '55%',
              endingShape: 'rounded'
            },
          },
        }
      };
    }
  };
  </script>
  