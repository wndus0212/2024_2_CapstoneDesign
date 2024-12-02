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
    bollingerBandData: {
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
          opposite: true, // 반대쪽에 위치
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
    bollingerBandData: {
      handler(newData) {
        // 데이터가 배열 형식인지 확인하고 출력
        console.log("Received Bollinger Band data:", newData);

        const dataArray = newData && Array.isArray(newData) ? newData : [];
        const totalItems = dataArray.length;
        
        if (dataArray.length > 0) {
          // 상단 밴드, 중심선(이동평균선), 하단 밴드를 각각 map으로 처리
          const upperBandData = dataArray.map((entry, index) => ({
            x: new Date(new Date().setDate(new Date().getDate() - totalItems + index)),
            y: entry.upper_band || null // 상단 밴드 값이 없다면 null로 처리
          }));

          const movingAverageData = dataArray.map((entry, index) => ({
            x: new Date(new Date().setDate(new Date().getDate() - totalItems + index)),
            y: entry.moving_average || null // 이동평균선 값이 없다면 null로 처리
          }));

          const lowerBandData = dataArray.map((entry, index) => ({
            x: new Date(new Date().setDate(new Date().getDate() - totalItems + index)),
            y: entry.lower_band || null // 하단 밴드 값이 없다면 null로 처리
          }));

          // series 배열에 상단 밴드, 이동평균선, 하단 밴드를 추가
          this.series = [
            {
              name: 'Upper Band',
              type: 'line',
              data: upperBandData,
              color: '#FF5733' // 상단 밴드 선의 색상
            },
            {
              name: 'Moving Average',
              type: 'line',
              data: movingAverageData,
              color: '#33FF57' // 이동평균선의 색상
            },
            {
              name: 'Lower Band',
              type: 'line',
              data: lowerBandData,
              color: '#33A1FF' // 하단 밴드 선의 색상
            }
          ];
        } else {
          console.error("Error: Bollinger Band 데이터가 비어있습니다.");
          this.series = [];
        }
      },
      immediate: true
    }
  }
};
</script>
