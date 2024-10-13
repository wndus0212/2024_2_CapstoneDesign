<template >
    <div class="newsWrapper">
        <InfoComponent/>
        <InfoComponent/>
        <InfoComponent/>
        <InfoComponent/>
        <InfoComponent/>
        <InfoComponent/>
    </div>
    <SmallButton text="더보기"/>
</template>
<script>
import InfoComponent from './InfoComponent.vue';
import SmallButton from '../SmallButton.vue';
export default {
    components:{
        InfoComponent,
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