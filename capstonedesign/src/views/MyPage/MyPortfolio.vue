<template>
    <div class="innerPageWrapper">
        <Box :width="'1000px'">
            <SelectBox :options="selectPortfolio" v-model="selectedPortfolio" />
            
            <PortfolioSum v-if="selectedPortfolio" :portfolio-id="Number(selectedPortfolio)"/>
            <!-- PortfolioChart는 selectedPortfolio가 설정될 때만 렌더링 -->
            <PortfolioChart v-if="selectedPortfolio" :portfolioId="Number(selectedPortfolio)" />

            <div style="display: flex; justify-content: space-between;">
                <SelectBox :options="selectCharacteristic" v-model="selectedCharacteristic" width="200px" />

            </div>
            
            <div style="display: flex;">
                <PortfolioPieChart :addedStock="portfolioStocks" />
            </div>
            <SmallButton text="수정" @click="openModal" />
            <EditPortfolio v-if="showModal" @close="closeModal" :portfolioId="Number(selectedPortfolio)" />

            <box class="AIFeedBack"></box>
            <SubTitle>
                백테스트
            </SubTitle>
            <div class="description-box">
                <p>몬테카를로 시뮬레이션을 통해 특정 투자 전략이나 포트폴리오가 시뮬레이션 기간 종료 시 보유하게 될 최종 자산 값을 의미합니다.</p>
                <p>해당 투자 전략의 잠재적인 수익 가능성을 알 수 있습니다.</p>
                
            </div>
            <PortfolioBackTestChart v-if="selectedPortfolio" :portfolioId="Number(selectedPortfolio)" />
            
            <SubTitle>
                몬테카를로 분석
            </SubTitle>
            <div class="description-box">
                <p>투자 기간 동안 포트폴리오의 가치가 가장 많이 하락한 비율을 의미합니다.</p>
                <p>포트폴리오의 최대 손실 위험을 측정하는 중요한 지표로, 투자 중 최악의 상황에서 자산이 얼마나 감소했는지를 나타냅니다.</p>
                
            </div>
            <PortfolioMontecarlo v-if="selectedPortfolio" :portfolioId="Number(selectedPortfolio)" />
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
import PortfolioSum from '@/components/MyPage/PortfolioSum.vue';
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
        PortfolioSum
    },
    data() {
        return {
            showModal: false,
            selectPortfolio: [],
            selectedPortfolio: null, // 초기값을 null로 설정
            selectCharacteristic: [
                { label: '지표', value: '1' }
            ],
            selectedCharacteristic: '',
            portfolioStocks: [],
            portfolioSum:null
        };
    },
    mounted() {
        const token = localStorage.getItem("token");
        axios.get('https://port-0-capstonedesign-m3vkxnzga0885b97.sel4.cloudtype.app/portfolio/portfolios/', {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        })
        .then(response => {
            this.selectPortfolio = response.data.map(portfolio => ({
                label: portfolio.name,
                value: portfolio.portfolio_id.toString(),
            }));
            
            // 첫 번째 포트폴리오 자동 선택
            if (this.selectPortfolio.length > 0) {
                this.selectedPortfolio = this.selectPortfolio[0].value.toString();
                this.fetchPortfolioStocks(this.selectedPortfolio);
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
            axios.get(`https://port-0-capstonedesign-m3vkxnzga0885b97.sel4.cloudtype.app/portfolio/portfolios/stock_list/${newPortfolioId}/`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            })
            .then(response => {
                this.portfolioStocks = response.data;
            })
            .catch(error => {
                console.error(error);
            });
        },
    },
    watch: {
        selectedPortfolio(newPortfolioId) {
            this.fetchPortfolioStocks(newPortfolioId);
        },
    },
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

    .AIFeedBack{
        width: 95%;
    }
</style>