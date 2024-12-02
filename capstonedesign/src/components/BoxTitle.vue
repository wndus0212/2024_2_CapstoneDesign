<template>
    <div class="boxTitle">
        <slot></slot>
    </div>
</template>
<script>
export default {
    name:'boxTitle'
}
</script>
<style>
    .boxTitle{
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 20px;
    }
</style>