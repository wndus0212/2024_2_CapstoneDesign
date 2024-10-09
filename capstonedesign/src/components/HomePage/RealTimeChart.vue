<template>
  <div>
    <canvas
      ref="MyChart"/>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)


export default {
  data:() => ({
    type: 'line',
    data: {
      labels: [ '1', '2', '3', '4', '5', '5' ],
      datasets: [{
        label: 'test charts',
        data: [ 12, 19, 3, 5, 2, 3 ],
        borderWidth: 1,
        pointRadius:0
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      },
      plugins:{
        legend: {
            display: false
        },
      }
    }
  }),
  mounted(){
    this.createChart()
  },
  methods:{
    createChart(){
      new Chart(this.$refs.MyChart, {
        type:'line',
        data:this.data,
        options:this.options,
        
      })

    }
  }

}
</script>

<style scoped>
div {
  max-width: 600px;
  margin: auto;
}
</style>
