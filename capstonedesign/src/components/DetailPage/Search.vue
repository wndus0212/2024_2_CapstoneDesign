<template>
  <div class="searchBar">
    <input
      type="text"
      v-model="searchInput"
      placeholder="검색어를 입력하세요..."
      class="search-bar"
      @input="filterSuggestions"
    />

    <!-- 연관 검색어 리스트 -->
    <ul v-if="suggestions.length" class="suggestion-list">
      <li
        v-for="(suggestion, index) in suggestions"
        :key="index"
        @click="selectSuggestion(suggestion)"
      >
        {{ suggestion }}
      </li>
    </ul>
    <div v-else-if="searchInput && !suggestions.length" class="no-results">
      검색 결과가 없습니다.
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
      console.log('입력된 값:', query);   // 입력된 값 출력
      console.log('query 데이터 타입:', typeof query);  // query의 데이터 타입 출력
      
      if (typeof query === 'string') {
        this.filteredSuggestions = this.filterSuggestions(query);
      } else {
        console.warn('입력값이 문자열이 아닙니다:', query);
      }
    },
    filterSuggestions(query) {
      if (!Array.isArray(this.searchData)) {
        console.warn('searchData는 배열이 아님:', this.searchData);
        return [];
      }
      console.log('입력된 값:', query);
      console.log('query 데이터 타입:', typeof query);
      const lowerCaseQuery = query.toLowerCase();
      return this.searchData.filter(item =>
        item.name.toLowerCase().includes(lowerCaseQuery)
      );
    },
  },
};
</script>
<style>
  .search-bar{
    background-color: white;
    height: 50px;
    width: 600px;
    border-radius: 10px;
    box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
  }
  
  .textInput{
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
    z-index: 10;
  }
  .suggestion-list li {
    padding: 10px;
    cursor: pointer;
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
</style>