<template>
    
    <nav class="TopNav">
      <ul>
        <li>
            <TopNavButton @click="goToHome">
                <p>홈</p>
            </TopNavButton>
        </li>
        <li>
            <TopNavButton @click="goToDetail">
                <p>종목별</p>
            </TopNavButton>
        </li>
        <li>
            <TopNavButton @click="goToMyPage">
                <p>마이페이지</p>
            </TopNavButton>
        </li>
      </ul>
    </nav>
  </template>
  
  <script>
  import TopNavButton from './TopNavButton.vue'

  export default {
    name: 'TopNav',
    components: {
        TopNavButton,
    },
    methods:{
      goToHome() {
        this.$router.push('/');
      },
      goToDetail() {
        this.$router.push('/Detail');
      },
      goToMyPage() {
        this.$router.push('/Mypage');
      },
    }
  };
  </script>
  
  <style scoped>
  .TopNav {
    padding: 0px 20px;
    margin: 0px;
    display: flex;
    gap:  20px;
    height: 100px;
    position: fixed; 
    top: 0; 
    width: 100%; 
    z-index: 1000; 
    border-bottom: 1px solid lightgray;
    background-color: white;
    box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
  }
  .TopNav ul {
    list-style: none;
    display: flex;
    gap: 40px;
    margin: 0;
    padding: 0;
  }
  .TopNav ul li {
    display: inline;
  }
  .TopNav ul li a {
    color: white;
    text-decoration: none;
  }
  .TopNav ul li a:hover {
    text-decoration: underline;
  }
  </style>
  