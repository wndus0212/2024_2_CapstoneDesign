<template>
    <div>
      <apexchart 
        type="line" 
        :options="chartOptions" 
        :series="series" 
        :width="600"
        :height="400"
      />
    </div>
  </template>
  
  <script>
  import VueApexCharts from 'vue3-apexcharts';
  
  export default {
    components: {
      apexchart: VueApexCharts
    },
    props: {
      movingAveragedata: {
        type: Array,
        required: true
      }
    },
    data() {
      return {
        series: [],
        chartOptions: {
          chart: {
            height: 350,
            width: 500,
            type: 'line',
          },
          xaxis: {
            type: 'datetime',
          },
          yaxis: {
            opposite: true,  // 반대쪽에 위치
            labels: {
              formatter: function (value) {
                value.toFixed(0);
                return value.toLocaleString(); // 1000 단위마다 쉼표 추가
              }
            }
          },
          tooltip: {
            shared: false,
          },
          legend: {
            show: true,
            position: 'bottom'
          },
          stroke: {
            width: 1, // 선의 굵기를 1로 설정 (얇게)
          }
        }
      };
    },
    watch: {
      movingAveragedata: {
        handler(newHistory) {
          // 데이터가 배열 형식인지 확인하고 출력
          console.log("Received ma data:", newHistory);
  
          const historyArray = newHistory && Array.isArray(newHistory) ? newHistory : [];
          const totalItems = historyArray.length;
          if (historyArray.length > 0) {
            // MA_3와 MA_5 데이터가 있는지 확인
            const ma3Data = historyArray.map((entry, index) => ({
              x: new Date(new Date().setDate(new Date().getDate() - totalItems + index)),
              y: entry.MA_3 || null // MA_3 값이 없다면 null로 처리
            }));
  
            const ma5Data = historyArray.map((entry, index) => ({
              x: new Date(new Date().setDate(new Date().getDate() - totalItems + index)),
              y: entry.MA_5 || null // MA_5 값이 없다면 null로 처리
            }));
  
            // series 배열에 MA_3와 MA_5를 추가
            this.series = [
              {
                name: 'MA_3',
                type: 'line',
                data: ma3Data,
                color: '#FF5733' // MA_3 선의 색상
              },
              {
                name: 'MA_5',
                type: 'line',
                data: ma5Data,
                color: '#33FF57' // MA_5 선의 색상
              }
            ];
          } else {
            console.error("Error: history 데이터가 비어있습니다.");
            this.series = [];
          }
        },
        immediate: true
      }
    }
  };
  </script>
  