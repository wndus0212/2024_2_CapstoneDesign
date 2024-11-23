<template>
  <container-box>
    <box-title>
      시장 한눈에 보기
    </box-title>

    <!-- 로딩 중 표시 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>로딩 중...</p>
    </div>

    <div style="display: flex; gap: 60px; justify-content: center;" v-if="!isLoading">
      <TreeMap :treemapData="filteredData" />
    </div>

    <div style="margin-top: 20px; text-align: center;" v-if="!isLoading">
      <SelectBox
        :options="selectOption"
        v-model="selectedOption1"
        @change="applyFilter"
      />
    </div>
  </container-box>
</template>

<script>
import containerBox from "@/components/Box.vue";
import boxTitle from "@/components/BoxTitle.vue";
import TreeMap from "./TreeMap.vue";
import SelectBox from "@/components/SelectBox.vue";
import axios from "axios";

export default {
  name: "TreeMapWidget",
  components: {
    containerBox,
    boxTitle,
    TreeMap,
    SelectBox,
  },
  data() {
    return {
      selectOption: [
        { label: "1일", value: "1d" },
        { label: "1달", value: "1mo" },
        { label: "1년", value: "1y" },
      ],
      selectedOption1: "1d", // 초기 선택 옵션
      treemapRawData: [], // API로부터 원본 데이터
      filteredData: [], // 필터링된 데이터
      isLoading: false, // 로딩 상태
    };
  },
  mounted() {
    this.fetchSectorData();
    this.updateUrlWithSelectedOption();
  },
  watch: {
    selectedOption1(newValue) {
      this.applyFilter();
      this.updateUrlWithSelectedOption(newValue);
    },
  },
  methods: {
    async fetchSectorData() {
      this.isLoading = true; // 로딩 시작
      try {
        const response = await axios.get(`http://127.0.0.1:8000/stock/sector_weight/${this.selectedOption1}`);
        const output = response.data.output || [];
        if (!Array.isArray(output) || output.length === 0) {
          console.warn("API returned no valid data.");
          alert("데이터를 가져오지 못했습니다. 다시 시도해주세요.");
          this.treemapRawData = [];
          this.filteredData = [];
          return;
        }

        this.treemapRawData = output;
        this.applyFilter();
      } catch (error) {
        console.error("Error fetching data:", error);
        alert("데이터를 불러오는 데 실패했습니다. 네트워크를 확인해주세요.");
        this.treemapRawData = [];
        this.filteredData = [];
      } finally {
        this.isLoading = false; // 로딩 종료
      }
    },
    applyFilter() {
      if (!this.treemapRawData || this.treemapRawData.length === 0) {
        console.warn("No raw data available to filter.");
        this.filteredData = [];
        return;
      }

      const periodKey = {
        "1d": "one_day_change",
        "1mo": "one_month_change",
        "1y": "one_year_change",
      }[this.selectedOption1];

      // 개별 주식으로 데이터 필터링
      this.filteredData = this.treemapRawData.map((item) => ({
        sector: item.sector,
        names: item.names,
        market_caps: parseFloat(item.market_caps?.replace(/,/g, "") || 0),
        change: parseFloat(item[periodKey]?.replace(/,/g, "") || 0),
      }));

      // 시가총액 기준으로 정렬 (내림차순)
      this.filteredData.sort((a, b) => b.market_caps - a.market_caps);

      console.log("Filtered Data:", this.filteredData);
    },
    updateUrlWithSelectedOption() {
      this.$router.push({ query: { period: this.selectedOption1 } });
    },
  },
};
</script>

<style>
/* 로딩 중 오버레이 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* 로딩 스피너 스타일 */
.loading-spinner {
  border: 5px solid #f3f3f3; /* 배경 색 */
  border-top: 5px solid #3498db; /* 로딩 색 */
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  margin-top: 20px;
}

.select-box {
  margin: 10px 0;
}
</style>
