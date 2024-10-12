<template>
  <div style="border-radius: 5px; border: 1px black solid; padding: 5px;">
    <apexchart 
      type="line" 
      :options="chartOptions" 
      :series="series" 
      :width="150"
      :height="230"
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
        title: {
          text: 'KOSDAQ',
          align: 'left',
          offsetY: 10,
          style:{
            fontSize: '10px',
          }
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
