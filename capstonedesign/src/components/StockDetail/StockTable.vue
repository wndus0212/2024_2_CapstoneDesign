<template>
  <div style="display: flex;">
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
            </tr>
          </thead>
          <tbody>
            <tr v-for="stock in stocks" :key="stock.symbols" @click="navigateTo(stock.symbols, stock.names)">
              <td>{{ stock.names }}</td>
              <td>{{ formatPrice(stock.prices) }}</td>
              <td>{{ stock.volume.toLocaleString() }}</td>
              <td>{{ formatPrice((stock.market_caps / 100000000).toFixed(2)) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    width: {
      type: String,
      default: '1200px'
    },
    height: {
      type: String,
      default: '700px'
    },
    selectedOption1: String,
    selectedOption2: String,
    selectedOption3: String,
    selectedOption4: String,
    selectedOption5: String
  },
  data() {
    return {
      stocks: [], // API에서 받은 데이터를 저장할 변수
      loading: true, // 로딩 상태 추가
    };
  },
  watch: {
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
      
      const url = `http://127.0.0.1:8000/stock/${market}/${sort}/`;
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
    
    // 가격 단위 표시 함수
    formatPrice(value) {
      if (this.selectedOption1 === 'KOR') {
        return value.toLocaleString() + ' 원'; // 한국 원화
      } else {
        return value.toLocaleString() + ' $'; // 글로벌 달러
      }
    },
    
    sortStocksByMarketCap() {
      this.stocks.sort((a, b) => parseFloat(b.Marcap) - parseFloat(a.Marcap));
    },
    
    navigateTo(stockCode, stockName) {
      // selectedOption1에 따른 unit 값을 설정
      const unit = this.selectedOption1 === 'KOR' ? '원' : '$';
      console.log(unit)
      this.$router.push({
        path: `/detail/${stockCode}`,
        query: {
          name: stockName,
          unit: unit 
        }
      });
    }
  },
  mounted() {
    this.fetchStockRank(); // 컴포넌트가 마운트될 때 데이터 요청
  }
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
  box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
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

.StockTable td, .StockTable th {
  padding: 8px;
  text-align: left;
  border: none;
}
</style>
