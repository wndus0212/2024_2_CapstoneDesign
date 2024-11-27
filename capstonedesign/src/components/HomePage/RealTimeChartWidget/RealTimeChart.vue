<template>
  <Box width="300px">
    <div style="display: flex">
      <div>
        <div class="chart-name">
          {{ this.chartname }}
        </div>
        <div>
          {{  }}
        </div>
      </div>
      
      <apexchart 
        type="line" 
        :options="chartOptions" 
        :series="series" 
        :width="200"
        :height="100"
      />
    </div>
    
  </Box>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts';
import Box from '@/components/Box.vue';

export default {
  components: {
    apexchart: VueApexCharts,
    Box
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
            enabled: true
          },
          toolbar: {
            show: true,
          },
        },
        tooltip: {
            enabled: false  // 툴팁 숨기기
        },
        legend: {
          show: false,
          position: 'bottom'
        },
        title:{
          show: false
        },
        xaxis: {
          type: 'datetime',
          show: false
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
                y: entry.Close
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
