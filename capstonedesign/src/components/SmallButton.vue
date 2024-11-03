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
      border: 1px solid rgb(37, 200, 255);
      border-radius: 3px;
      background: white;
      margin-top: 8px;
      height: 30px;
      font-size: 20px;
      box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
    }

    .SmallButton:hover{
      background-color: rgb(37, 200, 255);
      color: white;
    }
</style>