<template>
    <TopNav/>
    <div style="height: 120px;"></div>
    <PageTitle>전체 종목 보기</PageTitle>
    <div style="display: flex; justify-content: center;">
      <SearchBar/>
    </div>
    
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
      <ButtonContainer>
        <SelectBox :options="selectOption" v-model="selectedOption" width="200px"/>
        <SmallButton text="시가총액"/>
      </ButtonContainer>
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
  import SelectBox from '@/components/SelectBox.vue';

  export default {
    name: 'DetailPage',
    components: {
      TopNav,
      SearchBar,
      SmallButton,
      ButtonContainer,
      StockTable,
      PageTitle,
      SelectBox
    },
    data() {
        return {
            showModal: false,
            selectOption: [
              { label: '오름차순', value: '1' },
              { label: '내림차순', value: '2' }
            ],
            selectOption2: [
              { label: '국내', value: 'KOR' },
              { label: '미국', value: '' }
            ],
            selectedOption1: '', // 첫 번째 Select의 선택된 값
            selectedOption2: ''  // 두 번째 Select의 선택된 값
        };
    },
  }
  </script>
  
  <style>

  </style>
  