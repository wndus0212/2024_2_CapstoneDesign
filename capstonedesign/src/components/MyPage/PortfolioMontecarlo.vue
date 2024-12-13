<template>
  <div>
    <SmallButton text="몬테카를로 테스트 시작" @click="runMontecarloTest" />
    
    <!-- 로딩 중 애니메이션 -->
    <div v-if="loading" class="loading-overlay">
      <div>
        <div class="loading-spinner"></div>
        <div class="loading-text">로딩 중입니다</div>
        <div class="loading-text">약 30초가 소요됩니다</div>
      </div>
    </div>

    <!-- 로딩이 끝났으면 차트 표시 -->
    <div v-else>
      <!-- finalcash와 mdd 배열을 prop으로 전달 -->
      <MontecarloFinalCash v-if="finalcash.length > 0" :data="finalcash" />
      
      <!-- mdd가 비어 있지 않을 경우에만 MontecarloMDD 렌더링 -->
      <MontecarloMDD v-if="mdd.length > 0" :data="mdd" />
    </div>
  </div>
</template>

<script>
import SmallButton from '@/components/SmallButton.vue';
import axios from 'axios';
import MontecarloFinalCash from './MontecarloFinalCash.vue';
import MontecarloMDD from './MontecarloMDD.vue';

export default {
  components: {
    SmallButton,
    MontecarloFinalCash,
    MontecarloMDD
  },
  props: {
    portfolioId: {
      type: Number,
      required: true,
    }
  },
  data() {
    return {
      finalcash: [],  // Final Cash 데이터를 저장할 배열
      mdd: [],        // MDD 데이터를 저장할 배열
      loading: false  // 로딩 상태
    };
  },
  methods: {
    // 몬테카를로 테스트 실행 후 CSV 로드
    runMontecarloTest() {
      const token = localStorage.getItem("token");

      // 로딩 시작
      this.loading = true;

      // 1. 몬테카를로 테스트 실행 (CSV 파일 생성)
      axios.get(`https://port-0-capstonedesign-m3vkxnzga0885b97.sel4.cloudtype.app/portfolio/montecarlo/${this.portfolioId}/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
      .then(response => {
        const csvData = response.data.output;
        // Final Cash 및 MDD 데이터 추출
        this.finalcash = csvData.map(item => item.final_cash);
        this.mdd = csvData.map(item => item.mdd);
      })
      .catch(error => {
        console.error(error);
      })
      .finally(() => {
        this.loading = false;
      });
    },
  }
};
</script>

<style scoped>
/* 로딩 오버레이 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* 로딩 스피너 스타일 */
.loading-spinner {
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid #007bff;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

/* 로딩 텍스트 스타일 */
.loading-text {
  margin-top: 20px;
  color: black;
  font-size: 1.2em;
}

/* 스피너 회전 애니메이션 */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
