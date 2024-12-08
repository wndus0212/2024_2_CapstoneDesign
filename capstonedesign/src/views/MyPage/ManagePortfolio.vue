<template>
    <div class="innerPageWrapper">
        <Box width="1000px">
        

            <SubTitle>
                새 포트폴리오 생성
            </SubTitle>

            <CreatePortfolio/>
        </Box>
        
    </div>
</template>
<script>
import SubTitle from '@/components/SubTitle.vue';
import CreatePortfolio from '@/components/MyPage/CreatePortfolio.vue';
import Box from '@/components/Box.vue';

export default {
    components:{
        SubTitle,
        CreatePortfolio,
        Box
    },
    data(){
        return{
            Portfolios:[]
        }
    },
    mounted() {
        
    },
}
</script>
<style>
    .innerPageWrapper{
        text-align: left;
        min-width: 850px;
        padding: 30px;
    }
</style>