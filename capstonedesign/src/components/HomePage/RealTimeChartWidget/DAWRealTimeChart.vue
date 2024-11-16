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
        },
        xaxis: {
          type: 'datetime'
        },

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
        
        if (historyArray.length > 0) {
          console.log("차트: ",historyArray)
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
          console.log(this.series);
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
