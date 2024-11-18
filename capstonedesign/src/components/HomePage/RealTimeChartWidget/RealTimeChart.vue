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
import VueApexCharts from 'vue3-apexcharts';

export default {
  components: {
    apexchart: VueApexCharts
  },
  props: {
    history: {
      type: Array,
      required: true
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
            enabled: true
          },
          toolbar: {
            show: false,
          },
        },
        xaxis: {
            labels: {
                show: false  // x축 레이블 숨기기
            },
            axisBorder: {
                show: false  // x축 경계선 숨기기
            },
            axisTicks: {
                show: false  // x축 눈금 숨기기
            }
        },
        yaxis: {
            labels: {
                show: false  // y축 레이블 숨기기
            },
            axisBorder: {
                show: false  // y축 경계선 숨기기
            },
            axisTicks: {
                show: false  // y축 눈금 숨기기
            }
        },
        tooltip: {
            enabled: false  // 툴팁 숨기기
        },
        legend: {
          show: false,
          position: 'bottom'
        },
        title:{
          text: 'test'
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
                y: entry.Close,
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
