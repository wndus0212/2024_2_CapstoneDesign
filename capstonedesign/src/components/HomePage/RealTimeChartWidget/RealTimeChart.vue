<template>
  <div style="border-radius: 5px; border: 1px black solid; padding: 5px; margin-bottom: 5px;">
    <apexchart 
      type="line" 
      :options="chartOptions" 
      :series="series" 
      :width="600"
      :height="600"
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
    history: {
      type: Array,
      required: true
    },
    chartname:{
      type: String,
      required:true
    }
  },
  data() {
    return {
      series: [],
      chartOptions: {
        chart: {
          height: 150,
          width: 230,
          type: 'line',
          sparkline: {
            enabled: false
          },
          toolbar: {
            show: true,
          },
        },
        tooltip: {
            enabled: true  // 툴팁 숨기기
        },
        legend: {
          show: true,
          position: 'bottom'
        },
        title:{
          text: this.chartname
        },
        xaxis: {
          type: 'datetime'
        },
        yaxis: {
          labels: {
            formatter: (value) => {
              // 소수점 이하 자리수를 제거
              return Math.floor(value); 
            }
          }
        }
      }
    };
  },
  watch: {
    history: {
      handler(newHistory) {
        const historyArray = newHistory && Array.isArray(newHistory) ? newHistory : [];
        const totalItems = historyArray.length;
        
        if (historyArray.length > 0) {
          this.series = [
            {
              name: 'line',
              type: 'line',
              data: historyArray.map((entry, index) => ({
                x: new Date(new Date().setDate(new Date().getDate() - totalItems + index)),
                y: [entry.Open, entry.High, entry.Low, entry.Close], // 시가, 고가, 저가, 종가
              }))
            },

          ];
        } else {
          console.error("Error: history 데이터의 output이 비어있거나 존재하지 않습니다.", newHistory);
          this.series = [];
        }
      },
      immediate: true
    }
  }
};
</script>
