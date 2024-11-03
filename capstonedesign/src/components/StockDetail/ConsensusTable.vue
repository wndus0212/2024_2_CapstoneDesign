<template>
    <div class="ConsensusScrollContainer">
        <div class="table-wrapper">
            <BoxTitle>
                전문가 의견
            </BoxTitle>
            <table class="consensus">
                <thead>
                    <tr>
                        <th scope="col">의견</th>
                        <th scope="col">분석가</th>
                        <th scope="col">날짜</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="i in 20" :key="i" @click="navigateTo('StockDetail')">
                        <td>매수</td>
                        <td>TD Cowen</td>
                        <td>204-10-11</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import BoxTitle from '../BoxTitle.vue';
export default {
    components:{
        BoxTitle
    },
};
</script>

<style scoped>
.ConsensusScrollContainer {
    padding: 20px;
    background-color: white;
    box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
    min-width: 500px;
    max-width: 680px; /* 최대 너비로 조정 */
    border-radius: 10px;
    height: 400px; /* 높이 조정 */
    display: flex;
    text-align: left;
    margin: 10px;
}

.table-wrapper {
    max-height: 350px; /* 스크롤되는 높이 설정 */
    overflow-y: auto;
    width: 100%;
}

.consensus {
    width: 100%;
    border-collapse: collapse;
    font-size: 20px;
}

.consensus th {
    width: 100px;
    background-color: #f1f1f1;
}

.consensus thead th {
    position: sticky;
    top: 0;
    z-index: 10;
    background-color: white;
}

.consensus tbody tr {
    height: 80px;
}

.consensus td, .consensus th {
    padding: 8px;
    text-align: left;
    border-bottom: 1px solid #ddd; /* 하단 테두리 추가 */
}
</style>
