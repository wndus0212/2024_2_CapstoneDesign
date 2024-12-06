<template>
    <div class="mainContainer">
        <div>
            <slot></slot>
        </div>
        
    </div>
</template>
<script>
export default {
    name:'MainContainer'
}
</script>
<style>
    .mainContainer{
        display:flex;
        min-width: 1000px;
        flex-wrap: wrap;
        justify-content: center;
    }
</style>