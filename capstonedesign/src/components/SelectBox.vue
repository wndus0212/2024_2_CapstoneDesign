<template>
    <div class="select-box" :style="{ width: width, height: height }">
        <select :value="value" @change="updateValue($event.target.value)">
            <option v-for="(option, index) in options" :key="index" :value="option.value">
                {{ option.label }}
            </option>
        </select>
    </div>
</template>

<script>
export default {
    name: 'SelectBox',
    props: {
        options: {
            type: Array,
            required: true
        },
        value: {
            type: String,
            default: ''
        },
        width: {
            type: String,
            default: '300px' // 기본 너비
        },
    },
    methods: {
        updateValue(selectedValue) {
            this.$emit('input', selectedValue);
        }
    }
}
</script>

<style scoped>
.select-box select {
    width: 100%;
    padding: 8px;
    font-size: 16px;
    border-radius: 4px;
    border: 1px solid #ccc;
    background-color: #fff;
    margin-bottom: 20px;
}
</style>
