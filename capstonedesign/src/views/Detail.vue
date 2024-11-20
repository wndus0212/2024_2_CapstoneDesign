<template>
  <div>
    <TopNav />
    <div style="height: 120px;"></div>
    <div style="display: flex; justify-content: center">
      <div class="Container">
      <PageTitle>전체 종목 보기</PageTitle>
      <div style="display: flex; justify-content: center;">
        <SearchBar 
        :searchData="searchData" />
      </div>

      <div style="margin-left: 100px; min-width: 700px;">
        <ButtonContainer>
          <SelectBox :options="selectOption1" v-model="selectedOption1" width="200px"/>
          <SelectBox :options="selectOption2" v-model="selectedOption2" width="200px"/>
          <SelectBox v-if="selectedOption2 !== 'ETF'" :options="filteredSelectOption3" v-model="selectedOption3" width="200px"/>
        </ButtonContainer>
        <ButtonContainer>
          <SelectBox :options="selectOption5" v-model="selectedOption5" width="200px"/>
          <SelectBox :options="selectOption4" v-model="selectedOption4" width="200px"/>
          <SmallButton text="시가총액"/>
        </ButtonContainer>
      </div>
      <div style="display: flex; justify-content: center;">
        <StockTable :selectedOption1="selectedOption1"
          :selectedOption2="selectedOption2"
          :selectedOption3="selectedOption3"
          :selectedOption4="selectedOption4"
          :selectedOption5="selectedOption5">
        </StockTable>
      </div>
    </div>
    
    </div>
    
    
  </div>
</template>

<script>
import axios from 'axios';
import TopNav from '../components/Top/Top.vue'
import SearchBar from '@/components/DetailPage/Search.vue';
import SmallButton from '@/components/SmallButton.vue';
import ButtonContainer from '@/components/ButtonContainer.vue';
import StockTable from '@/components/StockDetail/StockTable.vue';
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
    SelectBox,
  },
  data() {
    return {
      selectOption1: [
        { label: '국내', value: 'KOR' },
        { label: '해외', value: 'GLB' }
      ],
      selectOption2: [
        { label: '주식', value: 'Stock' },
        { label: 'ETF', value: 'ETF' }
      ],
      selectOption3: {
        KOR: [
          { label: '전체', value: 'KRX' },
          { label: 'KOSPI', value: 'KOSPI' },
          { label: 'KOSDAQ', value: 'KOSDAQ' },
          { label: 'KONEX', value: 'KONEX' }
        ],
        GLB: [
          { label: 'NYSE', value: 'NYSE' },
          { label: 'NASDAQ', value: 'NASDAQ' },
          { label: 'S&P500', value: 'SP500' }
        ]
      },
      selectOption4: [
        { label: '시가총액', value: 'market_caps' },
        { label: '주가', value: 'prices'},
        {label: '거래량', value: 'volume'}
      ],
      selectOption5: [
        { label: '전체', value: '1' },
      ],
      selectedOption1: 'KOR',
      selectedOption2: 'Stock',
      selectedOption3: 'KRX', // 이 값은 첫 번째 값에 맞게 초기화
      selectedOption4: 'market_caps',
      selectedOption5: '1',

      searchData: [],
    };
  },
  computed: {
    // selectedOption1에 따라 selectOption3를 필터링
    filteredSelectOption3() {
      console.log(this.selectOption3[this.selectedOption1])
      return this.selectOption3[this.selectedOption1] || [];
      
    }
  },
  watch: {
    // selectedOption1이 변경되면 selectedOption3도 초기화
    selectedOption1(newValue) {
      console.log(newValue)
      console.log(this.selectOption3[newValue][0].value, this.selectOption3[this.selectedOption1]);
      
      this.selectedOption3 = this.selectOption3[newValue][0].value;
    }
  },
  mounted() {
    this.fetchStockData(); // 페이지 로드 시 전체 데이터 로드
  },
  methods: {
    fetchStockData() {
      // API 호출
      axios.get("http://127.0.0.1:8000/stock/search_term/").then((response) => {
        this.searchData = response.data["output"]; // 전체 데이터를 SearchBar로 전달
        console.log(this.searchData)
      });
    },
  },
}
</script>

<style scoped>
.Container{
    min-width: 1000px;
    max-width: 1250px;
    padding-top: 20px;
}
</style>
