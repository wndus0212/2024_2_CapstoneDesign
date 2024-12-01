<template>
  <div class="realtime_container" width="200px">
    <div style="display: flex">
      <div style="width: 130px; text-overflow: ellipsis;">
        <div class="indexname">
          {{ chartname }}
        </div>
        <div style="font-size: 20px; font-weight: 600;">
          {{ diff[0]?.['Current Price'].toFixed(2) || "데이터 없음" }}
        </div>
        <div :style="{ color: changeValueColor }" style="font-size: 15px;">
          {{ changeValue }}
        </div>
      </div>

      <apexchart 
        type="line" 
        :options="chartOptions" 
        :series="series" 
        :width="80"
        :height="100"
      />
    </div>
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  components: {
    apexchart: VueApexCharts,
  },
  props: {
    history: {
      type: Array,
      required: true,
    },
    chartname: {
      type: String,
      required: true,
    },
    diff: {
      type: Array, // diff는 배열로 정의
      required: true,
    },
    period: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      series: [],
      chartOptions: {
        chart: {
          height: 150,
          width: 230,
          type: "line",
          sparkline: {
            enabled: true,
          },
        },
        tooltip: {
          enabled: false, // 툴팁 숨기기
        },
        xaxis: {
          type: "datetime",
          labels: {
            show: false,
          },
        },
        yaxis: {
          labels: {
            formatter: (value) => Math.floor(value),
          },
        },
        stroke: {
          width: 1,
        },
      },
    };
  },
  computed: {
    /**
     * period와 diff를 기반으로 변화량을 계산
     */
    changeValue() {
      if (!this.diff || !this.diff[0]) {
        return "데이터 없음";
      }
      if (this.period === '1d') {
        return `${this.diff[0]['1 Day Change per'].toFixed(2)}%`;
      } else if (this.period === '1mo') {
        return `${this.diff[0]['1 Month Change per'].toFixed(2)}%`;
      } else if (this.period === '1y') {
        return `${this.diff[0]['1 Year Change per'].toFixed(2)}%`;
      }
      return "데이터 없음";
    },
    changeValueColor() {
      const value = this.changeValue;
      if (value === "데이터 없음") return "black"; // 데이터 없음일 때 기본 색상
      const percentage = parseFloat(value.replace('%', '')); // % 제거하고 숫자만 추출
      return percentage > 0 ? "red" : (percentage < 0 ? "blue" : "black");
    },
  },
  watch: {
    history: {
      handler(newHistory) {
        const historyArray = Array.isArray(newHistory) ? newHistory : [];
        const totalItems = historyArray.length;

        if (historyArray.length > 0) {
          this.series = [
            {
              name: "line",
              type: "line",
              data: historyArray.map((entry, index) => ({
                x: new Date(
                  new Date().setDate(new Date().getDate() - totalItems + index)
                ),
                y: entry.Close,
              })),
            },
          ];
        } else {
          console.error(
            "Error: history 데이터의 output이 비어있거나 존재하지 않습니다.",
            newHistory
          );
          this.series = [];
        }
      },
      immediate: true,
    },
  },
  mounted() {
    if (!this.diff || !Array.isArray(this.diff) || !this.diff[0]) {
      console.error("Error: diff 데이터가 비어 있거나 유효하지 않습니다.", this.diff);
    } else {
      console.log("diff 데이터:", this.diff[0]);
    }
  },
};
</script>

<style>
.realtime_container {
  background-color: rgb(240, 240, 250);
  border-radius: 15px;
  padding: 15px;
  width: 220px;
}

.indexname {
  font-weight: 500;
  margin-bottom: 10px;
}
</style>
