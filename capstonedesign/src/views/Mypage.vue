<template>
    <TopNav/>
    <MainContainer>
      <div style="height: 120px;"></div>
      <PageTitle>마이페이지</PageTitle>
      <div style="display: flex; min-width: 1000px; margin-right: 250px;">
        <SideMenu/>
        <div style=" width: 100%;  display: flex; justify-content: center;">
          <RouterView></RouterView>
        </div>
        
      </div>
    </MainContainer>
    
  </template>
  
  <script>
  import TopNav from '../components/Top/Top.vue'
  import PageTitle from '@/components/PageTitle.vue';
  import SideMenu from '@/components/MyPage/SideMenu.vue';
  import MainContainer from '@/components/MainContainer.vue';
  export default {
    name: 'MyPage',
    components: {
      TopNav,
      PageTitle,
      SideMenu,
      MainContainer
    },
    methods: {
      
    }
  }
  </script>
  
  <style>

  </style>
  