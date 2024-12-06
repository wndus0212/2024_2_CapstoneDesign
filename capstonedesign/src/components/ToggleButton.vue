<template>
    <button @click="toggleState" class="styled-button">
      {{ label }} {{ isVisible ? '숨기기' : '보기' }}
    </button>
  </template>
  
  <script>
  export default {
    props: {
      label: {
        type: String,
        required: true
      },
      isVisible: {
        type: Boolean,
        required: true
      }
    },
    methods: {
      toggleState() {
        this.$emit('toggle');
      }
    }
  };
  </script>
  
  <style scoped>
  .styled-button {
    padding: 12px 20px;
    margin: 5px;
    font-size: 16px;
    font-weight: bold;
    color: #000000;
    border: none;
    border-radius: 25px; /* 버튼 둥글게 */
    cursor: pointer;
    transition: all 0.3s ease; /* 부드러운 애니메이션 */
    background-color: white;
  }
  
  .styled-button:hover {
    transform: translateY(-3px); /* 살짝 떠오르는 효과 */
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15), 0 2px 4px rgba(0, 0, 0, 0.1); /* 더 강한 그림자 */
  }
  
  .styled-button:active {
    transform: translateY(0); /* 클릭 시 원래 위치로 */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.06); /* 클릭 시 그림자 원래대로 */
  }
  </style>
  