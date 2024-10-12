<template>
    <TopNav/>
    <PageTitle>마이페이지</PageTitle>
    <div style="display: flex;">
      <SideMenu/>
    </div>
  </template>
  
  <script>
  import TopNav from '../components/Top/Top.vue'
  import PageTitle from '@/components/PageTitle.vue';
  import SideMenu from '@/components/SideMenu.vue';
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
  