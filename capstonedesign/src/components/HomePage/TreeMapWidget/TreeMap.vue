<template>
  <apexchart 
    type="treemap" 
    :options="chartOptions" 
    :series="series" 
    :width="600" 
    :height="590" />
</template>

<script>
import VueApexCharts from 'vue3-apexcharts';
import axios from 'axios'; // Axios import

export default {
  name: 'TreeMapWidget',
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      series: [], // 초기값은 빈 배열로 설정
      chartOptions: {
        legend: {
          show: false,
        },
        chart: {
          height: 350,
          type: 'treemap',
          toolbar: {
            show: false,
          },
        },
        dataLabels: {
          enabled: true,
          style: {
            fontSize: '20px',
          },
          formatter: function (text, op) {
            return [text, op.value];
          },
          offsetY: -4,
        },
        plotOptions: {
          treemap: {
            enableShades: true,
            shadeIntensity: 0.5,
            reverseNegativeShade: true,
            colorScale: {
              ranges: [
                {
                  from: 0,
                  to: 1000000000000,
                  color: '#008f05'
                },
              ]
            },
          },
        },
      },
    };
  },
  mounted() {
    this.fetchTreeMapData(); // 컴포넌트가 마운트될 때 데이터 요청
  },
  methods: {
    fetchTreeMapData() {
      axios.get('http://127.0.0.1:8000/stock/sector_weight')
        .then(response => {
          // API 응답 데이터 확인
          console.log('Response data:', response.data);

          // output 배열 추출
          const fetchedData = response.data.output;

          // fetchedData가 배열인지 확인
          if (Array.isArray(fetchedData)) {
            // 데이터를 Treemap 형식에 맞게 변환
            this.series = [
              {
                data: fetchedData.map(item => ({
                  x: item.sector,       // 섹터 이름
                  y: item.market_weight // 시장 가중치
                }))
              }
            ];
          } else {
            console.error('Fetched data is not an array:', fetchedData);
          }
        })
        .catch(error => {
          console.error('Error fetching sector data:', error);
        });
    },
  },
};
</script>

<style>
/* 필요에 따라 스타일 추가 */
</style>
