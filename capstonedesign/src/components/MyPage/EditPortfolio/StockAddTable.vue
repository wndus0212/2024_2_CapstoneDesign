<template>
  <div style="display: flex; flex-direction: column;">
    <!-- 검색창 -->
    <div style="margin-bottom: 10px;">
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="종목 이름 또는 티커 검색" 
        class="searchInput" 
      />
    </div>

    <!-- 스크롤 컨테이너 -->
    <div class="scrollContainer" :style="{ width: width, height: height }">
      <div v-if="loading" class="loading">로딩 중...</div>
      <div v-else class="table-wrapper">
        <table class="StockTable">
          <thead>
            <tr>
              <th scope="col">종목</th>
              <th scope="col">현재가</th>
              <th scope="col">거래량</th>
              <th scope="col">시가총액(억)</th>
              <th scope="col">개수</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="stock in filteredStocks" 
              :key="stock.symbols" 
            >
              <td>{{ stock.names }}</td>
              <td>{{ stock.prices }}</td>
              <td>{{ stock.volume }}</td>
              <td>{{ (stock.market_caps / 100000000).toFixed(2) }}</td>
              <td><input type="number" min="0"></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
//import SpinBox from "@/components/SpinBoxComponent.vue";

export default {
  components:{
    //SpinBox
  },
  props: {
    width: {
      type: String,
      default: "1200px",
    },
    height: {
      type: String,
      default: "500px",
    },
  },
  data() {
    return {
      stocks: [], // API에서 받은 데이터를 저장할 변수
      loading: true, // 로딩 상태 추가
      searchQuery: "", // 검색어 입력 상태
    };
  },
  computed: {
    filteredStocks() {
      if (!this.searchQuery) {
        return this.stocks;
      }
      const query = this.searchQuery.toLowerCase();
      // 종목 이름과 티커 모두 검색
      return this.stocks.filter(
        (stock) =>
          stock.names.toLowerCase().includes(query) || // 이름 검색
          stock.symbols.toLowerCase().includes(query) // 티커 검색
      );
    },
  },
  methods: {
    fetchStockRank() {
      this.loading = true; // 로딩 시작

      const url = `http://127.0.0.1:8000/stock/list/KOSPI/market_caps/`;
      console.log(url);
      axios
        .get(url)
        .then((response) => {
          this.stocks = response.data;
          this.sortStocksByMarketCap();
        })
        .catch((error) => {
          console.error("데이터를 불러오는데 실패했습니다:", error);
        })
        .finally(() => {
          this.loading = false; // 로딩 종료
        });
    },
    sortStocksByMarketCap() {
      this.stocks.sort(
        (a, b) => parseFloat(b.Marcap) - parseFloat(a.Marcap)
      );
    },
    navigateTo(stockCode, stockName) {
      this.$router.push({
        path: `/detail/${stockCode}`,
        query: {
          name: stockName,
        },
      });
      console.log("Stock Name:", stockName);
    },
  },
  mounted() {
    this.fetchStockRank(); // 컴포넌트가 마운트될 때 데이터 요청
  },
};
</script>

<style scoped>
.scrollContainer {
  padding: 20px;
  min-width: 500px;
  width: 100%;
  border-radius: 10px;
  margin: 0px 50px;
  height: 100%;
  display: flex;
  background-color: white;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
}

.table-wrapper {
  height: 100%;
  overflow-y: auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: start;
}

.loading {
  font-size: 24px;
  text-align: center;
  width: 100%;
  padding: 20px;
}

.StockTable {
  width: 100%;
  border-collapse: collapse;
  font-size: 20px;
  border: none;
}

.StockTable th {
  width: 200px;
  background-color: #f1f1f1;
}

.StockTable thead th {
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: white;
  border: none;
}

.StockTable tbody tr {
  height: 100px;
  border: none;
}

.StockTable td,
.StockTable th {
  padding: 8px;
  text-align: left;
  border: none;
}

.searchInput {
  width: 100%;
  padding: 10px;
  font-size: 18px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.searchInput:focus {
  outline: none;
  border-color: #007bff;
}
</style>
