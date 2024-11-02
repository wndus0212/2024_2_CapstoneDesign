<template>
    <Top/>
    <div style="height: 120px;"></div>
    <PageTitle>
        삼성전자
    </PageTitle>
    <MainContainer>
        <div>
            <div style="display: flex;">
                <select>
                    <option>1일</option>
                </select>
                <select>
                    <option>지표 보기</option>
                </select>
            </div>
            <StockChart/>
            <StockChartBelow/>
        </div>

        <div style="margin:0px 20px ;">
            <Box>
                <EconomyNews/>
            </Box>
            <ConsensusTable/>
        </div>
        
    </MainContainer>
    <MainContainer>
        <div style="display: flex;flex-wrap: wrap; justify-content: center;">
            <div>

                <Box>
                    <div >
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
            </div>
            
            <Box>
                <FinancialStatementTable/>
            </Box>
        </div>
    
        
        
    </MainContainer>
    
</template>
<script>
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
    }
    
}
</script>
<style>
    
</style>