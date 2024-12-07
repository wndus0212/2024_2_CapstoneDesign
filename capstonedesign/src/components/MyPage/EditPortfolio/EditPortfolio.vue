<template>
    <div class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div>
          <BoxTitle>
            포트폴리오 수정
          </BoxTitle>
          <div style="display: flex;">
            <PortfolioAddPieChart :stocks="portfolioStocks"/>
            <myPortfolioChart :addedStock="addedStock"/>
          </div>

          <div style="width: 100%; display: flex; justify-content: center; margin-top: 20px;">
            <StockAddWidget :addedStock="addedStock"/>
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
  import axios from 'axios';
  import BoxTitle from '@/components/BoxTitle.vue';
  import PortfolioAddPieChart from './PortfolioAddPieChart.vue';
  import SmallButton from '@/components/SmallButton.vue';
  import myPortfolioChart from './myPortfolioTable.vue';
  //import AddAssets from './AddAssets.vue';
  import StockAddWidget from './StockAddWidget.vue';
  export default {
    components:{
      BoxTitle,
      PortfolioAddPieChart,
      SmallButton,
      myPortfolioChart,
      StockAddWidget
      //AddAssets
    },
    props:{
      portfolioId:{
        type: Number,
        required: true,
      },
    },
    data(){
      return {
          portfolioStocks: [],
          addedStock:[],
      }
    },
    mounted() {
        // API 호출하여 포트폴리오 목록을 가져옴
        this.fetchPortfolioStocks(this.portfolioId)
    },
    methods: {
      closeModal() {
        this.$emit('close'); // 부모 컴포넌트로 'close' 이벤트 전달
      },
      fetchPortfolioStocks(newPortfolioId) {
            if (!newPortfolioId) {
                this.portfolioStocks = [];
                return;
            }

            const token = localStorage.getItem("token");
            axios.get(`http://127.0.0.1:8000/portfolio/portfolios/stock_list/${newPortfolioId}/`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            })
            .then(response => {
                this.portfolioStocks = response.data; // 포트폴리오 종목 데이터 저장
            })
            .catch(error => {
                console.error(error);
            });
        },
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
  