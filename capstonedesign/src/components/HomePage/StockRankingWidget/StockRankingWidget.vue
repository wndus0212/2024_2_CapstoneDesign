<template>
    <containerBox>
      <BoxTitle>
        주식 순위
      </BoxTitle>
      <ButtonContainer>
        <SmallButton text="많이 상승한 순위"/>
        <SmallButton text="많이 하락한 순위"/>
        <SmallButton text="거래량 많은 순위"/>
        <SmallButton text="인기 많은 순위"/>
      </ButtonContainer>
      <StockRankingTable width="1000px" height="500px"/>
    </containerBox>
</template>
<script>
import containerBox from '@/components/Box.vue'
import BoxTitle from '@/components/BoxTitle.vue';
import SmallButton from '@/components/SmallButton.vue';
import ButtonContainer from '@/components/ButtonContainer.vue';
import StockRankingTable from './StockRankingTable.vue';

export default {
    name:'StockRankingWidget',
    components:{
        containerBox,
        BoxTitle,
        SmallButton,
        ButtonContainer,
        StockRankingTable
    }
}
</script>
<style>
    
</style>