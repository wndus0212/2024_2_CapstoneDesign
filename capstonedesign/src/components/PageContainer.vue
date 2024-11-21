<template>
    <div style="display: flex; justify-content: center;">
        <div class="pageContainer">
            <slot></slot>
        </div>
    </div>
    
</template>
<script>
export default {
    
}
</script>
<style>
.pageContainer{
    min-width: 1000px;
    max-width: 1250px;
    padding-top: 20px;
}
</style>