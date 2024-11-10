<template>
  <div>
    <TopNav />
    <div style="height: 120px;"></div>
    <PageTitle>전체 종목 보기</PageTitle>
    <div style="display: flex; justify-content: center;">
      <SearchBar />
    </div>

    <div style="margin-left: 100px; min-width: 700px;">
      <ButtonContainer>
        <SelectBox :options="selectOption1" v-model="selectedOption1" width="200px"/>
        <SelectBox :options="selectOption2" v-model="selectedOption2" width="200px"/>
        <SelectBox :options="filteredSelectOption3" v-model="selectedOption3" width="200px"/>
      </ButtonContainer>
      <ButtonContainer>
        <SelectBox :options="selectOption4" v-model="selectedOption4" width="200px"/>
        <SmallButton text="시가총액"/>
      </ButtonContainer>
    </div>

    <StockTable></StockTable>
  </div>
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
          { label: '전체', value: 'GLB' },
          { label: 'NYSE', value: 'NYSE' },
          { label: 'NASDAQ', value: 'NASDAQ' }
        ]
      },
      selectOption4: [
        { label: '시가총액', value: '1' },
      ],
      selectedOption1: 'KOR',
      selectedOption2: 'Stock',
      selectedOption3: 'KRX', // 이 값은 첫 번째 값에 맞게 초기화
      selectedOption4: '1'
    };
  },
  computed: {
    // selectedOption1에 따라 selectOption3를 필터링
    filteredSelectOption3() {
      return this.selectOption3[this.selectedOption1] || [];
    }
  },
  watch: {
    // selectedOption1이 변경되면 selectedOption3도 초기화
    selectedOption1(newValue) {
      this.selectedOption3 = this.selectOption3[newValue][0].value;
    }
  }
}
</script>

<style scoped>
/* 스타일을 추가하실 수 있습니다 */
</style>
