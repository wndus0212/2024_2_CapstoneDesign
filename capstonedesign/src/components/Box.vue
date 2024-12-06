<template>
    <div class="box" :style="{ width: width, height: height }">
        <div style="margin: 20px">
            <slot></slot>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ContainerBox',
    props: {
        width: {
            type: String,
            default: '700px' // 기본 너비
        },
        height: {
            type: String,
            default: 'auto'  // 기본 높이, 내용에 따라 자동 조정
        }
    }
}
</script>

<style scoped>
.box {
    min-width: 229px;
    border-radius: 5px;
    padding: 10px;
    margin: 10px;
    text-align: left;
    background-color: white;
    
}
</style>
