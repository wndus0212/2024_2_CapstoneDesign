<template>
    <Top />
    <div style="height: 120px;"></div>
        <PageContainer>
            <PageTitle>
            {{ stockName || "로딩 중..." }}
        </PageTitle>
        <MainContainer>
            <div style="display: flex; flex-wrap: wrap; gap: 10px;">
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
                        <StockChart :history="history" />
                    </div>
                    
                </div>
                <Box width="600px">
                    <div>
                        <div>
                            {{ info.sector }}
                        </div>
                        <div>
                            {{ info.industry }}
                        </div>
                        <div>
                            현재 주가: {{ info.currentPrice }}
                        </div>
                        <div>
                            구매량: {{ info.volume }}
                        </div>
                        <div>
                            시가총액: {{ info.marketCap }}
                        </div>
                        <div>
                            전일 종가: {{ info.previousClose }}
                        </div>
                        <div>
                            open: {{ info.open }}
                        </div>
                    </div>
                </Box>
            </div>
            
        </MainContainer>

        <!-- 재무제표 요약 섹션 -->
        <MainContainer>
            <FinancialState :stockCode="this.stockCode"/>
        </MainContainer>
    </PageContainer>
    
</template>
<script>
import axios from "axios";
import Top from "@/components/Top/Top.vue";
import PageTitle from "@/components/PageTitle.vue";
import MainContainer from "@/components/MainContainer.vue";
import StockChart from "@/components/StockDetail/StockChart.vue";
import PageContainer from "@/components/PageContainer.vue";
import FinancialState from "@/components/StockDetail/FinancialState.vue";
import Box from "@/components/Box.vue";

export default {
    components: {
        Top,
        PageTitle,
        MainContainer,
        StockChart,
        PageContainer,
        FinancialState,
        Box
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
            info:"",
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
        await this.fetchStockInfo();
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
        async fetchStockInfo() {
            this.isLoading = true; // 로딩 시작
            try {
                const response = await axios.get(
                    `http://127.0.0.1:8000/stock/detail_info/${this.stockCode}/`,
                );
                this.info = response.data|| [];
            } catch (error) {
                console.error("종목 정보를 가져오는 데 실패했습니다:", error);
                this.info = [];
            } finally {
                this.isLoading = false; // 로딩 종료
            }
        },
        
    },
};
</script>

<style>

</style>