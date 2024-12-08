<template>
    <div>
      <!-- 오버레이 (로딩 중일 때만 보이게) -->
      <div v-if="isLoading" class="loading-overlay">
        <div class="loading-spinner"></div>
      </div>
      
      <div class="questionBlock" v-for="(question, index) in questions" :key="index">
        <div class="question">
          {{ question }}
        </div>
        <input
          type="text"
          class="answer"
          v-model="answers[index]" 
        />
      </div>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <SmallButton text="생성하기" @click="submitPortfolioRequest" />
      
      <GPTCreatedPortfolio v-if="portfolioResult" :portfolioResult="portfolioResult" />
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import SmallButton from "../SmallButton.vue";
  import GPTCreatedPortfolio from "./GPTCreatedPortfolio.vue";
  
  export default {
    components: {
      SmallButton,
      GPTCreatedPortfolio,
    },
    data() {
      return {
        questions: [
          "새 포트폴리오 이름",
          "투자 시 고려하는 수익과 위험 밸런스(%)",
          "예상 투자 기간(year)",
          "투자 금액(원)",
          "감수 가능한 손실(%)",
          "기대 수익(%)",
        ],
        answers: ["", "", "", "", ""],
        portfolioResult: "",
        errorMessage: "",
        isLoading: false,  // 로딩 상태
      };
    },
    methods: {
      isFormValid() {
        const isValidNumber = (value) => !isNaN(value) && value.trim() !== '';
        return (
          this.answers[0].trim() !== '' && 
          isValidNumber(this.answers[1]) &&
          isValidNumber(this.answers[2]) &&
          isValidNumber(this.answers[3]) &&
          isValidNumber(this.answers[4])
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
          const response = await axios.post("http://127.0.0.1:8000/portfolio/ai_portfolio/", payload, {
            headers: {
              'Authorization': `Bearer ${token}`,
            }
          });
          this.portfolioResult = response.data;
          console.log(response.data);
        } catch (error) {
          console.error("포트폴리오 요청 실패:", error);
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
    background: rgba(0, 0, 0, 0.5);  /* 불투명한 배경 */
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
  </style>
  