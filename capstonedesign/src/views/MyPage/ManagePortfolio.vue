<template>
    <div class="innerPageWrapper">
        <SubTitle>
            내 포트폴리오 목록
        </SubTitle>
        <div style="margin-right: 120px; display: flex; justify-content: space-between; width:87%">
            <div style="display: flex; gap: 20px;">
                <SmallButton text="이름 순"/>
                <SmallButton text="투자 성향 순"/>
            </div>

            <p>
                전체 선택
                <input type="checkbox" >
            </p>
            
        </div>
        
        <PortfolioTable style="margin-left: auto;"/>
        <SmallButton text="삭제"/>
        
        <SubTitle>
            새 포트폴리오 생성
        </SubTitle>

        <CreatePortfolio/>
    </div>
</template>
<script>
import PortfolioTable from '@/components/MyPage/PortfolioTable.vue';
import SmallButton from '@/components/SmallButton.vue';
import SubTitle from '@/components/SubTitle.vue';
import CreatePortfolio from '@/components/MyPage/CreatePortfolio.vue';

export default {
    components:{
        PortfolioTable,
        SmallButton,
        SubTitle,
        CreatePortfolio
    }
}
</script>
<style>
    .innerPageWrapper{
        text-align: left;
        min-width: 850px;
        padding: 30px;
    }
</style>