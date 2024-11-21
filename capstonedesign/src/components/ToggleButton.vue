<template>
<button @click="toggleState">
    {{ label }} {{ isVisible ? '숨기기' : '보기' }}
</button>
</template>

<script>
export default {
    props: {
        label: {
        type: String,
        required: true
        },
        isVisible: {
        type: Boolean,
        required: true
        }
    },
    methods: {
        toggleState() {
            this.$emit('toggle');
        }
    }
}
</script>

<style scoped>
    button {
        padding: 10px;
        margin: 5px;
    }
</style>
