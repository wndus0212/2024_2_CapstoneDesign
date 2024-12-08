<template>
  <button :class="['SmallButton', { 'active': active }]" >
    {{ text }}
  </button>
</template>

<script>
export default {
  name: 'SmallButton',
  props: {
    text: {
      type: String,
      required: true
    },
    active: {
      type: Boolean,
      default: false
    }
  }
};
</script>

<style scoped>
.SmallButton {
  display: inline-block;
  border: none;
  border-radius: 12px; /* 둥근 모서리 */
  background-color: #6dbdff;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease; /* 부드러운 애니메이션 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
  margin-bottom: 10px;
  margin-top: 10px;
}

/* 호버 효과 */
.SmallButton:hover {
  transform: translateY(-2px); /* 위로 살짝 이동 */
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.2); /* 더 강조된 그림자 */
}

/* 클릭 효과 */
.SmallButton:active {
  transform: translateY(2px); /* 살짝 아래로 눌린 효과 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 클릭 시 그림자 줄임 */
}

/* 활성 상태 (active) */
.SmallButton.active {
  color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15); /* 강조된 그림자 */
}
</style>
