<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div>
        <BoxTitle>
          포트폴리오 수정
        </BoxTitle>
        <div style="display: flex;">
          <!-- addedStock을 전달하여 종목을 보여줍니다 -->
          <PortfolioAddPieChart :addedStock="addedStock"/>
          <myPortfolioTable :addedStock="addedStock"/>
        </div>

        <div style="width: 100%; display: flex; justify-content: center; margin-top: 20px;">
          <!-- StockAddWidget에서 종목을 추가하거나 수정 -->
          <StockAddWidget @addedstock="updateStockList" :addedStock="addedStock"/>
        </div>

        <div style="display: flex; gap: 20px; margin-left: 50px; margin-top: 50px;">
          <SmallButton 
            text="수정하기" 
            :disabled="isUpdating" 
            @click="updatePortfolioStocks"
          />
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
import myPortfolioTable from './myPortfolioTable.vue';
import StockAddWidget from './StockAddWidget.vue';

export default {
  components: {
    BoxTitle,
    PortfolioAddPieChart,
    SmallButton,
    myPortfolioTable,
    StockAddWidget,
  },
  props: {
    portfolioId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      portfolioStocks: [],
      addedStock: [],
      isUpdating: false, // 수정 중 상태 관리
    };
  },
  mounted() {
    this.fetchPortfolioStocks(this.portfolioId);
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
    fetchPortfolioStocks(newPortfolioId) {
      if (!newPortfolioId) {
        this.portfolioStocks = [];
        return;
      }

      const token = localStorage.getItem("token");
      axios.get(`https://port-0-capstonedesign-m3vkxnzga0885b97.sel4.cloudtype.app/portfolio/portfolios/stock_list/${newPortfolioId}/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
      .then(response => {
        this.portfolioStocks = response.data;
        this.addedStock = response.data;
        console.log("editportfolio addedStock:", this.addedStock);
      })
      .catch(error => {
        console.error(error);
      });
    },
    updateStockList(stock) {
      console.log(stock);
      this.addedStock = stock;
      console.log("edit", this.addedStock);
    },
    updatePortfolioStocks() {
      // 수정 중 상태 활성화
      this.isUpdating = true;

      const token = localStorage.getItem("token");
      const requests = this.addedStock.map(stock =>
        axios.put(
          `https://port-0-capstonedesign-m3vkxnzga0885b97.sel4.cloudtype.app/portfolio/portfolios/stock_list/${this.portfolioId}/`,
          {
            symbols: stock.symbols,
            allocation: stock.allocation,
          },
          {
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          }
        )
      );

      // 모든 요청이 완료되면 상태 업데이트
      Promise.all(requests)
        .then((responses) => {
          console.log("포트폴리오 종목 추가 완료:", responses);
        })
        .catch((error) => {
          console.error("종목 추가 실패:", error);
        })
        .finally(() => {
          this.isUpdating = false; // 수정 완료 후 비활성화
        });

        this.closeModal()
    },
  },
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
