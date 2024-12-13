<template>
  <div>
    <!-- 히스토그램 차트 컴포넌트 -->
    <apexchart 
      type="bar" 
      :options="chartOptions" 
      :series="series" 
      :width="850"
      :height="400"
    />
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts';

export default {
  components: {
    apexchart: VueApexCharts,
  },
  props: {
    data: {
      type: Array,
      required: true,
    }
  },
  data() {
    return {
      chartOptions: {
        chart: {
          type: 'bar',
          height: 350,
        },
        dataLabels: {
          enabled: false,
        },
        title: {
          text: 'MDD',
          align: 'left',
        },
        xaxis: {
          title: {
            text: 'MDD',
          },
          categories: [],  // x축에 분포 구간을 넣을 예정
        },
        yaxis: {
          title: {
            text: 'Frequency',
          },
        },
        tooltip: {
          shared: false,
        },
      },
      series: [
        {
          name: 'Frequency',
          data: [],  // 빈도 데이터를 여기에 채울 예정
        }
      ],
    };
  },
  watch: {
      data(newData) {
      console.log("Received data:", newData); // 데이터가 전달되었는지 확인
      this.updateHistogramData(newData); // 차트 업데이트 함수 호출
      },
  },
  mounted(){
      this.updateHistogramData(this.data)
  },
  methods: {
      updateHistogramData(data) {
          console.log("histogram")
          if (!data || !Array.isArray(data)) {
              console.error("Data is undefined or not an array:", data);
              return;
          }
          // 최종 현금값만 추출
          const mddValues = data
          console.log(mddValues)
          // 히스토그램 구간을 만들기 위해 데이터의 최소값과 최대값을 구함
          const minValue = Math.min(...mddValues);
          const maxValue = Math.max(...mddValues);

          // 구간 설정 (예: 10단위로 구간 나누기)
          const bins = 20;
          const binWidth = (maxValue - minValue) / bins;

          const histogramData = new Array(bins).fill(0);
          const categories = [];

          // 데이터 분포를 히스토그램 구간에 맞게 나누기
          mddValues.forEach(value => {
              let binIndex = Math.floor((value - minValue) / binWidth);  // let으로 선언
              if (binIndex === bins) binIndex--;  // 최대값을 마지막 구간에 포함
              histogramData[binIndex]++;
          });

          // 구간을 x축에 표시할 범위로 생성
          for (let i = 0; i < bins; i++) {
              const binStart = (minValue + i * binWidth).toFixed(0);
              const binEnd = (minValue + (i + 1) * binWidth).toFixed(0);
              categories.push(`${binStart} - ${binEnd}`);
          }
          console.log(categories)
          // 차트 데이터 업데이트
          this.chartOptions.xaxis.categories = categories;
          this.series[0].data = histogramData;
      }

  }
};
</script>

<style scoped>
/* 스타일을 필요에 맞게 조정 */
</style>
