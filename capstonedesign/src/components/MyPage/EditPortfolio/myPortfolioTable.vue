<template>
    <div style="display: flex; justify-content: center;">
        <div class="scrollContainer" :style="{ width: width, height: height}">
            <div class="table-wrapper">
                <table class="StockTable">
                    
                </table>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        data: {
            type: String,
            required: true,
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
    border: none
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
    border: none
}

.StockTable tbody tr {
    height: 100px;
    border: none
}

.StockTable td, .StockTable th {
    padding: 8px;
    text-align: left;
    border: none;
}
</style>
