<template>
  <Box :width="1400">
    <BoxTitle>
      지금 뜨는 섹터
    </BoxTitle>
    
    <div v-if="isLoading">
      <LoadingComponent/>
    </div>
    <div v-else class="sector-list">
      <div v-for="(sector, index) in visibleSectors" :key="index" @click="openModal(sector)">
        <div class="sectorhover">
          <TrendingSector
            :data="sector"
            :index="index"
          />
        </div>
        
      </div>
    </div>
    
    <!-- 더보기 버튼: 로딩 중일 때는 보이지 않도록 조건 추가 -->
    <div v-if="!isLoading" @click="toggleShowAll" class="load-more">
      {{ showAll ? '접기' : '더보기' }}
    </div>
    
    <!-- 모달 컴포넌트 -->
    <SectorModal
      :isOpen="isModalOpen"
      :sector="modalSector"
      @close="closeModal"
    />
  </Box>
</template>

<script>
import axios from 'axios';
import Box from '@/components/Box.vue';
import BoxTitle from '@/components/BoxTitle.vue';
import TrendingSector from './TrendingSector.vue';
import SectorModal from './SectorModal.vue';
import LoadingComponent from '@/components/LoadingComponent.vue';

export default {
  components: {
    Box,
    BoxTitle,
    TrendingSector,
    SectorModal,
    LoadingComponent
  },
  mounted() {
    this.updateChartData(); // 초기 데이터 로드
  },
  data() {
    return {
      isLoading: true, // 로딩 상태 플래그
      sector_diffs: [], // 섹터의 차트 데이터
      showAll: false, // 더보기 버튼 클릭 여부
      isModalOpen: false, // 모달 열림 상태
      modalSector: {}, // 모달에 전달할 섹터 정보
    };
  },
  computed: {
    visibleSectors() {
      // 더보기 버튼을 클릭했을 때는 모든 데이터를 보여주고, 아니면 5개만 보여준다.
      return this.showAll ? this.sector_diffs : this.sector_diffs.slice(0, 5);
    },
  },
  methods: {
    updateChartData() {
      console.log("Updating chart data...");
      this.fetchAllDiffData();
    },
    fetchAllDiffData() {
      this.isLoading = true; // 로딩 시작
      axios
        .get("https://web-capstonedesignfront-m3vkxnzga0885b97.sel4.cloudtype.app/stock/sector_diff/")
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
    toggleShowAll() {
      this.showAll = !this.showAll; // 버튼 클릭 시 showAll 값을 토글
    },
    openModal(sector) {
      this.modalSector = sector; // 클릭한 섹터 정보를 모달에 전달
      this.isModalOpen = true; // 모달 열기
    },
    closeModal() {
      this.isModalOpen = false; // 모달 닫기
      this.modalSector = {}; // 모달 내용 초기화
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
  display: grid; /* Flex 대신 grid 사용 */
  grid-template-columns: repeat(5, 1fr); /* 한 줄에 5개의 섹터 */
  gap: 20px; /* 섹터 간의 간격 */
  margin-top: 20px;
}

.sectorhover {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.sectorhover:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15), 0 2px 4px rgba(0, 0, 0, 0.1);
}

.load-more {
  text-align: center;
  font-size: 1em;
  color: gray;
  cursor: pointer;
  margin-top: 20px;
}


</style>
