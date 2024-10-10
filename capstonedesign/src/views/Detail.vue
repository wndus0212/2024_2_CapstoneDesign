<template>
    <TopNav/>

    <SearchBar/>
    <div style="margin-left: 10px;">
      <ButtonContainer>
        <SmallButton>
          국내
        </SmallButton>
        <SmallButton>
          해외
        </SmallButton>
      </ButtonContainer>
      <ButtonContainer>
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
      </ButtonContainer>
      <div style="display: flex; justify-content: space-between; margin-right: 10px;">
        <ButtonContainer>
          <select>
            <option value="1">조건 추가</option>
          </select>
          <SmallButton>
            카테고리
          </SmallButton>
          <SmallButton>
            시가총액
          </SmallButton>
        </ButtonContainer>

        <ButtonContainer>
          <SmallButton>
            관련 핫토픽
          </SmallButton>
          <SmallButton>
            전문가 의견
          </SmallButton>
          <SmallButton>
            비슷한 종목
          </SmallButton>
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

  export default {
    name: 'DetailPage',
    components: {
      TopNav,
      SearchBar,
      SmallButton,
      ButtonContainer,
      
      StockTable
    }
  }
  </script>
  
  <style>

  </style>
  