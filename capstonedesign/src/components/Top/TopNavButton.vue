<template>
    <button class="TopNavButton">
        <slot></slot>
    </button>
</template>
<script>
export default {
    name:'TopNavButton'
}
</script>
<style>
    .TopNavButton{
        width: 100px;
        background-color: transparent;
        border: 0px;
        margin:0px;
        padding: 0px;
        height:100%;
        font-size: 20px;
    }
    .TopNavButton:hover{
        background-color: skyblue;
    }
</style>