<template>
    <button>
        <slot></slot>
    </button>
</template>
<script>
export default {
    name:'TopNavButton'
}
</script>
<style>
    button{
        background-color: transparent;
        border: 0px;
        margin:0px;
        padding: 0px;
        height:100%;
    }
    button:hover{
        background-color: skyblue;
    }
</style>