<template>
    <div v-if="isOpen" class="modal" @click.self="closeModal">
      <div class="modal-content" @click.stop>
        <span class="close-btn" @click="closeModal">&times;</span>
        <h3>{{ sector.name_ko}}</h3>
        <p>{{ sector.description }}</p>
        <!-- 여기에 섹터의 상세 정보를 넣으세요 -->
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      isOpen: {
        type: Boolean,
        required: true,
      },
      sector: {
        type: Object,
        required: true,
      },
    },
    methods: {
      closeModal() {
        this.$emit("close"); // 부모 컴포넌트에게 모달을 닫도록 알림
      },
    },
  };
  </script>
  
  <style scoped>
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    overflow: hidden;
  }
  
  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    width: 300px;
    position: relative;
  }
  
  .close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 1.5em;
    cursor: pointer;
  }
  
  .modal-content {
    cursor: pointer;
  }
  </style>
  