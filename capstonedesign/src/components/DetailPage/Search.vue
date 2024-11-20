<template>
  <div class="searchBar">
    <input
      type="text"
      v-model="searchInput"
      placeholder="검색어를 입력하세요..."
      class="search-bar"
      @input="onInput"  
      @keyup.enter="onEnter"
    />

    <ul v-if="suggestions.length" class="suggestion-list">
      <li
        v-for="(suggestion, index) in suggestions"
        :key="index"
        @click="selectSuggestion(suggestion)"
      >
        <span>{{ suggestion.names }}</span>
        <span class="symbol">{{ suggestion.symbols }}</span>
      </li>
    </ul>
    <div v-else-if="searchInput && !suggestions.length" class="no-results">
      검색 결과가 없습니다. 현재 시장별 시가총액 상위 50위 이상 종목만 검색할 수 있습니다.
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchBar",
  props: {
    searchData: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      searchInput: "", // 검색창에 입력한 값
      suggestions: [], // 연관 검색어 리스트
    };
  },
  methods: {
    onInput(event) {
      const query = event.target.value;  // event.target.value로 문자열 값만 가져옴
      console.log('입력된 값:', event.target.value);   // 입력된 값 출력
      console.log('추천 검색어:', this.suggestions);
      if (typeof query === 'string') {
        this.suggestions = this.filterSuggestions(query); // suggestions 업데이트
      } else {
        console.warn('입력값이 문자열이 아닙니다:', query);
      }
    },
    filterSuggestions(query) {
      if (!Array.isArray(this.searchData)) {
        console.warn('searchData는 배열이 아님:', this.searchData);
        return [];
      }
      
      const lowerCaseQuery = query.toLowerCase();
      return this.searchData.filter(item => {
        // item.name과 item.symbol 두 속성에 대해 필터링
        const nameMatches = item.names && item.names.toLowerCase().includes(lowerCaseQuery);
        const symbolMatches = item.symbols && item.symbols.toLowerCase().includes(lowerCaseQuery);

        // 둘 중 하나라도 일치하면 결과로 반환
        return nameMatches || symbolMatches;
      }).slice(0, 5);
    },
    selectSuggestion(suggestion) {
      this.searchInput = suggestion['names']; // 선택된 추천 검색어로 검색창 값 설정
      this.suggestions = [];  // 검색어 선택 후 추천 리스트 초기화
    },
    onEnter() {
      const lowerCaseInput = this.searchInput.toLowerCase();

  // 입력값이 심볼인지 이름인지 판별하고 대응되는 값 가져오기
      const matchedItem = this.searchData.find(item => {
        const isSymbolMatch = item.symbols.toLowerCase() === lowerCaseInput;
        const isNameMatch = item.names.toLowerCase() === lowerCaseInput;
        console.log("item:",item)
        return isSymbolMatch || isNameMatch;
      });

      if (matchedItem) {
        // 입력값이 심볼이면 이름을 가져오고, 이름이면 심볼을 가져옴
        const stockCode = matchedItem.symbols;
        const stockName = matchedItem.names;
        
        // navigateTo 호출
        this.navigateTo(stockCode, stockName);
      } else {
        console.warn("검색어와 일치하는 항목이 없습니다.");
      }
    },
    navigateTo(stockCode, stockName) {
      this.$router.push({
        path: `/detail/${stockCode}`,
        query: {
          name: stockName,
        },
      });
      console.log("Stock Name:", stockName);
    },
  },
};
</script>

<style>
  .searchBar {
    background-color: white;
    height: 50px;
    width: 600px;
    border-radius: 10px;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
    position: relative;
  }

  .search-bar{
    height: 50px;
    width: 600px;
    font-size: 20px;
    border-radius: 10px;
  }

  .textInput {
    border: none;
    outline: none;
    width: 90%;
    height: 90%;
    font-size: 20px;
  }

  .suggestion-list {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    border: 1px solid #ccc;
    border-radius: 5px;
    background: white;
    list-style: none;
    margin: 0;
    padding: 0;
    z-index: 15;
    font-size: 20px;
    border-radius: 10px;
  }
  
  .suggestion-list li {
    padding: 10px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    margin: 0 20px
  }
  
  .suggestion-list li:hover {
    background-color: #f0f0f0;
  }

  .no-results {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    padding: 10px;
    text-align: center;
    color: #999;
    background: white;
    border: 1px solid #ccc;
    border-radius: 5px;
    z-index: 10;
  }


.symbol {
  font-size: 14px; /* 심볼 글자 크기 */
  color: #999; /* 서브 텍스트 색상 */
}

/* 애니메이션 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
