<template>
  <div>
    <BoxTitle>
      Chat GPT 생성 포트폴리오
    </BoxTitle>
    <Box>
      <!-- 테이블: 종목 목록 -->
      <div class="table-container">
        <table class="styled-table">
          <thead>
            <tr>
              <th>종목 이름</th>
              <th>개수</th>
              <th>섹터</th>
              <th>배분 금액(KRW)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(stock, index) in portfolioResult.output" :key="index">
              <td>{{ stock['종목명'] }}</td>
              <td>{{ stock['개수'] }}</td>
              <td>{{ stock['섹터'] }}</td>
              <td>{{ stock['배분 금액(KRW)'] }} 원</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 포트폴리오 설명 -->
      <Box class="description-box">
        <h3>포트폴리오 설명</h3>
        <p>{{ portfolioResult.description }}</p>
      </Box>
    </Box>

    
  </div>
</template>

<script>
import BoxTitle from '@/components/BoxTitle.vue';
import Box from '../Box.vue';

export default {
  components: {
    BoxTitle,
    Box
  },
  props: {
    // 포트폴리오 종목 목록을 prop으로 받음
    portfolioResult: {
      type: Object,
      required: true
    },
    // 포트폴리오 설명을 prop으로 받음 (기본값 설정 가능)
    description: {
      type: String,
      default: '이 포트폴리오는 Chat GPT가 생성한 투자 전략을 기반으로 설계되었습니다. 안정성과 수익성을 고려하여 다양한 종목으로 구성되어 있으며, 지속적인 업데이트와 분석을 통해 최적화된 결과를 제공합니다.'
    }
  }
};
</script>

<style scoped>
.table-container {
  overflow-x: auto;
  margin: 20px 0;
  border-radius: 8px;
  border: 1px solid #ddd;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 16px;
  text-align: left;
}

.styled-table thead tr {
  background-color: #6dbdff;
  color: #ffffff;
  text-align: center;
}

.styled-table th, .styled-table td {
  padding: 12px 15px;
  border: 1px solid #ddd;
}

.styled-table tbody tr:nth-child(even) {
  background-color: #f3f3f3;
}

.styled-table tbody tr:hover {
  background-color: #f1f1f1;
}

.description-box {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f8f8f8;
}

.description-box h3 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 18px;
}

.description-box p {
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
}
</style>
