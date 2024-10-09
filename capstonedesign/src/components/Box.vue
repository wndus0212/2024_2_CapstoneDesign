<template>
    <div class="box">
        <slot></slot>
    </div>
</template>
<script>

export default {
    name:'containerBox',
    
}
</script>
<style>
    .box{
        width: 40%;
        border: 1px solid black;
        border-radius: 5px;
        padding: 10px;
        margin: 10px;
        text-align: left;
    }
</style>