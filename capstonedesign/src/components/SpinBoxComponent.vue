<template>
    <div class="spinbox">
      <button class="spinbox-button" @click="decrement">▲</button>
      <input 
        type="number" 
        v-model.number="internalValue" 
        :min="min" 
        :max="max" 
        class="spinbox-input"
        @input="onInput"
      />
      <button class="spinbox-button" @click="increment">▼</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SpinBoxComponent',
    props: {
      value: {
        type: Number,
        default: 0,
      },
      min: {
        type: Number,
        default: 0, // 최소값 설정
      },
      max: {
        type: Number,
        default: Infinity, // 최대값 설정
      },
    },
    data() {
      return {
        // prop의 값은 직접 수정하지 않고, 내부 데이터로 복사하여 사용
        internalValue: this.value,
      };
    },
    watch: {
      // 외부 value 값이 변경되면 내부 값을 동기화
      value(newValue) {
        this.internalValue = newValue;
      },
    },
    methods: {
      increment() {
        if (this.internalValue < this.max) {
          this.internalValue++;
          this.$emit('update:value', this.internalValue); // 부모에 새로운 값 전달
        }
      },
      decrement() {
        if (this.internalValue > this.min) {
          this.internalValue--;
          this.$emit('update:value', this.internalValue); // 부모에 새로운 값 전달
        }
      },
      onInput() {
        if (this.internalValue < this.min) {
          this.internalValue = this.min;
        } else if (this.internalValue > this.max) {
          this.internalValue = this.max;
        }
        this.$emit('update:value', this.internalValue); // 부모에 새로운 값 전달
      },
    },
  };
  </script>
  
  <style scoped>
  .spinbox {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .spinbox-button {
    background-color: #f1f1f1;
    border: 1px solid #ccc;
    padding: 5px;
    cursor: pointer;
  }
  
  .spinbox-button:hover {
    background-color: #e0e0e0;
  }
  
  .spinbox-input {
    width: 60px;
    text-align: center;
    border: 1px solid #ccc;
    padding: 5px;
    margin: 0 5px;
    font-size: 16px;
  }
  
  .spinbox-input:focus {
    outline: none;
    border-color: #007bff;
  }
  </style>
  