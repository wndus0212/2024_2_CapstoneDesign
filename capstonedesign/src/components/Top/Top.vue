<template>
    
    <nav class="TopNav">
      <ProjectLogo/>
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
            <TopNavButton @click="goToContents">
                <p>경제콘텐츠</p>
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
  import ProjectLogo from './logo.vue';

  export default {
    name: 'TopNav',
    components: {
        TopNavButton,
        ProjectLogo
    },
    methods:{
      goToHome() {
        this.$router.push('/');
      },
      goToDetail() {
        this.$router.push('/Detail');
      },
      goToContents() {
        this.$router.push('/Contents');
      },
      goToMyPage() {
        this.$router.push('/Mypage');
      },
    }
  };
  </script>
  
  <style scoped>
  .TopNav {
    background-color: lightblue;
    padding: 0px 20px;
    margin: 0px;
    display: flex;
    gap:  20px;
  }
  .TopNav ul {
    list-style: none;
    display: flex;
    gap: 1em;
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
  