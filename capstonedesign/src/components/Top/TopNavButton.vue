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
        font-size: 26px;
        font-weight: 500;
        color:rgb(111, 114, 121)
    }
    .TopNavButton:hover{
        color: black;
    }
</style>