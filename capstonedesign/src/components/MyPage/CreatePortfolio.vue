<template>
    <div>
        <div class="questionBlock" v-for="(question, index) in questions" :key="index">
            <div class="question">
                {{ question }}
            </div>
            <input type="text" class="answer" />
        </div>

        <SmallButton text="생성하기" @click="openModal" />
        
        <GPTCreatedPortfolio v-if="isModalOpen" @close="closeModal" />
    </div>
</template>

<script>
import SmallButton from '../SmallButton.vue';
import GPTCreatedPortfolio from './GPTCreatedPortfolio.vue';

export default {
    components: {
        SmallButton,
        GPTCreatedPortfolio
    },
    data() {
        return {
            questions: [
                "새 포트폴리오 이름",
                "투자 시 고려하는 수익과 위험 밸런스",
                "예상 투자 기간",
                "감수 가능한 손실",
                "기대 수익"
            ],
            isModalOpen: false // 모달 상태 관리
        };
    },
    methods: {
        openModal() {
            this.isModalOpen = true; // 모달 열기
        },
        closeModal() {
            this.isModalOpen = false; // 모달 닫기
        }
    }
};
</script>

<style scoped>
.question {
    font-size: 18px;
    margin-bottom: 10px;
    color: #333;
    font-weight: 600;
}

.answer {
    width: 100%;
    max-width: 300px;
    padding: 10px;
    font-size: 16px;
    border: none;
    border-radius: 8px;
    background-color: rgb(240, 240, 250);
    transition: border-color 0.3s, box-shadow 0.3s;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.answer:focus {
    border-color: #37a0f4;
    box-shadow: 0 0 8px rgba(55, 160, 244, 0.4);
    background-color: #fff;
    outline: none;
}

.answer:hover {
    border-color: #bbb;
}

.questionBlock {
    margin-bottom: 20px;
}
</style>
