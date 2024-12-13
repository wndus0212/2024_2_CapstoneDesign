<template>
    <div style="display: flex; gap: 12px;">
        <div class="totalAmount">
            {{ portfolioSum}}
        </div>
        <div 
            class="priceChange" 
            :class="{ positive: change > 0, negative: change < 0 }">
            {{ change }}%
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    props: {
        portfolioId: {
            type: Number,
            required: true,
        },
    },
    data() {
        return {
            portfolioSum: null, // 현재 값
            initial: null, // 초기 값
            change: null, // 변화량
        };
    },
    mounted() {
        const token = localStorage.getItem("token");

        // 현재 포트폴리오 값 가져오기
        axios
            .get(`http://127.0.0.1:8000/portfolio/history/${this.portfolioId}/`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .then((response) => {
                const output=response.data.output
                this.initial = output[0]['portfolio_value'].toFixed(0); // JSON의 "value" 값 사용
                this.portfolioSum = output[output.length-1]['portfolio_value'].toFixed(0); // JSON의 "value" 값 사용
                this.calculateChange();
            })
            .catch((error) => {
                console.error(error);
            });
    },
    methods: {
        calculateChange() {
            // 값이 모두 존재하면 변화량 계산
            if (this.portfolioSum !== null && this.initial !== null) {
                this.change = ((this.portfolioSum - this.initial)/this.initial).toFixed(2);
            }
        },
    },
};
</script>

<style>
.totalAmount {
    font-size: 30px;
    margin-bottom: 20px;
}

.priceChange {
    font-size: 20px;
}

/* 긍정적 변화 (빨간색) */
.priceChange.positive {
    color: red;
}

/* 부정적 변화 (파란색) */
.priceChange.negative {
    color: blue;
}
</style>
