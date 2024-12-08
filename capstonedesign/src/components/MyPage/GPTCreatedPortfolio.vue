<template>
    <div>
      <BoxTitle>
        Chat GPT 생성 포트폴리오
      </BoxTitle>
      <Box>

      </Box>
      <SmallButton text="저장하기"></SmallButton>

    </div>
  </template>
  
  <script>
  import BoxTitle from '@/components/BoxTitle.vue';
  import SmallButton from '@/components/SmallButton.vue';
  import Box from '../Box.vue';
  export default {
    components:{
      BoxTitle,
      SmallButton,
      Box
    },
    methods: {
    }
  };
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.5); /* 어두운 배경 */
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    z-index: 1001;
    display: flex;
    justify-content: center;
    height: 90%;
    overflow: scroll;
  }
  </style>
  