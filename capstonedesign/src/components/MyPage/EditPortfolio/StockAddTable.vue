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
    <div class="scrollContainer">
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
              <td>
                <input 
                  type="number" 
                  min="0" 
                  v-model="stock.allocation" 
                  @input="updateStockQuantity(stock)" 
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    addedStock: {
      type: Array,
      required: true,
      
    },
    selectedOption1: String,
    selectedOption2: String,
    selectedOption3: String,
    selectedOption4: String,
    selectedOption5: String
  },
  data() {
    return {
      localAddedStock: [...this.addedStock], // prop 데이터를 로컬로 복사
      stocks: [], // API에서 받아온 데이터
      loading: true, // 로딩 상태
      searchQuery: "", // 검색어 상태
    };
  },
  watch: {
    // 부모 컴포넌트에서 prop이 변경되면 로컬 데이터도 동기화
    addedStock(newVal) {
      this.localAddedStock = [...newVal];
    },
    selectedOption1() {
      this.fetchStockRank();
    },
    selectedOption2() {
      this.fetchStockRank();
    },
    selectedOption3() {
      this.fetchStockRank();
    },
    selectedOption4() {
      this.fetchStockRank();
    }
  },
  computed: {
    filteredStocks() {
      if (!this.searchQuery) {
        return this.stocks;
      }
      const query = this.searchQuery.toLowerCase();
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
      let market = '';
      let sort = '';
      
      if(this.selectedOption1 === 'KOR'){
        market = "list/";
      } else {
        market = "list_global/";
      }

      if(this.selectedOption2 === 'Stock'){
        market = market + this.selectedOption3;
      } else {
        if(this.selectedOption1 === 'KOR'){
          market = market + "KOR_ETF";
        } else {
          market = market + "GLB_ETF";
        }
      }

      sort = this.selectedOption4;
      console.log(this.selectedOption4)
      const url = `https://web-capstonedesignfront-m3vkxnzga0885b97.sel4.cloudtype.app/stock/${market}/${sort}/`;
      axios
        .get(url)
        .then(response => {
          this.stocks = response.data;
          this.sortStocksByMarketCap();
        })
        .catch(error => {
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
    updateStockQuantity(stock) {
      // allocation 값이 비어 있으면 0으로 설정
      if (stock.allocation === "") {
        stock.allocation = 0;
      }
      
      // 기존 로컬 데이터 업데이트
      const updatedStocks = this.localAddedStock.map((item) =>
        item.symbols === stock.symbols
          ? { ...item, allocation: stock.allocation }  // allocation 값도 함께 업데이트
          : item
      );

      // 새로운 주식 추가
      const isNewStock = !this.localAddedStock.some((item) => item.symbols === stock.symbols);
      if (isNewStock) {
        updatedStocks.push({ ...stock, allocation: stock.allocation }); // 새로운 주식과 allocation 값을 함께 추가
      }
      // 로컬 데이터 갱신
      this.localAddedStock = updatedStocks;

      // 부모 컴포넌트로 데이터 전달
      this.$emit("addedstock", this.localAddedStock);
    },
  },
  mounted() {
    this.fetchStockRank();
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
