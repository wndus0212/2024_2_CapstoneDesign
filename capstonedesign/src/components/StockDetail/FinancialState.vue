<template>
    <div style="display: flex;flex-wrap: wrap; justify-content: center;">
      <Box width="1250px">
        <div>
          <SubTitle style="margin: 10px;">
            재무제표 요약
          </SubTitle>
        </div>
        <IncomeStatement :data="income_stmt"/>
        <IncomeStatement :data="balance_sheet"/>
        <IncomeStatement :data="cashflow"/>
      </Box>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import Box from '../Box.vue';
  import IncomeStatement from './IncomeStatement.vue';
  import SubTitle from '../SubTitle.vue';
  
  export default {
    components: {
      Box,
      IncomeStatement,
      SubTitle, 
    },
    props: {
        stockCode: {
            type: String,
            required: true,
        },
    },
    data() {
      return {
        income_stmt: [], // 손익 계산서 데이터
        balance_sheet: [], // 대차대조표 데이터
        cashflow: [], // 현금 흐름표 데이터
        incomeStmtVisible: false, // 손익 계산서 토글 상태
        balanceSheetVisible: false, // 대차대조표 토글 상태
        cashflowVisible: false // 현금 흐름표 토글 상태
      };
    },
    methods: {
      async fetchFinancialState() {
        try {
            this.isLoading = true; // 로딩 시작
            axios
                .get(`http://127.0.0.1:8000/stock/financial_state/income_stmt/${this.stockCode}/`)
                .then(response => {
                    this.income_stmt = response.data["output"] || [];
                    console.log("재무제표", this.income_stmt)
                })    
                .catch(error => console.error("종목 히스토리를 가져오는 데 실패했습니다:", error));
            
            axios
                .get(`http://127.0.0.1:8000/stock/financial_state/balance_sheet/${this.stockCode}/`)
                .then(response => {
                    this.income_stmt = response.data["output"] || [];
                    console.log("재무제표", this.income_stmt)
                })    
                .catch(error => console.error("종목 히스토리를 가져오는 데 실패했습니다:", error));
            
            axios
                .get(`http://127.0.0.1:8000/stock/financial_state/cashflow/${this.stockCode}/`)
                .then(response => {
                    this.income_stmt = response.data["output"] || [];
                    console.log("재무제표", this.income_stmt)
                })    
                .catch(error => console.error("종목 히스토리를 가져오는 데 실패했습니다:", error));
        } catch (error) {
          console.error("종목 히스토리를 가져오는 데 실패했습니다:", error);
          this.income_stmt = [];
        }
      },
  
      // 손익 계산서 토글
      toggleIncomeStatement() {
        this.incomeStmtVisible = !this.incomeStmtVisible;
      },
  
      // 대차대조표 토글
      toggleBalanceSheet() {
        this.balanceSheetVisible = !this.balanceSheetVisible;
      },
  
      // 현금 흐름표 토글
      toggleCashflow() {
        this.cashflowVisible = !this.cashflowVisible;
      }
    },
    async mounted() {
        await this.fetchFinancialState();
    },
  }
  </script>
  
  <style scoped>
  /* 스타일 추가 필요시 작성 */
  </style>
  