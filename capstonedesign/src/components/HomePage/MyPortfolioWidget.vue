<template>
    <containerBox>
      <BoxTitle>
        내 포트폴리오
      </BoxTitle>
      <p>
        hello
      </p>
    </containerBox>
</template>
<script>
import containerBox from '@/components/Box.vue'
import BoxTitle from '@/components/BoxTitle.vue';
export default {
    name:'MyPortfolioWidget',
    components:{
        containerBox,
        BoxTitle
    }
}
</script>
<style>
    
</style>