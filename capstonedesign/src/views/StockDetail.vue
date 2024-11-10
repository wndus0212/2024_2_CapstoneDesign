<template>
    <Top/>
    <div style="height: 120px;"></div>
    <PageTitle>
        {{ stock.prdt_abrv_name }}
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
            <StockChart :history="history" />
            <StockChartBelow/>
        </div>

        <div style="margin:0px 20px;">
            <Box>
                <EconomyNews/>
            </Box>
            <ConsensusTable/>
        </div>
    </MainContainer>

    <!-- 재무제표 요약 섹션 -->
    <MainContainer>
        <div style="display: flex;flex-wrap: wrap; justify-content: center;">
            <Box>
                <div>
                    <SubTitle style="margin: 10px;">
                        재무제표 요약
                    </SubTitle>
                    <ButtonContainer>
                        <SmallButton text="손익계산서"/>
                        <SmallButton text="대차대조표"/>
                        <SmallButton text="현금흐름표"/>
                    </ButtonContainer>
                </div>
                <FinancialStatementChart/>
            </Box>
            
            <Box>
                <FinancialStatementTable/>
            </Box>
        </div>
    </MainContainer>
</template>

<script>
import axios from 'axios';
import Top from '@/components/Top/Top.vue';
import PageTitle from '@/components/PageTitle.vue';
import MainContainer from '@/components/MainContainer.vue';
import StockChart from '@/components/StockDetail/StockChart.vue';
import StockChartBelow from '@/components/StockDetail/StockChartBelow.vue';
import Box from '@/components/Box.vue';
import ConsensusTable from '@/components/StockDetail/ConsensusTable.vue';
import SubTitle from '@/components/SubTitle.vue';
import ButtonContainer from '@/components/ButtonContainer.vue';
import SmallButton from '@/components/SmallButton.vue';
import FinancialStatementChart from '@/components/StockDetail/FinancialStatementChart.vue';
import FinancialStatementTable from '@/components/StockDetail/FinancialStatementTable.vue';

export default {
    components:{
        Top,
        PageTitle,
        MainContainer,
        StockChart,
        Box,
        ConsensusTable,
        StockChartBelow,
        SubTitle,
        ButtonContainer,
        SmallButton,
        FinancialStatementChart,
        FinancialStatementTable
    },
    props: {
        stockCode: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            stock: '',
            history: '',
            selectedPeriod: '1mo', // 기본값
            selectedInterval: '1d' // 기본값
        };
    },
    mounted() {
        console.log("코드:",this.Code);
        this.fetchStockDetails();
        this.fetchStockHistory();
    },
    methods: {
        fetchStockDetails() {
            axios
                .get(`http://127.0.0.1:8000/stock/detail/${this.stockCode}/`)
                .then(response => {
                    this.stock = response.data['output'];
                    console.log(this.stock)
                })
                .catch(error => console.error("종목 정보를 가져오는 데 실패했습니다:", error,this.Code));
        },
        fetchStockHistory() {
            // 선택한 기간과 간격을 URL 파라미터로 전달
            axios
                .get(`http://127.0.0.1:8000/stock/history/${this.stockCode}/`, {
                    params: {
                        start: '',
                        end: '',
                        period: this.selectedPeriod,
                        interval: this.selectedInterval
                    }
                })
                .then(response => {
                    this.history = response.data['output'];
                })
                .catch(error => console.error("종목 히스토리를 가져오는 데 실패했습니다:", error));
        }
    }
}
</script>
