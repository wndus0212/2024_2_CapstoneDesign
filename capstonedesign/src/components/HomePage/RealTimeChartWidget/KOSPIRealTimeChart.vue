<template>
  <div>
    <apexchart 
      type="line" 
      :options="chartOptions" 
      :series="series" 
    />
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts'
export default {
  conponents:{
    apexchart:VueApexCharts
  },
  data: function() {
    return {
      series: [{
        name: "Desktops",
        data: [10, 41, 35, 51, 49, 62, 69, 91, 148]
      }],
      chartOptions: {
        chart: {
          height: 350,
          type: 'line',
          zoom: {
            enabled: false
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'smooth' // 변경 가능
        },
        title: {
          text: 'KOSPI',
          align: 'left'
        },
        grid: {
          row: {
            colors: ['#f3f3f3', 'transparent'], 
            opacity: 0.5
          }
        },
        xaxis: {
          categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
        }
      }
    };
  }
};
</script>
