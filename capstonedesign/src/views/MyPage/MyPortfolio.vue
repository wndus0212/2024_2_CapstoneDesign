<template>
    <div class="innerPageWrapper">
        <select class="select">
            <option>포트폴리오 1</option>
        </select>
        <div class="investmentPropensity">
            위험 중립형
        </div>
        <div style="display: flex; gap: 12px;">
            <div class="totalAmount">
                10,000,000
            </div>
            <div class="priceChange">
                (+0.05%)
            </div>
        </div>
        <select class="select">
            <option>
                지표 선택
            </option>
        </select>
        <PortfolioChart/>
        <div style="display: flex; justify-content: space-between;">
            <select class="select">
                <option>
                    기간
                </option>
            </select>
            <div>
                모든 종목 보기
                <input type="checkbox">
            </div>
        </div>
        
        <div style="display: flex;">
            <PortfolioPieChart/>
        </div>
        <SmallButton text="수정"/>
        <box class="AIFeedBack"></box>

        <div>
            백테스트
        </div>
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
        
        <PortfolioMontecarlo/>
        
    </div>
    
</template>
<script>
import PortfolioChart from '@/components/MyPage/PortfolioChart.vue';
import PortfolioPieChart from '@/components/MyPage/PortfolioPieChart.vue';
import SmallButton from '@/components/SmallButton.vue';
import Box from '@/components/Box.vue';
import PortfolioBackTestChart from '@/components/MyPage/PortfolioBackTestChart.vue';
import PortfolioMontecarlo from '@/components/MyPage/PortfolioMontecarlo.vue';

export default {
    components:{
        PortfolioChart,
        PortfolioPieChart,
        SmallButton,
        Box,
        PortfolioBackTestChart,
        PortfolioMontecarlo
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