<template>
  <div style="display: flex;">
      <div class="scrollContainer" :style="{ width: width, height: height,}">
          <div class="table-wrapper">
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
                    <tr v-for="stock in stocks" :key="stock.Code" @click="navigateTo(stock.Code)">
                        <td>{{ stock.Name }}</td>
                        <td>{{ stock.Close }}</td>
                        <td>{{ stock.Volume }}</td>
                        <td>{{ stock.Marcap/100000000 }}</td>
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
    stocks: [],  // API에서 받은 데이터를 저장할 변수
  };
},
methods: {
  fetchStockRank() {
    if(this.selectedOption1=="KOR"){
      axios
        .get("http://127.0.0.1:8000/stock/list/KRX/")  // Django에서 제공하는 API 호출
        .then(response => {
          this.stocks = response.data;  // 받아온 데이터를 stockData에 저장
          this.sortStocksByMarketCap();  // 시가총액 기준으로 정렬
        })
        .catch(error => {
          console.error("데이터를 불러오는데 실패했습니다:", error);
        });
    }else{
      axios
        .get("http://127.0.0.1:8000/stock/list/NASDAQ/")  // Django에서 제공하는 API 호출
        .then(response => {
          this.stocks = response.data;  // 받아온 데이터를 stockData에 저장
          this.sortStocksByMarketCap();  // 시가총액 기준으로 정렬
        })
        .catch(error => {
          console.error("데이터를 불러오는데 실패했습니다:", error);
        });
    }
    
  },
  sortStocksByMarketCap() {
    this.stocks.sort((a, b) => {
        const marcapA = parseFloat(a.Marcap);  // 시가총액 값 숫자로 변환
        const marcapB = parseFloat(b.Marcap);  // 시가총액 값 숫자로 변환
        return marcapB - marcapA;  // 내림차순 정렬
      });
  },
  navigateTo(stockCode) {
    this.$router.push({
      path: `/detail/${stockCode}`,  // path에 stockCode를 포함한 URL 설정
    });
    console.log(stockCode);
  }
},
mounted() {
  this.fetchStockRank();  // 컴포넌트가 마운트될 때 데이터 요청
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
  flex-direction:column;
  justify-content: start; 
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
