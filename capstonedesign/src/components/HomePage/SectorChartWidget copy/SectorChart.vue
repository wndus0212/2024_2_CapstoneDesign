<template>
  <div style="border-radius: 5px; border: 1px black solid; padding: 5px; margin-bottom: 5px;">
    <apexchart 
      type="line" 
      :options="chartOptions" 
      :series="series" 
      width="600"
      height="600"
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
    chartname: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      series: [],
      chartOptions: {
        chart: {
          type: 'line',
          toolbar: {
            show: true,
          },
        },
        stroke: {
          width: 2, // 선의 두께를 지정 (기본값은 4)
        },
        tooltip: {
          enabled: true,
        },
        legend: {
          show: true,
          position: 'bottom',
        },
        title: {
          text: this.chartname,
        },
        xaxis: {
          type: 'datetime',
          title: {
            text: 'Date',
          },
        },
        yaxis: {
          title: {
            text: 'Close Price',
          },
          labels: {
            formatter: (value) => Math.floor(value), // 소수점 제거
          },
        },
      },
    };
  },
  watch: {
    history: {
      handler(newHistory) {
        if (Array.isArray(newHistory) && newHistory.length > 0) {
          // 섹터별로 데이터를 그룹화
          const groupedData = this.groupBySector(newHistory);

          // 섹터별 시리즈 생성
          this.series = Object.keys(groupedData).map((sector) => ({
            name: sector,
            data: groupedData[sector].map((entry) => ({
              x: entry.Date, // 날짜
              y: entry.Close, // 종가
            })),
          }));
        } else {
          console.error("Error: history 데이터가 비어있습니다.", newHistory);
          this.series = [];
        }
      },
      immediate: true,
    },
  },
  methods: {
    /**
     * 섹터별로 데이터를 그룹화하는 메서드
     * @param {Array} data - 전체 주식 데이터
     * @returns {Object} 섹터별로 그룹화된 데이터
     */
    groupBySector(data) {
      const grouped = {};
      data.forEach((sectorData) => {
        const { Sector, "Stock History": stockHistory } = sectorData;
        if (!grouped[Sector]) {
          grouped[Sector] = [];
        }
        grouped[Sector].push(...stockHistory); // 섹터에 해당하는 주식 데이터를 추가
      });
      return grouped;
    },
  },
};
</script>
