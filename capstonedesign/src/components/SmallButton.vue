<template>
    <div>
      <button class="SmallButton">
        <slot></slot>
      </button>  
    </div>
</template>
<script>
export default {
    name: 'SmallButton'
}
</script>
<style>
    .SmallButton{
      border: 1px solid black;
      border-radius: 3px;
      background: white;
      margin-top: 8px;
    }

    .SmallButton:hover{
      background-color: lightblue;
      color: white;
    }
</style>