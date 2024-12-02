<template>
    <div class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div>
          <BoxTitle>
            포트폴리오 수정
          </BoxTitle>
          <div style="display: flex;">
            <PortfolioPieChart/>
            <myPortfolioChart/>
          </div>

          <div style="width: 100%; display: flex; justify-content: center; margin-top: 20px;">
            <StockAddWidget/>
          </div>

          <div style="display: flex; gap: 20px; margin-left: 50px; margin-top: 50px;">
            <SmallButton text="수정하기"/>
            <SmallButton text="닫기" @click="closeModal"/>
          </div>
        </div>
        
      </div>
    </div>
  </template>
  
  <script>
  import BoxTitle from '@/components/BoxTitle.vue';
  import PortfolioPieChart from '../PortfolioPieChart.vue';
  import SmallButton from '@/components/SmallButton.vue';
  import myPortfolioChart from './myPortfolioTable.vue';
  //import AddAssets from './AddAssets.vue';
  import StockAddWidget from './StockAddWidget.vue';
  export default {
    components:{
      BoxTitle,
      PortfolioPieChart,
      SmallButton,
      myPortfolioChart,
      StockAddWidget
      //AddAssets
    },
    methods: {
      closeModal() {
        this.$emit('close'); // 부모 컴포넌트로 'close' 이벤트 전달
      }
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
  