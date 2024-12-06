<template>
    <div style="display: flex;">
      <div class="scrollContainer" :style="{ width: width, height: height }">
        <div v-if="loading" class="loading">
          <LoadingComponent/>
        </div>
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
                <td>{{ stock.prices.toLocaleString() }}</td>
                <td>{{ stock.volume.toLocaleString() }}</td>
                <td>{{ (stock.market_caps / 100000000).toFixed(2).toLocaleString() }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import LoadingComponent from '@/components/LoadingComponent.vue';

  export default {
    components:{
      LoadingComponent
    },
    props: {
      width: {
        type: String,
        default: '1200px'
      },
      height: {
        type: String,
        default: '700px'
      },
    },
    data() {
      return {
        stocks: [], // API에서 받은 데이터를 저장할 변수
        loading: true, // 로딩 상태 추가
      };
    },

    methods: {
      fetchStockRank() {
        this.loading = true; // 로딩 시작
              
        const url = `https://port-0-capstonedesign-m3vkxnzga0885b97.sel4.cloudtype.app/stock/list/KOSPI/market_caps/`;
        console.log(url);
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
        this.stocks.sort((a, b) => parseFloat(b.Marcap) - parseFloat(a.Marcap));
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
  }
</style>
  