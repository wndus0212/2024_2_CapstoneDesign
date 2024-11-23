<template>
  <apexchart
    type="treemap"
    :options="chartOptions"
    :series="series"
    :width="600"
    :height="590"
  />
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: "TreeMap",
  components: {
    apexchart: VueApexCharts,
  },
  props: {
    treemapData: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      series: [
        {
          data: [],
        },
      ],
      chartOptions: {
        legend: {
          show: false,
        },
        chart: {
          height: 350,
          type: "treemap",
          toolbar: {
            show: false,
          },
        },
        dataLabels: {
          enabled: true,
          style: {
            fontSize: "14px",
            colors: ["#fff"],
          },
          formatter: function (text, op) {
            const value = op.value;
            return [text, `${value}%`];
          },
        },
        plotOptions: {
          treemap: {
            enableShades: false,
            colorScale: {
              ranges: [
                { from: -100, to: -1, color: "#FF4560" }, // 하락: 빨간색
                { from: 0, to: 1, color: "#FEB019" },   // 변화 없음: 노란색
                { from: 1, to: 100, color: "#00E396" },  // 상승: 녹색
              ],
            },
          },
        },
      },
    };
  },
  watch: {
    treemapData: {
      handler(newData) {
        if (Array.isArray(newData) && newData.length > 0) {
          this.series = [
            {
              data: newData.map((item) => ({
                x: item.names, // 섹터 이름
                y: item.market_caps, // 시가총액: 네모 크기
                color: item.change, // 변화량에 따라 색상
              })),
            },
          ];
        } else {
          console.warn("No valid data for treemap.");
          this.series = [{ data: [] }];
        }
      },
      immediate: true,
    },
  },
};
</script>

<style>
/* 필요 시 스타일 추가 */
</style>
