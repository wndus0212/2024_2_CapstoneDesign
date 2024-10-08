<template>
    <nav class="TopNav">
      <ul>
        <li>
            <TopNavButton>
                <p>홈</p>
            </TopNavButton>
        </li>
        <li>
            <TopNavButton>
                <p>종목별</p>
            </TopNavButton>
        </li>
        <li>
            <TopNavButton>
                <p>경제콘텐츠</p>
            </TopNavButton>
        </li>
        <li>
            <TopNavButton>
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
    }
  };
  </script>
  
  <style scoped>
  .TopNav {
    background-color: lightblue;
    padding: 0px 20px;
    margin: 0px;
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
  