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
        background-color: transparent;
        border: 0px;
        margin:0px;
        padding: 0px;
        height:100%;
    }
    .TopNavButton:hover{
        background-color: skyblue;
    }
</style>