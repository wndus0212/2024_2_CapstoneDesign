<template>
    <div>
      <apexchart 
        type="line" 
        :options="chartOptions" 
        :series="series" 
        :width="650"
        :height="400"
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
                    return (val / 1000000).toFixed(0);
                    },
                },
                title: {
                    text: 'Price'
                },
            },
            tooltip: {
                shared: false,
                y: {
                    formatter: function (val) {
                    return (val / 1000000).toFixed(0)
                    }
                }
            },
            legend:{
                show: true,
                position: 'bottom'
            }
        }
      };
    }
  };
  </script>
  