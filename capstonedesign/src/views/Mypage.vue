<template>
    <TopNav/>
    <div style="height: 120px;"></div>
    <PageTitle>마이페이지</PageTitle>
    <div style="display: flex; min-width: 1000px; margin-right: 250px;">
      <SideMenu/>
      <div style=" width: 100%;  display: flex; justify-content: center;">
        <RouterView></RouterView>
      </div>
      
    </div>
  </template>
  
  <script>
  import TopNav from '../components/Top/Top.vue'
  import PageTitle from '@/components/PageTitle.vue';
  import SideMenu from '@/components/MyPage/SideMenu.vue';
  
  export default {
    name: 'MyPage',
    components: {
      TopNav,
      PageTitle,
      SideMenu
    }
  }
  </script>
  
  <style>

  </style>
  