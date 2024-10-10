<template>
    <containerBox>
      <BoxTitle>
        ETF
      </BoxTitle>
      <ButtonContainer>
        <SmallButton>
          시장 현황
        </SmallButton>
        <SmallButton>
          순자산
        </SmallButton>
        <SmallButton>
          거래량
        </SmallButton>
        <SmallButton>
          수익률
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
    name:'ETFWidget',
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