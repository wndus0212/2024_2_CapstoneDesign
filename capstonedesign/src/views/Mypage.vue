<template>
    <TopNav/>
    <div>
      <containerBox>
        <p>
          MyPage
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
    name: 'MyPage',
    components: {
      TopNav,
      containerBox
    }
  }
  </script>
  
  <style>

  </style>
  