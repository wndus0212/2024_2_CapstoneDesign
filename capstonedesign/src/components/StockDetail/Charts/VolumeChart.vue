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
        yaxis: {
          // 두 번째 y축: 거래량
          opposite: true,  // 반대쪽에 위치
          title: {
            text: '구매량'
          },
          labels: {
            formatter: function (value) {
              value.toFixed(0);
              return value.toLocaleString(); // 1000 단위마다 쉼표 추가
            }
          }
        },
        tooltip: {
          shared: false
        },
        legend: {
          show: true,
          position: 'bottom'
        },
        plotOptions: {
          bar: {
            borderRadius: 0, // 테두리 반경을 0으로 설정
            borderWidth: 0,  // 테두리 두께를 0으로 설정하여 테두리를 없앰
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
        console.log("Received history data:", newHistory);
        if (historyArray.length > 0) {
          
          this.series = [
            {
              name: 'Volume',
              type: 'column', // 거래량은 column 차트로 표시
              data: historyArray.map((entry, index) => ({
                x: new Date(new Date().setDate(new Date().getDate() - totalItems + index)), // 같은 날짜
                y: entry.Volume // 거래량
              }))
            }
          ];
          console.log("series",this.series)
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
