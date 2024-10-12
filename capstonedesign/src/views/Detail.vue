<template>
    <TopNav/>
  <PageTitle>전체 종목 보기</PageTitle>
    <SearchBar/>
    <div style="margin-left: 100px; min-width: 700px;">
      <ButtonContainer>
        <SmallButton text="국내"/>
        <SmallButton text="해외"/>
      </ButtonContainer>
      <ButtonContainer>
        <SmallButton text="전체"/>
        <SmallButton text="성장 기대주"/>
        <SmallButton text="안정 성장주"/>
        <SmallButton text="고수익 저평가"/>
        <SmallButton text="저평가 성장주"/>
      </ButtonContainer>
      <div style="display: flex; justify-content: space-between; ">
        <ButtonContainer>
          <select>
            <option value="1">조건 추가</option>
          </select>
          <SmallButton text="시가총액"/>
        </ButtonContainer>
      </div>
    </div>
    <StockTable></StockTable>
  </template>
  
  <script>
  import TopNav from '../components/Top/Top.vue'
  import SearchBar from '@/components/DetailPage/Search.vue';  
  import SmallButton from '@/components/SmallButton.vue';
  import ButtonContainer from '@/components/ButtonContainer.vue';
  import StockTable from '@/components/StockTable.vue'; 
  import PageTitle from '@/components/PageTitle.vue';
  export default {
    name: 'DetailPage',
    components: {
      TopNav,
      SearchBar,
      SmallButton,
      ButtonContainer,
      
      StockTable,
      PageTitle
    }
  }
  </script>
  
  <style>

  </style>
  