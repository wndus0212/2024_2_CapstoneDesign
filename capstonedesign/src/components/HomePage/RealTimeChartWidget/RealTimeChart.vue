<template>
  <div class="realtime_container" width="300px">
    <div style="display: flex">
      <div style="width: 100px">
        <div class="chart-name">
          {{ this.chartname }}
        </div>
        <div>
          현재 {{ this.current }}
        </div>
        <div>
          하루 변화량: {{ this.current }}
        </div>
      </div>
      
      <apexchart 
        type="line" 
        :options="chartOptions" 
        :series="series" 
        :width="100"
        :height="100"
      />
    </div>
    
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts';

export default {
  components: {
    apexchart: VueApexCharts,
  },
  props: {
    history: {
      type: Array,
      required: true
    },
    chartname:{
      type: String,
      required:true
    },
    current:{
      type: Number,
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
        },
        stroke: {
          width: 1
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
<style>
  .realtime_container{
    background-color: rgb(240, 240, 250);
    border-radius: 15px;
    padding: 15px;
    width: 200px;
  }

  .chart-name{
    font-weight:500;
  }
</style>