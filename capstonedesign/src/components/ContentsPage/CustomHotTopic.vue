<template >
    <div class="newsWrapper">
        <NewsComponent/>
        <NewsComponent/>
        <NewsComponent/>
        <NewsComponent/>
        <NewsComponent/>
        <NewsComponent/>
    </div>
    <SmallButton text="더보기"/>
</template>
<script>
import NewsComponent from './NewsComponent.vue';
import SmallButton from '../SmallButton.vue';
export default {
    components:{
        NewsComponent,
        SmallButton
    }
}
</script>
<style>
    .newsWrapper{
        height: 400px;
        overflow-y:auto ;
    }
</style>