<template>
    <div style="display: flex; justify-content: center;">
        <div class="scrollContainer">
            <div class="table-wrapper">
                <table class="StockTable">
                    <thead>
                        <tr>
                            <th scope="col">종목</th>
                            <th scope="col"></th>
                            <th scope="col">현재가</th>
                            <th scope="col">거래량</th>
                            <th scope="col">시가총액</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="i in 20" :key="i" @click="navigateTo('StockDetail')">
                            <td>삼성전자</td>
                            <td></td>
                            <td>60600</td>
                            <td>23,107,725</td>
                            <td>361조 7688억</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  data() {

  },
  methods: {
    navigateTo(route) {
      this.$router.push(route);  // 해당 경로로 페이지 이동
    }
  }
};
</script>

<style>
.scrollContainer {
    padding: 20px;
    border: 1px solid black;
    min-width: 500px;
    width: 1200px;
    border-radius: 10px;
    margin: 0px 50px;
    height: 700px;
    display: flex;
    
}

.table-wrapper {
    max-height: 700px; /* 스크롤되는 높이 설정 */
    overflow-y: auto; /* 수직 스크롤 */
    width: 100%;
}

.StockTable {
    width: 100%;
    border-collapse: collapse;
    font-size: 20px;
    border: none
}

.StockTable th {
    width: 200px;
    background-color: #f1f1f1;
}

.StockTable thead th {
    position: sticky; /* 헤더 고정 */
    top: 0;
    z-index: 10;
    background-color: white; /* 헤더 배경색 */
    border: none
}

.StockTable tbody tr {
    height: 100px;
    border: none
}

.StockTable td, .StockTable th {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
    border: none
}
</style>
