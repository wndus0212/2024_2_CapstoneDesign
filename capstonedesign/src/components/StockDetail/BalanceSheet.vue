<template>
  <div class="financialbox">
    <apexchart 
      :options="chartOptions" 
      :series="series" 
      width="600" 
      height="400" 
    />
    
    <ToggleButton
      label="대차 대조표 자세히"
      :isVisible="toggle"
      @toggle="toggleIncomeStatement"
    />
    <div v-if="toggle" class="table-wrapper">
      <div>대차 대조표</div>
      <table class="FinancialStatement">
        <thead>
          <tr>
            <th>항목</th>
            <th v-for="(year, index) in years" :key="index">{{ year }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(value, key) in formattedData" :key="key">
            <td>{{ key }}</td>
            <td v-for="(item, index) in value" :key="index">{{ item }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";
import ToggleButton from "../ToggleButton.vue";

export default {
  components: {
    apexchart: VueApexCharts,
    ToggleButton,
  },
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      chartOptions: {
        chart: {
          height: 350,
          width: 500,
          type: "bar",
        },
        stroke: {
          width: [3, 1],
        },
        dataLabels: {
          enabled: false
        },
        yaxis: {
          labels: {
            formatter: function (value) {
              value.toFixed(0);
              return value.toLocaleString(); // 1000 단위마다 쉼표 추가
            }
          },
        },
        xaxis: {
          categories: [
            "2020",
            "2021",
            "2022",
            "2023",
          ],
        },
        tooltip: {
          shared: false,
          y: {
            formatter: function (val) {
              return val.toFixed(0);
            },
          },
        },
        legend: {
          show: true,
          position: "bottom",
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: "55%",
            endingShape: "rounded",
          },
        },
      },
      toggle: false, // 토글 상태 초기값
    };
  },
  computed: {
    years() {
      // 연도를 추출
      console.log(this.data)
      return Object.keys(this.data);
    },
    series() {
      const totalAssets = [];
      const liabilities = [];
      const equity = [];

      this.years.forEach((year) => {
        const yearData = this.data[year];
        console.log("yearData", yearData)
        totalAssets.push(yearData["Total Assets"] || 0);
        liabilities.push(yearData["Current Liabilities"] || 0);
        equity.push(yearData["Common Stock Equity"] || 0);
      });
      return [
        { name: "totalAssets", data: totalAssets },
        { name: "liabilities", data: liabilities },
        { name: "equity", data: equity },
      ];
    },
    formattedData() {
      // 데이터를 항목별로 정리
      const result = {};
      this.years.forEach((year) => {
        const yearData = this.data[year];
        for (const [key, value] of Object.entries(yearData)) {
          if (!result[key]) {
            result[key] = [];
          }
          result[key].push(value);
        }
      });
      return result;
    },
  },
  methods: {
    toggleIncomeStatement() {
      this.toggle = !this.toggle; // 토글 상태 변경
    },
  },
};
</script>

<style>
.FinancialScrollContainer {
  min-width: 500px;
  width: 1200px;
  border-radius: 10px;
  height: 700px;
  display: flex;
}

.table-wrapper {
  max-height: 600px; /* 스크롤되는 높이 설정 */
  overflow-y: auto; /* 수직 스크롤 */
  width: 100%;
  display: flex;
  flex-direction: column;
}

.FinancialStatement {
  width: 100%;
  border-collapse: collapse;
  font-size: 20px;
  border: none;
}

.FinancialStatement th {
  width: 200px;
  background-color: #f1f1f1;
}

.FinancialStatement tbody tr {
  font-size: 15px;
  height: 50px;
  border: 1px solid lightgray;
}

.FinancialStatement td,
.FinancialStatement th {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  border: none;
}

.financialbox{
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 10px;
  margin-bottom: 20px;
}
</style>
