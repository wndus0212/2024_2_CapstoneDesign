<template>
      <apexchart 
      type="treemap" 
      :options="chartOptions" 
      :series="series" 
      :width="300" 
      :height="290"/>
  </template>
  
  <script>
  import VueApexCharts from 'vue3-apexcharts'
  export default{
    name: 'TreeMapWidget',
    components: {
        apexchart:VueApexCharts
    },
    data() {
      return {
        series: [
          {
            data: [
              { x: 'INTC', y: 1.2 },
              { x: 'GS', y: 0.4 },
              { x: 'CVX', y: -1.4 },
              { x: 'GE', y: 2.7 },
              { x: 'CAT', y: -0.3 },
              { x: 'RTX', y: 5.1 },
              { x: 'CSCO', y: -2.3 },
              { x: 'JNJ', y: 2.1 },
              { x: 'PG', y: 0.3 },
              { x: 'TRV', y: 0.12 },
              { x: 'MMM', y: -2.31 },
              { x: 'NKE', y: 3.98 },
              { x: 'IYT', y: 1.67 }
            ]
          }
        ],
        chartOptions: {
          legend: {
            show: false
          },
          chart: {
            height: 350,
            type: 'treemap',
            toolbar:{
                    show:false
                },
          },
          dataLabels: {
            enabled: true,
            style: {
              fontSize: '12px'
            },
            formatter: function(text, op) {
              return [text, op.value];
            },
            offsetY: -4
          },
          plotOptions: {
            treemap: {
              enableShades: true,
              shadeIntensity: 0.5,
              reverseNegativeShade: true,
              colorScale: {
                ranges: [
                  {
                    from: -6,
                    to: 0,
                    color: '#CD363A' // 부정적인 값에 대한 색상
                  },
                  {
                    from: 0.001,
                    to: 6,
                    color: '#52B12C' // 긍정적인 값에 대한 색상
                  }
                ]
              }
            },
          },
        }
      };
    }
  };
  </script>
  
  <style>
  /* 필요에 따라 스타일 추가 */
  </style>
  