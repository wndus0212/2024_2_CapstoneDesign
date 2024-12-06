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
                <PortfolioPieChart/>
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
    components:{
        PortfolioChart,
        PortfolioPieChart,
        SmallButton,
        Box,
        PortfolioBackTestChart,
        PortfolioMontecarlo,
        SubTitle,
        EditPortfolio,
        SelectBox
    },
    data() {
        return {
            showModal: false,
            selectPortfolio:[
                {label: '포트폴리오 1', value: '1'}
            ],
            selectedPortfolio: '',

            selectCharacteristic:[
                {label: '지표', value: '1'}
            ],
            selectedCharacteristic: ''
        };
    },
    methods:{
        openModal() {
            this.showModal = true;
        },
        closeModal() {
            this.showModal = false;
        }
    }
}
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