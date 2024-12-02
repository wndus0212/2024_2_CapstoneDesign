<template>
  <div v-if="isOpen" class="modal" @click.self="closeModal">
    <div class="modal-content">
      <button class="close-btn" @click="closeModal">&times;</button>
      <div class="modal-header">
        <h3>{{ sector.name_ko }}</h3>
      </div>
      <div class="modal-body">
        <h2>
          대표 기업
        </h2>
        <h3>KOSPI</h3>
        <ul>
          <li v-for="stock in kospiStocks" :key="stock.Symbol" @click="navigateTo(stock.Symbol, stock.Name)">
            <span>
              {{ stock.Name }}
            </span>
            <span>
              시가총액: {{ stock.MarketCap.toLocaleString() }}
            </span>
          </li>
        </ul>

        <h3>KOSDAQ</h3>
        <ul>
          <li v-for="stock in kosdaqStocks" :key="stock.Symbol" @click="navigateTo(stock.Symbol, stock.Name)">
            <span>
              {{ stock.Name }}
            </span>
            <span>
              시가총액: {{ stock.MarketCap.toLocaleString() }}
            </span>
          </li>
        </ul>

        <h3>S&P 500</h3>
        <ul>
          <li v-for="stock in sp500Stocks" :key="stock.Symbol" @click="navigateTo(stock.Symbol, stock.Name)">
            <span>
              {{ stock.Name }}
            </span>
            <span>
              시가총액: {{ stock.MarketCap.toLocaleString() }}
            </span>
          </li>
        </ul>
      </div>
      <div class="modal-footer">
        <button @click="closeModal" class="btn-primary">닫기</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      stock_list: [],
    };
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    sector: {
      type: Object,
      required: true,
      default: () => ({ name: "", name_ko: "", description: "" }),
    },
  },
  computed: {
    kospiStocks() {
      return this.stock_list.filter(stock => stock.Market === "KOSPI");
    },
    kosdaqStocks() {
      return this.stock_list.filter(stock => stock.Market === "KOSDAQ");
    },
    sp500Stocks() {
      return this.stock_list.filter(stock => stock.Market === "S&P500");
    },
  },
  watch: {
    sector: {
      handler(newSector) {
        if (newSector && newSector.name) {
          this.fetchStockList();
        }
      },
      immediate: true,
    },
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
    fetchStockList() {
      if (!this.sector || !this.sector.name) {
        console.error("sector 데이터가 올바르지 않습니다:", this.sector);
        return;
      }
      const encodedSectorName = encodeURIComponent(this.sector.name);
      console.log(this.sector.name);
      axios
        .get(`http://127.0.0.1:8000/stock/sector_stock_list/${encodedSectorName}/`)
        .then((response) => {
          this.stock_list = response.data.output;
          console.log("sector_stock_list", this.stock_list);
        })
        .catch((error) => {
          console.error("데이터 로드 중 오류:", error);
        });
    },
    navigateTo(stockCode, stockName) {
      this.$router.push({
        path: `/detail/${stockCode}`,
        query: {
          name: stockName,
        }
      });
      console.log("Stock Name:", stockName);
    }
  },
};
</script>

<style scoped>
/* 모달 배경 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* 모달 콘텐츠 */
.modal-content {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.3s ease-out;
}

/* 헤더 */
.modal-header {
  border-bottom: 1px solid #ddd;
  margin-bottom: 15px;
}

/* 닫기 버튼 */
.close-btn {
  background: none;
  border: none;
  font-size: 1.5em;
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
  color: #333;
}

/* 모달 본문 */
.modal-body {
  margin-bottom: 15px;
  line-height: 1.6;
}

/* 모달 푸터 */
.modal-footer {
  display: flex;
  justify-content: flex-end;
}

/* 버튼 스타일 */
.btn-primary {
  background-color: #007bff;
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.btn-primary:hover {
  background-color: #0056b3;
}

/* 애니메이션 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

h2 {
  color: #007bff;
  margin-bottom: 10px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  padding: 5px 0;
  border-bottom: 1px solid #ddd;
}

li :hover{
  background-color: #f0f8ff; /* 호버 시 배경색 변경 */
  transform: translateY(-2px); /* 살짝 위로 이동하는 효과 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 가벼운 그림자 추가 */
}

li:last-child {
  border-bottom: none;
}

</style>
