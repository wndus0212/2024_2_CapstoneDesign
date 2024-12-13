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
  import axios from 'axios';
  export default {
    name: 'MyPage',
    components: {
      TopNav,
      PageTitle,
      SideMenu,
      MainContainer
    },
    methods: {
      createTestData() {
        // Django 서버로 POST 요청을 보냄
        axios.post('https://web-capstonedesignfront-m3vkxnzga0885b97.sel4.cloudtype.app/create-test-data/')
          .then(response => {
            console.log(response.data.message);  // "Test data created successfully!" 출력
            alert('테스트 데이터가 생성되었습니다.');
          })
          .catch(error => {
            console.error("Error creating test data:", error);
            alert('데이터 생성 실패');
          });
      }
    }
  }
  </script>
  
  <style>

  </style>
  