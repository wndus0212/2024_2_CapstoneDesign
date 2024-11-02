<template>
    <div class="box">
        <div style="margin: 20px">
            <slot></slot>
        </div>
        
    </div>
</template>
<script>

export default {
    name:'containerBox',
    
}
</script>
<style>
    .box{
        width: 700px;
        min-width: 229px;
        border-radius: 5px;
        padding: 10px;
        margin: 10px;
        text-align: left;
        background-color: white;
        box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
    }
</style>