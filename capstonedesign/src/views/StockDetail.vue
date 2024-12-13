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
                        <SelectBox 
                            :options="periodOptions" 
                            v-model="selectedPeriod" 
                            :width="'120px'" 
                        />
                        
                        <!-- 간격 선택 -->
                        <SelectBox 
                            :options="intervalOptions" 
                            v-model="selectedInterval" 
                            :width="'120px'" 
                        />

                        <!-- 지표 선택 -->
                        <SelectBox 
                            :options="indicatorOptions" 
                            v-model="selectedIndicator" 
                            :width="'120px'" 
                        />
                    </div>

                    <!-- 로딩 상태 및 히스토리 데이터 처리 -->
                    <div v-if="isLoading">차트 데이터를 로딩 중입니다...</div>
                    <div v-else-if="!history || history.length === 0">데이터가 없습니다.</div>
                    <div v-else>
                        <!-- 지표에 따라 다른 차트 컴포넌트 렌더링 -->
                        <component 
                        :is="getChartComponent" 
                        :history="selectedIndicator === 'volume' || selectedIndicator === 'price' ? history : undefined" 
                        :movingAveragedata="selectedIndicator === 'movingAverage' ? movingAveragedata : undefined" 
                        :bollingerBandData="selectedIndicator === 'bollingerBand' ? bollingerBandData : undefined"
                        />
                    </div>
                </div>

                <!-- 종목 정보 -->
                <Box width="600px">
                    <div v-if="info" class="info-card">
                        <div class="info-item">
                            <span class="info-title">섹터:</span>
                            <span>{{ info.sector || '정보 없음' }}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-title">산업:</span>
                            <span>{{ info.industry || '정보 없음' }}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-title">현재 주가:</span>
                            <span class="price">{{ info.currentPrice ? info.currentPrice.toLocaleString() : '정보 없음' }} {{ stockUnit }}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-title">구매량:</span>
                            <span>{{ info.volume ? info.volume.toLocaleString() : '정보 없음' }}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-title">시가총액:</span>
                            <span>{{ info.marketCap ? (info.marketCap/ 100000000).toLocaleString() : '정보 없음' }} 억{{ stockUnit }}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-title">전일 종가:</span>
                            <span>{{ info.previousClose ? info.previousClose.toLocaleString() : '정보 없음' }} {{ stockUnit }}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-title">Open:</span>
                            <span>{{ info.open ? info.open.toLocaleString() : '정보 없음' }} {{ stockUnit }}</span>
                        </div>
                    </div>
                </Box>

            </div>
        </MainContainer>

        <!-- 재무제표 요약 섹션 -->
        <MainContainer>
            <FinancialState :stockCode="this.stockCode" />
        </MainContainer>
    </PageContainer>
</template>

<script>
import axios from "axios";
import Top from "@/components/Top/Top.vue";
import PageTitle from "@/components/PageTitle.vue";
import MainContainer from "@/components/MainContainer.vue";
import PageContainer from "@/components/PageContainer.vue";
import FinancialState from "@/components/StockDetail/FinancialState.vue";
import Box from "@/components/Box.vue";
import SelectBox from "@/components/SelectBox.vue"; // SelectBox 컴포넌트 임포트

import VolumeChart from "@/components/StockDetail/Charts/VolumeChart.vue"; 
import PriceChart from "@/components/StockDetail/Charts/PriceChart.vue"; 
import MovingAverageChart from "@/components/StockDetail/Charts/MovingAverageChart.vue"; 
import BollingerBandChart from "@/components/StockDetail/Charts/BollingerBandChart.vue";

export default {
    components: {
        Top,
        PageTitle,
        MainContainer,
        PageContainer,
        FinancialState,
        Box,
        SelectBox, // SelectBox 컴포넌트 등록
        VolumeChart, // 거래량 차트 컴포넌트
        PriceChart, // 주가 차트 컴포넌트
        MovingAverageChart,
        BollingerBandChart
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
            stockUnit: "",
            stock: "",
            history: [],
            movingAveragedata: [],
            bollingerBandData:[],
            info: null, // 초기값을 null로 설정
            isLoading: false,
            selectedPeriod: "1mo", // 기본값
            selectedInterval: "1d", // 기본값
            selectedIndicator: "volume", // 기본 지표 설정

            // 옵션들 정의
            periodOptions: [
                { label: '1개월', value: '1mo' },
                { label: '6개월', value: '6mo' },
                { label: '1년', value: '1y' },
                { label: '5년', value: '5y' },
                { label: '전체', value: 'max' },
            ],
            intervalOptions: [
                { label: '일봉', value: '1d' },
                { label: '주봉', value: '1wk' },
                { label: '월봉', value: '1mo' },
            ],
            indicatorOptions: [
                { label: '거래량', value: 'volume' },
                { label: '주가', value: 'price' },
                { label: '이동평균선', value: 'movingAverage' },
                { label: '볼린저 밴드', value: 'bollingerBand' }
            ],
        };
    },
    watch: {
        // selectedPeriod 또는 selectedInterval이 변경되면 데이터를 다시 요청
        selectedPeriod() {
            this.fetchStockHistory();
            this.fetchMovingAverage();
            this.fetchBollingerBand();
        },
        selectedInterval() {
            this.fetchStockHistory();
            this.fetchMovingAverage();
            this.fetchBollingerBand();
        }
    },
    computed: {
        // 선택된 지표에 따라 차트 컴포넌트 반환
        getChartComponent() {
            if (this.selectedIndicator === "volume") {
                return "VolumeChart"; // 거래량 차트를 보여줌
            } else if (this.selectedIndicator === "price") {
                return "PriceChart"; // 주가 차트를 보여줌
            } else if (this.selectedIndicator === "movingAverage") {
                return "MovingAverageChart"; // 이동평균선 차트를 보여줌
            } else if (this.selectedIndicator === "bollingerBand") {
                return "BollingerBandChart"; // 이동평균선 차트를 보여줌
            }
            return null;
        }
    },
    async created() {
        this.stockName = this.$route.query.name || "알 수 없는 종목";
        // stockCode에 따라 단위 설정
        this.setStockUnit();
        await this.fetchStockHistory();
        await this.fetchStockInfo();
        await this.fetchMovingAverage();
    },
    methods: {
        // stockCode에 따른 단위 설정
        setStockUnit() {
            if (this.stockCode.endsWith(".KQ") || this.stockCode.endsWith(".KS")) {
                this.stockUnit = "원";
            } else {
                this.stockUnit = "달러";
            }
        },
        async fetchStockHistory() {
            this.isLoading = true; // 로딩 시작
            try {
                const response = await axios.get(
                    `https://web-capstonedesignfront-m3vkxnzga0885b97.sel4.cloudtype.app/stock/history/${this.stockCode}/`,
                    {
                        params: {
                            period: this.selectedPeriod,
                            interval: this.selectedInterval,
                        },
                    }
                );
                this.history = response.data?.output || []; // 데이터가 없으면 빈 배열로 처리
            } catch (error) {
                console.error("종목 히스토리를 가져오는 데 실패했습니다:", error);
                this.history = []; // 실패 시 빈 배열로 처리
            } finally {
                this.isLoading = false; // 로딩 종료
            }
        },
        async fetchMovingAverage() {
            this.isLoading = true; // 로딩 시작
            try {
                const response = await axios.get(
                    `https://web-capstonedesignfront-m3vkxnzga0885b97.sel4.cloudtype.app/stock/chart/moving_average/${this.stockCode}/`,
                    {
                        params: {
                            period: this.selectedPeriod,
                            interval: this.selectedInterval,
                        },
                    }
                );
                this.movingAveragedata = response.data?.output || []; // 데이터가 없으면 빈 배열로 처리
            } catch (error) {
                console.error("이동평균 데이터를 가져오는 데 실패했습니다:", error);
                this.movingAveragedata = []; // 실패 시 빈 배열로 처리
            } finally {
                this.isLoading = false; // 로딩 종료
            }
        },
        async fetchBollingerBand() {
            this.isLoading = true; // 로딩 시작
            try {
                const response = await axios.get(
                    `https://web-capstonedesignfront-m3vkxnzga0885b97.sel4.cloudtype.app/stock/chart/bollinger_band/${this.stockCode}/`,
                    {
                        params: {
                            period: this.selectedPeriod,
                            interval: this.selectedInterval,
                        },
                    }
                );
                this.bollingerBandData = response.data?.output || []; // 데이터가 없으면 빈 배열로 처리
            } catch (error) {
                console.error("볼린저 밴드 데이터를 가져오는 데 실패했습니다:", error);
                this.bollingerBandData = []; // 실패 시 빈 배열로 처리
            } finally {
                this.isLoading = false; // 로딩 종료
            }
        },
        async fetchStockInfo() {
            this.isLoading = true; // 로딩 시작
            try {
                const response = await axios.get(
                    `https://web-capstonedesignfront-m3vkxnzga0885b97.sel4.cloudtype.app/stock/detail_info/${this.stockCode}/`,
                );
                this.info = response.data || {}; // 응답 데이터가 없으면 빈 객체로 처리
            } catch (error) {
                console.error("종목 정보를 가져오는 데 실패했습니다:", error);
                this.info = {}; // 실패 시 빈 객체로 처리
            } finally {
                this.isLoading = false; // 로딩 종료
            }
        },
    },
};
</script>

<style scoped>
.info-card {
  background-color: #f9f9f9;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #ddd;
}

.info-title {
  font-weight: bold;
  color: #333;
}

.price {
  font-size: 1.2em;
  color: #2c7dff;
}

.info-item:last-child {
  border-bottom: none;
}
</style>
