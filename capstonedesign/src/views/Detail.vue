<template>
    <TopNav/>
    <SearchBar/>
    <div class="ButtonContainer">
      <SmallButton>
        국내
      </SmallButton>
      <SmallButton>
        해외
      </SmallButton>
    </div>
    <div class="ButtonContainer">
      <SmallButton>
        전체
      </SmallButton>
      <SmallButton>
        성장 기대주
      </SmallButton>
      <SmallButton>
        안정 성장주
      </SmallButton>
      <SmallButton>
        고수익 저평가
      </SmallButton>
      <SmallButton>
        저평가 성장주
      </SmallButton>
    </div>
    <div class="ButtonContainer">
      <select>
        <option value="1">조건 추가</option>
      </select>
      <SmallButton>
        카테고리
      </SmallButton>
      <SmallButton>
        시가총액
      </SmallButton>
    </div>
  </template>
  
  <script>
  import TopNav from '../components/Top/Top.vue'
  import SearchBar from '@/components/DetailPage/Search.vue';  
  import SmallButton from '@/components/SmallButton.vue';
  export default {
    name: 'DetailPage',
    components: {
      TopNav,
      SearchBar,
      SmallButton
    }
  }
  </script>
  
  <style>
    .ButtonContainer{
      display: flex;
      gap: 5px;
      margin: 10px;
    }
  </style>
  