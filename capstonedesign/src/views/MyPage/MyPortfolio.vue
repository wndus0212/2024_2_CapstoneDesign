<template>
    <div class="innerPageWrapper">
        <Box width="1000px">
            <SelectBox :options="selectPortfolio" v-model="selectedPortfolio"/>
            <div style="display: flex; gap: 12px;">
                <div class="totalAmount">
                    10,000,000
                </div>
                <div class="priceChange">
                    (+0.05%)
                </div>
            </div>
            <SelectBox :options="selectCharacteristic" v-model="selectedCharacteristic" width="200px"/>
            <PortfolioChart/>
            <div style="display: flex; justify-content: space-between;">
                <SelectBox :options="selectCharacteristic" v-model="selectedCharacteristic" width="200px"/>
                <div>
                    모든 종목 보기
                    <input type="checkbox">
                </div>
            </div>
            
            <div style="display: flex;">
                <PortfolioPieChart :stocks="portfolioStocks"/>
            </div>
            <SmallButton text="수정" @click="openModal"/>
            <EditPortfolio v-if="showModal" @close="closeModal">
            </EditPortfolio>
            <box class="AIFeedBack"></box>
            <SubTitle>
                백테스트
            </SubTitle>
            <div style="display: flex; gap: 20px;">
                <div>
                    <div>시작 날짜</div>
                    <input type="date">
                </div>

                <div>
                    <div>종료 날짜</div>
                    <input type="date">
                </div>
            </div>
            <PortfolioBackTestChart/>
            
            <SubTitle>
                몬테카를로 분석
            </SubTitle>
            <PortfolioMontecarlo/>
        </Box>
    </div>
</template>

<script>
import axios from 'axios';
import PortfolioChart from '@/components/MyPage/PortfolioChart.vue';
import PortfolioPieChart from '@/components/MyPage/PortfolioPieChart.vue';
import SmallButton from '@/components/SmallButton.vue';
import Box from '@/components/Box.vue';
import PortfolioBackTestChart from '@/components/MyPage/PortfolioBackTestChart.vue';
import PortfolioMontecarlo from '@/components/MyPage/PortfolioMontecarlo.vue';
import SubTitle from '@/components/SubTitle.vue';
import EditPortfolio from '@/components/MyPage/EditPortfolio/EditPortfolio.vue';
import SelectBox from '@/components/SelectBox.vue';

export default {
    components: {
        PortfolioChart,
        PortfolioPieChart,
        SmallButton,
        Box,
        PortfolioBackTestChart,
        PortfolioMontecarlo,
        SubTitle,
        EditPortfolio,
        SelectBox,
    },
    data() {
        return {
            showModal: false,
            selectPortfolio: [],
            selectedPortfolio: '',

            selectCharacteristic: [
                { label: '지표', value: '1' }
            ],
            selectedCharacteristic: '',
            portfolioStocks: [],
        };
    },
    mounted() {
        const token = localStorage.getItem("token");
        // API 호출하여 포트폴리오 목록을 가져옴
        axios.get('http://127.0.0.1:8000/portfolio/portfolios/', {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        })
        .then(response => {
            this.selectPortfolio = response.data.map(portfolio => ({
                label: portfolio.name,
                value: portfolio.portfolio_id,
            }));
            console.log(response.data);
            // 포트폴리오 목록이 로드된 후, 첫 번째 포트폴리오의 ID로 포트폴리오 종목 불러오기
            if (this.selectPortfolio.length > 0) {
                this.selectedPortfolio = this.selectPortfolio[0].value;
                this.fetchPortfolioStocks(this.selectedPortfolio); // 처음 실행
            }
        })
        .catch(error => {
            console.error(error);
        });
    },
    methods: {
        openModal() {
            this.showModal = true;
        },
        closeModal() {
            this.showModal = false;
        },
        fetchPortfolioStocks(newPortfolioId) {
            if (!newPortfolioId) {
                this.portfolioStocks = [];
                return;
            }

            const token = localStorage.getItem("token");
            axios.get(`http://127.0.0.1:8000/portfolio/portfolios/stock_list/${newPortfolioId}/`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            })
            .then(response => {
                this.portfolioStocks = response.data; // 포트폴리오 종목 데이터 저장
            })
            .catch(error => {
                console.error(error);
            });
        },
    }
};
</script>

<style>
    .innerPageWrapper{
        text-align: left;
        min-width: 850px;
        padding: 30px;
        
    }

    .select{
        margin-bottom: 10px;
    }

    .investmentPropensity{
        font-size: 24px;
        margin-bottom: 10px;
    }

    .totalAmount{
        font-size: 30px;
        margin-bottom: 20px;
    }

    .priceChange{
        color: red;
    }

    .AIFeedBack{
        width: 95%;
    }
</style>