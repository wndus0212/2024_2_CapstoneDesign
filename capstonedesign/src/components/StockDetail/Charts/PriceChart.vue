<template>
  <div>
    <apexchart 
      type="candlestick" 
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
          height: 350,
          width: 500,
          type: 'candlestick',
        },
        xaxis: {
          type: 'datetime'
        },
        yaxis: [
          {
            // 첫 번째 y축: 시가/고가/저가/종가
            title: {
              text: '주가'
            },
          }
        ],
        tooltip: {
          shared: false
        },
        legend: {
          show: true,
          position: 'bottom'
        }
      }
    };
  },
  watch: {
    history: {
      handler(newHistory) {
        const historyArray = newHistory && Array.isArray(newHistory) ? newHistory : [];
        const totalItems = historyArray.length;
        console.log("Received history data:", newHistory);
        if (historyArray.length > 0) {
          this.series = [
            {
              name: 'candlestick',
              type: 'candlestick',
              data: historyArray.map((entry, index) => ({
                x: new Date(new Date().setDate(new Date().getDate() - totalItems + index)),
                y: [entry.Open, entry.High, entry.Low, entry.Close], // 시가, 고가, 저가, 종가
              }))
            }
          ]
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
