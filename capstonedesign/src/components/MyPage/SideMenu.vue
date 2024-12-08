<template>
    <div style="margin: 0px 60px; width: 200px;">
      <SmallButton @click="navigateTo('/MyPage/MyPortfolio')" class="menuButton" text="내 포트폴리오">
      </SmallButton>
      <SmallButton @click="navigateTo('/MyPage/AddPortfolio')" class="menuButton" text="포트폴리오 생성">
      </SmallButton>
    </div>
  </template>
  <script>
  import SmallButton from '../SmallButton.vue';
  export default {
    components: {
      SmallButton
    },
    methods: {
      navigateTo(route) {
        this.$router.push(route); // Vue Router를 사용해 라우트 변경
      }
    }
  };
  </script>
  <style scoped>
  .menuButton {
    width: 200px;
    height: 70px !important;
    margin-top: 30px;
    font-size: 20px;
    font-weight: bold;
    margin-left: auto;
    margin-right: auto;
    padding: 10px 20px;
    border: none;
    border-radius: 12px; /* 둥근 모서리 */
    background-color: #6dbdff;
    color: #fff;
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* 그림자 효과 */
    transition: all 0.3s ease-in-out; /* 부드러운 애니메이션 */
    text-align: center;
  }
  
  /* 호버 효과 */
  .menuButton:hover {
    transform: translateY(-3px); /* 살짝 위로 이동 */
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3); /* 강조된 그림자 */
  }
  
  /* 클릭 시 효과 */
  .menuButton:active {
    transform: translateY(0); /* 원래 위치로 돌아옴 */
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* 기본 그림자 */
  }
  </style>
  