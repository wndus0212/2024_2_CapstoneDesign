<template>
    <TopNav/>
    <div>
      <PageTitle>실시간 뉴스</PageTitle>
      <containerBox>
        <p>
          contents
        </p>
      </containerBox>

      <PageTitle>맞춤 핫 토픽</PageTitle>
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
  import PageTitle from '@/components/PageTitle.vue'; 
  export default {
    name: 'ContentsPage',
    components: {
      TopNav,
      containerBox,
      PageTitle
    }
  }
  </script>
  
  <style>

  </style>
  