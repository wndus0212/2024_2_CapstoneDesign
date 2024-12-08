<template>
    <div>
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
      <!-- 유효성 검사 실패 시 메시지 출력 -->
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <SmallButton text="생성하기" @click="submitPortfolioRequest" />
      
      <GPTCreatedPortfolio />
  
      
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
        answers: ["", "", "", "", ""], // 사용자 입력 저장
        isModalOpen: false, // 모달 상태 관리
        portfolioResult: "", // Python 결과 저장
        errorMessage: "", // 에러 메시지 상태 추가
      };
    },
    methods: {
      // 유효성 검사 함수
      isFormValid() {
        // 이름 외에는 숫자 입력 검증
        const isValidNumber = (value) => !isNaN(value) && value.trim() !== '';
        return (
          this.answers[0].trim() !== '' && // 포트폴리오 이름은 반드시 있어야 함
          isValidNumber(this.answers[1]) && // 수익과 위험 밸런스는 숫자여야 함
          isValidNumber(this.answers[2]) && // 투자 기간은 숫자여야 함
          isValidNumber(this.answers[3]) && // 감수 가능한 손실은 숫자여야 함
          isValidNumber(this.answers[4])    // 기대 수익은 숫자여야 함
        );
      },
  
      // 포트폴리오 요청 보내기
      async submitPortfolioRequest() {
        if (!this.isFormValid()) {
          this.errorMessage = "모든 항목을 올바르게 입력해 주세요."; // 유효하지 않으면 에러 메시지 표시
          return; // 유효하지 않으면 함수 종료
        }
  
        // 에러 메시지를 초기화
        this.errorMessage = "";
  
        const payload = {
            name: this.answers[0],
            strategy: this.answers[1], // 투자 전략
            duration: this.answers[2], // 예상 투자 기간
            amount: parseInt(this.answers[3]), // 투자 금액
            risk_tolerance: parseFloat(this.answers[4]), // 리스크 감수 범위
            goal: parseFloat(this.answers[5]), // 목표 수익
            market: "국내", // 시장 (고정값)
        };
  
        try {
          const response = await axios.post("http://127.0.0.1:8000/portfolio/ai_portfolio/", payload);
          this.portfolioResult = response.data;
          console.log(response.data);
          this.isModalOpen = true; // 결과 표시를 위해 모달 열기
        } catch (error) {
          console.error("포트폴리오 요청 실패:", error);
        }
      },
  
      closeModal() {
        this.isModalOpen = false; // 모달 닫기
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
  
  /* 에러 메시지 스타일 */
  .error-message {
    color: red;
    font-size: 16px;
    font-weight: bold;
    margin-top: 20px;
  }
  </style>
  