<template>
  <div>
    <div>
      <Box :width="'1400'">
        <ButtonContainer>
          <SelectBox :options="selectOption1" v-model="selectedOption1" :width="'200px'"/>
          <SelectBox :options="selectOption2" v-model="selectedOption2" :width="'200px'"/>
          <SelectBox v-if="selectedOption2 !== 'ETF'" :options="filteredSelectOption3" v-model="selectedOption3" width="200px"/>
        </ButtonContainer>
        <ButtonContainer>
          <SelectBox :options="selectOption5" v-model="selectedOption5" :width="'200px'"/>
          <SelectBox :options="selectOption4" v-model="selectedOption4" :width="'200px'"/>
        </ButtonContainer>
        <StockAddTable 
          :selectedOption1="selectedOption1"
          :selectedOption2="selectedOption2"
          :selectedOption3="selectedOption3"
          :selectedOption4="selectedOption4"
          :selectedOption5="selectedOption5"
          :addedStock="addedStock"
          @addedstock="handleStockUpdate"
        />
      </Box>
    </div>
  </div>
</template>

<script>
import SelectBox from '@/components/SelectBox.vue';
import ButtonContainer from '@/components/ButtonContainer.vue';
import StockAddTable from './StockAddTable.vue';
import Box from '@/components/Box.vue';

export default {
  name: 'StockAddWidget',
  components: {
    ButtonContainer,
    StockAddTable,
    SelectBox,
    Box
  },
  
  props: {
    addedStock: {
      type: Array,
      required: true,
      default: () => [] // 기본값으로 빈 배열 설정
    }
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
        { label: '주가', value: 'prices' },
        { label: '거래량', value: 'volume' }
      ],
      selectOption5: [
        { label: '전체', value: '1' }
      ],
      selectedOption1: 'KOR',
      selectedOption2: 'Stock',
      selectedOption3: 'KRX', // 기본값 설정
      selectedOption4: 'market_caps',
      selectedOption5: '1'
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
  mounted(){
    console.log("stockaddwidget this.addedstock:",this.addedStock)
  },
  methods: {
    handleStockUpdate(addedstock) {
      // 부모로 이벤트 전달
      console.log("addwidget:",addedstock)
      this.$emit('addedstock', addedstock);
    }
  }
};
</script>

<style scoped>
.Container {
  min-width: 1280px;
  padding-top: 20px;
}
</style>
