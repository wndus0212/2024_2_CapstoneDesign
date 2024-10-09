<template>
    <TopNav/>
    <div>
      <containerBox>
        <p>
          Details
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
  import TopNav from '../components/Top/Top.vue'
  import containerBox from '../components/Box.vue'
  export default {
    name: 'DetailPage',
    components: {
      TopNav,
      containerBox
    }
  }
  </script>
  
  <style>

  </style>
  