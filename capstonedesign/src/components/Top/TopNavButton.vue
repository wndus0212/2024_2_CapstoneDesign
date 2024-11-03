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
        width: 150px;
        background-color: transparent;
        border: 0px;
        margin:0px;
        padding: 0px;
        height:100%;
        font-size: 24px;
    }
    .TopNavButton:hover{
        border-bottom: 3px solid rgb(37, 200, 255);
    }
</style>