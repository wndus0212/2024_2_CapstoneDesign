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
      
      const url = `http://port-0-capstonedesign-m3vkxnzga0885b97.sel4.cloudtype.app/stock/${market}/${sort}/`;
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
}

.StockTable tbody tr {
  height: 100px;
}

.StockTable td, .StockTable th {
  padding: 8px;
  text-align: left;
  border: none;

}

.StockTable tbody tr {
  height: 100px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.StockTable tbody tr:hover {
  background-color: #f0f8ff; /* 호버 시 배경색 변경 */
  transform: translateY(-2px); /* 살짝 위로 이동하는 효과 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 가벼운 그림자 추가 */
}

.table-wrapper::-webkit-scrollbar {
  width: 12px; /* 세로 스크롤바의 너비 */
  height: 12px; /* 가로 스크롤바의 높이 */
}

.table-wrapper::-webkit-scrollbar-track {
  background: #f1f1f1; /* 스크롤 트랙(배경) 색상 */
}

.table-wrapper::-webkit-scrollbar-thumb {
  background: #888; /* 스크롤 핸들 색상 */
  border-radius: 4px; /* 핸들 모서리 둥글게 */
}

.table-wrapper::-webkit-scrollbar-thumb:hover {
  background: #555; /* 핸들에 마우스 오버 시 색상 */
}

</style>
