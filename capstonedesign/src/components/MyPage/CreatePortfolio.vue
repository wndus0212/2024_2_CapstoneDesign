<template>
  <div>
    <!-- 오버레이 (로딩 중일 때만 보이게) -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <div>
        Chat GPT가 포트폴리오를 생성중입니다
      </div>
    </div>
    
    <!-- 질문 블록 -->
    <div class="questionBlock" v-for="(question, index) in questions" :key="index">
      <div class="question">
        {{ question }}
      </div>
      <template v-if="index === 1">
        <!-- 투자 전략 질문은 SelectBox로 대체 -->
        <SelectBox
          :options="strategyOptions"
          v-model="answers[index]"
        />
      </template>
      <template v-else>
        <input
          type="text"
          class="answer"
          v-model="answers[index]" 
        />
      </template>
    </div>

    <!-- 에러 메시지 -->
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <!-- 생성하기 버튼 클릭 시 포트폴리오 요청 -->
    <SmallButton text="생성하기" @click="submitPortfolioRequest" />
    
    <!-- 포트폴리오 결과 표시 -->
    <GPTCreatedPortfolio v-if="portfolioResult" :portfolioResult="portfolioResult" />
    <SmallButton v-if="portfolioResult" text="저장하기" @click="savePortfolio"></SmallButton>
  </div>
</template>

<script>
import axios from "axios";
import SmallButton from "../SmallButton.vue";
import GPTCreatedPortfolio from "./GPTCreatedPortfolio.vue";
import SelectBox from "../SelectBox.vue"; // SelectBox 컴포넌트 import

export default {
  components: {
    SmallButton,
    GPTCreatedPortfolio,
    SelectBox,
  },
  data() {
    return {
      questions: [
        "새 포트폴리오 이름",
        "투자 전략",
        "예상 투자 기간(year)",
        "투자 금액(원)",
        "감수 가능한 손실(%)",
        "기대 수익(%)",
      ],
      strategyOptions: [
        { label: "--선택하세요--", value: "" },
        { label: "가치투자", value: "가치투자" },
        { label: "성장투자", value: "성장투자" },
      ],
      answers: ["", "", "", "", "",""],
      portfolioResult: null,
      errorMessage: "",
      isLoading: false,  // 로딩 상태
    };
  },
  methods: {
    isFormValid() {
      const isValidNumber = (value) => !isNaN(value) && value.trim() !== '';

      return (
        this.answers[0].trim() !== '' && 
        this.answers[1].trim() !== '' && // 투자 전략 선택 여부 확인
        isValidNumber(this.answers[2]) &&
        isValidNumber(this.answers[3]) &&
        isValidNumber(this.answers[4]) &&
        isValidNumber(this.answers[5]) 
      );
    },

    async submitPortfolioRequest() {
      if (!this.isFormValid()) {
        this.errorMessage = "모든 항목을 올바르게 입력해 주세요.";
        return;
      }

      this.errorMessage = "";
      this.isLoading = true;  // 로딩 시작

      const payload = {
        name: this.answers[0],
        strategy: this.answers[1],
        duration: this.answers[2],
        amount: parseInt(this.answers[3]),
        risk_tolerance: parseFloat(this.answers[4]),
        goal: parseFloat(this.answers[5]),
        market: "국내",
      };

      const token = localStorage.getItem("token");
      try {
        const response = await axios.post("https://web-capstonedesignfront-m3vkxnzga0885b97.sel4.cloudtype.app/portfolio/ai_portfolio/", payload, {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        });
        this.portfolioResult = response.data;  // API 응답 데이터 저장
        console.log(response.data);
      } catch (error) {
        console.error("포트폴리오 요청 실패:", error);
        this.errorMessage = "포트폴리오 요청에 실패했습니다. 다시 시도해주세요.";
      } finally {
        this.isLoading = false;  // 로딩 끝
      }
    },
    async savePortfolio() {
      if (!this.portfolioResult) {
        this.errorMessage = "저장할 포트폴리오가 없습니다.";
        return;
      }

      this.errorMessage = "";
      this.isLoading = true;  // 로딩 시작

      const payload = {
        name:this.answers[0],
        portfolio_data: this.portfolioResult,  // 포트폴리오 데이터를 서버로 전송
      };

      const token = localStorage.getItem("token");
      try {
        const response = await axios.put("https://web-capstonedesignfront-m3vkxnzga0885b97.sel4.cloudtype.app/portfolio/ai_portfolio/", payload, {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        });
        console.log("포트폴리오 저장 성공:", response.data);
        alert("포트폴리오가 저장되었습니다.");
        this.$router.push({ name: '/Mypage/MyPortfolio' });
      } catch (error) {
        console.error("포트폴리오 저장 실패:", error);
        this.errorMessage = "포트폴리오 저장에 실패했습니다. 다시 시도해주세요.";
      } finally {
        this.isLoading = false;  // 로딩 끝
      }
    },
  },
};
</script>

<style scoped>
.question {
  font-size: 20px;
  margin-bottom: 10px;
  color: #333;
  font-weight: 600;
}

.answer {
  width: 100%;
  max-width: 600px;
  padding: 10px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  background-color: rgb(240, 240, 250);
  transition: border-color 0.3s, box-shadow 0.3s;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.answer:focus {
  border-color: #37a0f4;
  box-shadow: 0 0 8px rgba(55, 160, 244, 0.4);
  background-color: #fff;
  outline: none;
}

.answer:hover {
  border-color: #bbb;
}

.questionBlock {
  margin-bottom: 20px;
}

.error-message {
  color: red;
  font-size: 16px;
  font-weight: bold;
  margin-top: 20px;
}

/* 로딩 오버레이 스타일 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(1, 1, 1, 0.6);    /* 불투명한 배경 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;  /* 다른 요소들 위에 표시 */
}

.loading-spinner {
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid #fff;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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
