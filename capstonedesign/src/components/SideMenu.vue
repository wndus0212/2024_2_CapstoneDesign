<template>
    <div style="margin-left: 60px;">
        <SmallButton class="menuButton" text="내 포트폴리오">        
        </SmallButton>
        <SmallButton class="menuButton" text="포트폴리오 추가">
        </SmallButton>
        <SmallButton class="menuButton" text="관심 종목">
        </SmallButton>
    </div>
</template>
<script>
import SmallButton from './SmallButton.vue';    
export default {
    components:{
        SmallButton
    }
}
</script>
<style>
    .menuButton {
        width: 500px; 
        height: 60px; 
        margin-top: 20px; 
        font-size: 50px; 
    }
</style>