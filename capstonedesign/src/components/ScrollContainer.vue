<template>
    <div style="display: flex; justify-content: center;">
        <div class="scrollContainer">
            <slot></slot> 
        </div>
    </div>
    
</template>
<script>
export default {
    
}
</script>
<style>
    .scrollContainer{
        overflow-y: auto;
        padding: 20px;
        border: 1px black solid;
        min-width: 500px;
        width: 1200px;
        border-radius: 10px;
        margin:0px 50px;
        height: 700px;   
    }
</style>