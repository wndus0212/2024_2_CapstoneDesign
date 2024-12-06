<template>
    <div class="portfolioScrollContainer">
        <div class="table-wrapper">
            <table class="PortfolioTable">
                <tbody>
                    <!-- 추가 데이터 -->
                    <tr v-for="i in 5" :key="i">
                        <td class="portfolioName">포트폴리오 {{ i }}</td>
                        <td class="tendency">위험 중립형</td>
                        <td class="check"><input type="checkbox"></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
export default {};
</script>

<style scoped>
.portfolioScrollContainer {
    padding: 20px;

    border-radius: 15px;
    min-width: 500px;
    width: 850px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
    height: 300px;
    display: flex;  
}

.table-wrapper {
    max-height: 700px; 
    overflow-y: auto; 
    width: 100%;
}

.PortfolioTable {
    width: 100%;
    border-collapse: collapse;
    font-size: 20px;
}

.PortfolioTable th {
    width: 200px;
    background-color: #f1f1f1;
}

.PortfolioTable tbody tr {
    height: 70px;
}

.PortfolioTable td, .PortfolioTable th {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

.portfolioName{
    width: 30%;
}

.check{
    width: 7%
}
</style>
