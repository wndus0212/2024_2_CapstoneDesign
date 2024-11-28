<template>
    <Box width="1280px">
      <BoxTitle>
        지금 뜨는 섹터
      </BoxTitle>
      
      <div v-if="isLoading" class="loading">
        데이터 로딩 중...
      </div>
      <div v-else class="sector-list">
        <div v-for="(sector, index) in sector_diffs" :key="index" class="sector-item">
          <TrendingSector
            :data="sector"
          />
        </div>
      </div>
    </Box>
  </template>
  
  <script>
  import axios from 'axios';
  import Box from '@/components/Box.vue';
  import BoxTitle from '@/components/BoxTitle.vue';
  import TrendingSector from './TrendingSector.vue';
  
  export default {
    components: {
      Box,
      BoxTitle,
      TrendingSector,
    },
    mounted() {
      this.updateChartData(); // 초기 데이터 로드
    },
    data() {
      return {
        isLoading: true, // 로딩 상태 플래그
        sector_diffs: [], // 섹터의 차트 데이터
      };
    },
    methods: {
      updateChartData() {
        console.log("Updating chart data...");
        this.fetchAllDiffData();
      },
      fetchAllDiffData() {
        this.isLoading = true; // 로딩 시작
        axios
          .get("http://127.0.0.1:8000/stock/sector_diff/")
          .then((response) => {
            this.sector_diffs = response.data["output"];
            console.log("sectordiff", this.sector_diffs);
          })
          .catch((error) => {
            console.error("데이터 로드 중 오류:", error);
          })
          .finally(() => {
            this.isLoading = false; // 로딩 종료
          });
      },
    },
  };
  </script>
  
  <style scoped>
  .loading {
    text-align: center;
    font-size: 1.5em;
    color: gray;
    margin-top: 20px;
  }
  
  .sector-list {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .sector-item {
    background-color: #f0f0f0;
    border-radius: 15px;
    padding: 20px;
    width: 250px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  </style>
  