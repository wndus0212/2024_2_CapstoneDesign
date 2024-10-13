<template>
    <div class="questionBlock">
        <div class="question">
            새 포트폴리오 이름
        </div>
        <input type="text" class="answer">
    </div>
    <div class="questionBlock">
        <div class="question">
            투자 시 고려하는 수익과 위험 밸런스
        </div>
        <input type="text" class="answer">
    </div>
    <div class="questionBlock">
        <div class="question">
            예상 투자 기간
        </div>
        <input type="text" class="answer">
    </div>
    <div class="questionBlock">
        <div class="question">
            감수 가능한 손실
        </div>
        <input type="text" class="answer">
    </div>
    <div class="questionBlock">
        <div class="question">
            기대 수익
        </div>
        <input type="text" class="answer">
    </div>

    <SmallButton text="저장"></SmallButton>
</template>
<script>
import SmallButton from '../SmallButton.vue';
export default {
    components:{
        SmallButton
    }
}
</script>
<style>
    .question{
        font-size: 22px;
        margin-bottom: 10px;
    }

    .answer{
        height: 30px;
        width: 200px
    }
    .questionBlock{
        margin-bottom: 20px
    }
</style>