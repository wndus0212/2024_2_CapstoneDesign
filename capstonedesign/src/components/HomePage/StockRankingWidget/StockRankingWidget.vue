<template>
    <containerBox>
      <BoxTitle>
        주식 순위
      </BoxTitle>
      <ButtonContainer>
        <SmallButton>
          많이 상승한 순위
        </SmallButton>
        <SmallButton>
          많이 하락한 순위
        </SmallButton>
        <SmallButton>
          거래량 많은 순위
        </SmallButton>
        <SmallButton>
          인기 많은 순위
        </SmallButton>
      </ButtonContainer>

    </containerBox>
</template>
<script>
import containerBox from '@/components/Box.vue'
import BoxTitle from '@/components/BoxTitle.vue';
import SmallButton from '@/components/SmallButton.vue';
import ButtonContainer from '@/components/ButtonContainer.vue';
export default {
    name:'StockRankingWidget',
    components:{
        containerBox,
        BoxTitle,
        SmallButton,
        ButtonContainer
    }
}
</script>
<style>
    
</style>