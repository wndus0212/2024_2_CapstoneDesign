<template>
    <div>
      <apexchart 
        type="line" 
        :options="chartOptions" 
        :series="series" 
        :width="300"
        :height="290"
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
            type: 'line',
            zoom: {
              enabled: false
            },
            toolbar: {
              show: false,
             
            },
            sparkline: {
              enabled: true
            },
            parentHeightOffset: 0,
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            width: 1,
          },
          yaxis:{
            labels:{
              style:{
                fontSize:'8px'
              }
            }
          },
          xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
            labels:{
              show:false
            },
          }
        }
      };
    }
  };
  </script>
  