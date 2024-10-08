<template>
    <TopNav/>
    <div>
      <containerBox>
        <p>
          hello
        </p>
      </containerBox>
      <containerBox>
        <p>
          hello
        </p>
      </containerBox>
      <containerBox>
        <p>
          hello
        </p>
      </containerBox>
    </div>
  </template>
  
  <script>
  import TopNav from './components/Top.vue'
  import containerBox from './components/Box.vue'
  export default {
    name: 'App',
    components: {
      TopNav,
      containerBox
    }
  }
  </script>
  
  <style>

  </style>
  