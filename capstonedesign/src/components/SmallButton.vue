<template>
  <button :class="['SmallButton', { 'active': active }]">
    {{ text }}
  </button>  
</template>

<script>
export default {
  name: 'SmallButton',
  props: {
    text: {
      type: String,
      required: true
    },
    active: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.SmallButton {
  border: 1px solid rgb(37, 200, 255);
  border-radius: 3px;
  background: white;
  margin-top: 8px;
  height: 30px;
  font-size: 20px;
  box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.SmallButton:hover {
  background-color: rgb(37, 200, 255);
  color: white;
}

.SmallButton.active {
  background-color: rgb(37, 200, 255);
  color: white;
  border-color: rgb(37, 200, 255);
}
</style>
