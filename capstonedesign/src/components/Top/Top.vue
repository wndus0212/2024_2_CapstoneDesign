<template>
    <nav class="TopNav">
      <ul>
        <li>
            <TopNavButton @click="goToHome">
                <p>홈</p>
            </TopNavButton>
        </li>
        <li>
            <TopNavButton @click="goToMyPage">
                <p>마이페이지</p>
            </TopNavButton>
        </li>
        <li  style="display: flex; flex-direction: column; justify-content: center;">
          <Search :searchData="searchData"/>
        </li>
      </ul>
    </nav>

    <SmallButton text="로그인"/>
  </template>
  
  <script>
  import axios from 'axios';
  import TopNavButton from './TopNavButton.vue'
  import Search from './Search.vue';
  import SmallButton from '../SmallButton.vue';

  export default {
    name: 'TopNav',
    components: {
        TopNavButton,
        Search,
        SmallButton
    }, 
    data(){
      return{
        searchData: [],
      }
    },
    mounted() {
      this.fetchStockData(); // 페이지 로드 시 전체 데이터 로드
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
      goToLogin() {
        this.$router.push('/login');
      },
      fetchStockData() {
        // API 호출
        axios.get("http://127.0.0.1:8000/stock/search_term/").then((response) => {
          this.searchData = response.data["output"]; // 전체 데이터를 SearchBar로 전달
          console.log(this.searchData)
        });
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
    justify-content: center;
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
  