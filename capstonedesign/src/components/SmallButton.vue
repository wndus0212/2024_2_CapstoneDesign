<template>
      <button class="SmallButton">
        {{ text }}
      </button>  
</template>
<script>
export default {
    name: 'SmallButton',
    props:{
      text:{
        type: String,
        required:true
      }
    }
}
</script>
<style scoped>
    .SmallButton{
      border: 1px solid black;
      border-radius: 3px;
      background: white;
      margin-top: 8px;
      height: 30px;
      font-size: 20px;
    }

    .SmallButton:hover{
      background-color: lightblue;
      color: white;
    }
</style>