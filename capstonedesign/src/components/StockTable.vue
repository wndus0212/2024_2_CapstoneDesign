<template>
    <div>
        <table class="StockTable">
            <thead>
                <tr>
                    <th scope="col">종목</th>
                    <th scope="col"></th>
                    <th scope="col">현재가</th>
                    <th scope="col">거래량</th>
                    <th scope="col">시가총액</th>
                    <th scope="col"></th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>삼성전자</td>
                    <td></td>
                    <td>60600</td>
                    <td>23,107,725</td>
                    <td>361조 7688억</td>
                    <td></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
<script>
export default {
    
}
</script>
<style>
    .StockTable{
        border-collapse: 0px;
    }

    .StockTable th{
        width: 200px;
    }
</style>