<template>
    <div style="display: flex; justify-content: center;">
        <div class="scrollContainer">
            <div class="table-wrapper" v-if="stocks.length > 0">
                <table class="StockTable">
                    <thead>
                        <tr>
                            <th scope="col">종목</th>
                            <th scope="col">현재가</th>
                            <th scope="col">개수</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="stock in parsedStocks" :key="stock.symbols">
                            <td v-if="stock.allocation !== 0">{{ stock.names }}</td>
                            <td v-if="stock.allocation !== 0">{{ stock.prices*stock.allocation }}</td>
                            <td v-if="stock.allocation !== 0">{{ stock.allocation }}</td>

                            
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-else>
                <p>로딩 중...</p> <!-- 데이터가 없으면 로딩 중 메시지 표시 -->
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        addedStock: {
            type: Array,  // addedStock은 배열이어야 함
            required: true,
        },
    },
    data() {
        return {
            stocks: [],  // 초기화된 배열
        };
    },
    mounted() {
        // 컴포넌트가 마운트되면 addedStock 데이터를 stocks에 할당
        this.stocks = this.addedStock;
        console.log("myportfoliotable this.stocks", this.addedStock);
    },
    watch: {
        // addedStock이 업데이트되면 stocks 배열도 업데이트
        addedStock(newStock) {
            this.stocks = newStock;
        },
    },
    computed: {
        // stocks 배열을 표시할 데이터로 변환
        parsedStocks() {
            return this.stocks;
        },
    },
};
</script>

<style scoped>
.scrollContainer {
    width: 600px;
    height: 700px;
    padding: 20px;
    min-width: 500px;
    border-radius: 10px;
    margin: 0px 50px;
    height: 90%;
    display: flex;
    background-color: white;
    box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
}

.table-wrapper {
    max-height: 90%;
    overflow-y: auto;
    width: 100%;
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
