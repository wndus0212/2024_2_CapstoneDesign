<template>
    <div class="select-box" :style="{ width: width }">
        <select :value="modelValue || options[0]?.value" @change="updateValue($event.target.value)">
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
        modelValue: {
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
            // 모델 값 업데이트 이벤트 호출
            this.$emit('update:modelValue', selectedValue);
        }
    }
}
</script>

<style scoped>
.select-box{
    
    margin-right:10px;
}

.select-box select {
    width: 100%;
    padding: 8px;
    font-size: 16px;
    border-radius: 10px;
    border: none;
    background-color: rgb(240, 240, 250);
    margin-bottom: 20px;
}
</style>
