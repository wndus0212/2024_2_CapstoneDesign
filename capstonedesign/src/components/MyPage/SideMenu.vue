<template>
    <div style="margin:0px 60px; width: 200px;">
        <SmallButton @click="navigateTo('/MyPage/MyPortfolio')" class="menuButton" text="내 포트폴리오">        
        </SmallButton>
        <SmallButton @click="navigateTo('/MyPage/AddPortfolio')" class="menuButton" text="포트폴리오 관리">
        </SmallButton>
    </div>
</template>
<script>
import SmallButton from '../SmallButton.vue';    
export default {
    components:{
        SmallButton
    },
    methods:{
        navigateTo(route) {
            this.$router.push(route); // Vue Router를 사용해 라우트 변경
        }
            
    }
}
</script>
<style>
    .menuButton {
        width: 200px; 
        height: 70px !important; 
        margin-top: 50px !important; 
        font-size: 50px; 
        font-weight: 600;
        margin-left: 50px;
        margin-right: 50px;
        min-width: 200px;
    }
</style>