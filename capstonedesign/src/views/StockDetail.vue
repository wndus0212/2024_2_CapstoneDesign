<template>
    <Top />
    <div style="height: 120px;"></div>
    <PageTitle>
        {{ stockName || "로딩 중..." }}
    </PageTitle>
    <MainContainer>
        <div>
            <div style="display: flex;">
                <!-- 기간 선택 -->
                <select v-model="selectedPeriod" @change="fetchStockHistory">
                    <option value="1mo">1개월</option>
                    <option value="6mo">6개월</option>
                    <option value="1y">1년</option>
                    <option value="5y">5년</option>
                    <option value="max">전체</option>
                </select>
                
                <!-- 간격 선택 -->
                <select v-model="selectedInterval" @change="fetchStockHistory">
                    <option value="1d">일봉</option>
                    <option value="1wk">주봉</option>
                    <option value="1mo">월봉</option>
                </select>
                
                <select>
                    <option>지표 보기</option>
                </select>
            </div>

            <!-- 로딩 상태 및 히스토리 데이터 처리 -->
            <div v-if="isLoading">차트 데이터를 로딩 중입니다...</div>
            <div v-else-if="!history || history.length === 0">데이터가 없습니다.</div>
            <div v-else>
                <StockChart :history="history" />
            </div>

            <StockChartBelow />
        </div>

        <div style="margin:0px 20px;">
            <Box>
                <EconomyNews />
            </Box>
            <ConsensusTable />
        </div>
    </MainContainer>

    <!-- 재무제표 요약 섹션 -->
    <MainContainer>
        <div style="display: flex;flex-wrap: wrap; justify-content: center;">
            <Box width="1500px">
                <div>
                    <SubTitle style="margin: 10px;">
                        재무제표 요약
                    </SubTitle>
                </div>
                <div>
                    손익 계산서
                </div>
                <div style="display: flex; justify-content: space-evenly;">
                    <IncomeStatement :data="income_stmt"/>
                </div>
                <div>
                    대차대조표
                </div>
                <div style="display: flex; justify-content: space-evenly;">
                    <BalanceSheet :data="balance_sheet"/>
                </div>
                <div>
                    현금 흐름표
                </div>
                <div style="display: flex; justify-content: space-evenly;">
                    <CashFlow :data="cashflow"/>
                </div>
            </Box>
        </div>
    </MainContainer>
</template>
<script>
import axios from "axios";
import Top from "@/components/Top/Top.vue";
import PageTitle from "@/components/PageTitle.vue";
import MainContainer from "@/components/MainContainer.vue";
import StockChart from "@/components/StockDetail/StockChart.vue";
import StockChartBelow from "@/components/StockDetail/StockChartBelow.vue";
import Box from "@/components/Box.vue";
import ConsensusTable from "@/components/StockDetail/ConsensusTable.vue";
import SubTitle from "@/components/SubTitle.vue";
import IncomeStatement from "@/components/StockDetail/IncomeStatement.vue";
import BalanceSheet from "@/components/StockDetail/BalanceSheet.vue";
import CashFlow from "@/components/StockDetail/CashFlow.vue";

export default {
    components: {
        Top,
        PageTitle,
        MainContainer,
        StockChart,
        Box,
        ConsensusTable,
        StockChartBelow,
        SubTitle,
        IncomeStatement,
        BalanceSheet,
        CashFlow
    },
    props: {
        stockCode: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            stockName: "",
            stock: "",
            history: "",
            income_stmt:"",
            balance_sheet:"",
            cashflow:"",
            isLoading: false, // 로딩 상태
            selectedPeriod: "1mo", // 기본값
            selectedInterval: "1d", // 기본값
        };
    },
    async mounted() {
        this.stockName = this.$route.query.name || "알 수 없는 종목";
        await this.fetchStockHistory();
    },
    methods: {
        async fetchStockHistory() {
            this.isLoading = true; // 로딩 시작
            try {
                const response = await axios.get(
                    `http://127.0.0.1:8000/stock/history/${this.stockCode}/`,
                    {
                        params: {
                            start: "",
                            end: "",
                            period: this.selectedPeriod,
                            interval: this.selectedInterval,
                        },
                    }
                );
                this.history = response.data["output"] || [];
            } catch (error) {
                console.error("종목 히스토리를 가져오는 데 실패했습니다:", error);
                this.history = [];
            } finally {
                this.isLoading = false; // 로딩 종료
            }
        },
        async fetchFinancialState(){
            try {
                axios
                    .get(`http://127.0.0.1:8000/stock/financial_statement/1/${this.stockCode}`)
                    .then(response => {
                    this.income_stmt = response.data['output'];
                    })
                    .catch(error => console.error("종목 히스토리를 가져오는 데 실패했습니다:", error));
                
                axios
                    .get(`http://127.0.0.1:8000/stock/financial_statement/2/${this.stockCode}`)
                    .then(response => {
                    this.balance_sheet = response.data['output'];
                    })
                    .catch(error => console.error("종목 히스토리를 가져오는 데 실패했습니다:", error));
                
                axios
                    .get(`http://127.0.0.1:8000/stock/financial_statement/3/${this.stockCode}`)
                    .then(response => {
                    this.cashflow = response.data['output'];
                    })
                    .catch(error => console.error("종목 히스토리를 가져오는 데 실패했습니다:", error));
            } catch (error) {
                console.error("종목 히스토리를 가져오는 데 실패했습니다:", error);
                this.income_stmt = [];
            }
        }
    },
};
</script>

