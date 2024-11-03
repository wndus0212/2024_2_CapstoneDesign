<template>
    <div style="display: flex; justify-content: center;">
        <div class="FinancialScrollContainer">
            <div class="table-wrapper">
                <table class="FinancialStatement">
                    <tbody>
                        <tr>
                            <td>
                                매출총이익률
                            </td>
                            <td>
                                100,000,000
                            </td>
                        </tr>
                        <tr>
                            <td>
                                영업이익률
                            </td>
                            <td>
                                100,000,000
                            </td>
                        </tr>
                        <tr>
                            <td>
                                순이익률
                            </td>
                            <td>
                                100,000,000
                            </td>
                        </tr>
                        <tr>
                            <td>
                                투자수익률
                            </td>
                            <td>
                                100,000,000
                            </td>
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
};
</script>

<style>
.FinancialScrollContainer {

    min-width: 500px;
    width: 1200px;
    border-radius: 10px;

    height: 500px;
    display: flex;
    
}

.table-wrapper {
    max-height: 700px; /* 스크롤되는 높이 설정 */
    overflow-y: auto; /* 수직 스크롤 */
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.FinancialStatement {
    width: 100%;
    border-collapse: collapse;
    font-size: 20px;
    border: none
}

.FinancialStatement th {
    width: 200px;
    background-color: #f1f1f1;
}

.FinancialStatement tbody tr {
    font-size: 30px;
    height: 100px;
    border: 1px solid lightgray;
}

.FinancialStatement td, .FinancialStatement th {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
    border: none
}
</style>
