<template>
    <containerBox>
      <BoxTitle>
        ETF
      </BoxTitle>
      <ButtonContainer>
        <SmallButton text="시장 현황"/>
        <SmallButton text="순자산"/>
        <SmallButton text="거래량"/>
        <SmallButton text="수익률"/>
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