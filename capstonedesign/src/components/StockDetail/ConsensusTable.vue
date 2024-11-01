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
  data() {

  },
};
</script>

<style>
.ConsensusScrollContainer {
    padding: 20px;
    border: 1px solid black;
    min-width: 500px;
    width: 680px !important;
    border-radius: 10px;
    height: 400px !important;
    display: flex;
    text-align: left;
    margin: 10px !important
}

.table-wrapper {
    max-height: 650px; 
    overflow-y: auto;
    width: 100%;
}

.consensus {
    width: 100%;
    border-collapse: collapse;
    font-size: 20px;
    border: none
}

.consensus th {
    width: 100px;
    background-color: #f1f1f1;
}

.consensus thead th {
    position: sticky; /* 헤더 고정 */
    top: 0;
    z-index: 10;
    background-color: white; /* 헤더 배경색 */
    border: none
}

.consensus tbody tr {
    height: 80px;
    border: none
}

.consensus td, .consensus th {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
    border: none
}
</style>
