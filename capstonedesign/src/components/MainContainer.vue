<template>
    <div class="mainContainer">
        <slot></slot>
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