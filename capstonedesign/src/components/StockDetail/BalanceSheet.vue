<template>
    <div style="display: flex; justify-content: space-evenly;">
      <apexchart 
        :options="chartOptions" 
        :series="series" 
        width="700" 
        height="400" 
      />
      <div style="display: flex; justify-content: center;">
        <div class="FinancialScrollContainer">
            <div class="table-wrapper">
                <table class="FinancialStatement">
                    <tbody>
                        <tr>
                            <td>
                                매출총이익률
                            </td>
                            <td>
                                100,000,000
                            </td>
                        </tr>
                        <tr>
                            <td>
                                영업이익률
                            </td>
                            <td>
                                100,000,000
                            </td>
                        </tr>
                        <tr>
                            <td>
                                순이익률
                            </td>
                            <td>
                                100,000,000
                            </td>
                        </tr>
                        <tr>
                            <td>
                                투자수익률
                            </td>
                            <td>
                                100,000,000
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    </div>
  </template>
  
  <script>
  import VueApexCharts from 'vue3-apexcharts'
  
  export default {
    components: {
      apexchart: VueApexCharts
    },
    data() {
      return {
        series: [
          {
            name: 'Net Profit',
            data: [44, 55, 57, 56, 61, 58, 63, 60, 66]
          },
          {
            name: 'Revenue',
            data: [76, 85, 101, 98, 87, 105, 91, 114, 94]
          },
          {
            name: 'Free Cash Flow',
            data: [35, 41, 36, 26, 45, 48, 52, 53, 41]
          }
        ],
        chartOptions: {
          chart: {
            height: 350,
            width: 500,
            type: 'bar',  // 바 차트로 설정
          },
          stroke: {
            width: [3, 1]
          },
          yaxis: {
            labels: {
              formatter: function (val) {
                return val.toFixed(0); // 포맷 간단화
              },
            },
            title: {
              text: 'Price'
            },
          },
          xaxis: {
            categories: ['2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028'], // 임의로 설정 (datetime 대신 카테고리로 변경)
          },
          tooltip: {
            shared: false,
            y: {
              formatter: function (val) {
                return val.toFixed(0) // 포맷 간단화
              }
            }
          },
          legend: {
            show: true,
            position: 'bottom'
          },
          plotOptions: {
            bar: {
              horizontal: false,
              columnWidth: '55%',
              endingShape: 'rounded'
            },
          },
        }
      };
    }
  };
  </script>
<style>
.FinancialScrollContainer {

  min-width: 500px;
  width: 700px;
  border-radius: 10px;

  height: 500px;
  display: flex;

}

.table-wrapper {
  max-height: 700px; /* 스크롤되는 높이 설정 */
  overflow-y: auto; /* 수직 스크롤 */
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.FinancialStatement {
  width: 100%;
  border-collapse: collapse;
  font-size: 20px;
  border: none
}

.FinancialStatement th {
  width: 200px;
  background-color: #f1f1f1;
}

.FinancialStatement tbody tr {
  font-size: 30px;
  height: 100px;
  border: 1px solid lightgray;
}

.FinancialStatement td, .FinancialStatement th {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  border: none
}
</style>