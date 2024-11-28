<template>
    <div class="diff_container" style="width: 200px">
      <div style="display: flex">
        <div>
          <div class="chart-name">
            {{ this.data['name_ko'] }}
          </div>
  
          <div>
            하루 변화량: {{ formattedChange }}
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      data: {
        type: Object,
        required: true
      },
    },
    computed: {
      formattedChange() {
        const change = this.data['1 Day Change per'];
        return change !== undefined && change !== null
          ? change.toFixed(2) // 소수점 2자리로 제한
          : 'N/A'; // 데이터가 없을 경우 표시할 값
      }
    }
  };
  </script>
  
  <style>
  .diff_container {
    background-color: rgb(240, 240, 250);
    border-radius: 15px;
    padding: 15px;
    width: 200px;
  }
  
  .chart-name {
    font-weight: 500;
  }
  </style>
  