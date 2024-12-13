<template>
  <nav class="TopNav">
    <ul>
      <li>
        <TopNavButton @click="goToHome">
          <p>홈</p>
        </TopNavButton>
      </li>
      <li style="display: flex; flex-direction: column; justify-content: center;">
        <Search :searchData="searchData" />
      </li>
      <li>
        <TopNavButton @click="goToMyPage">
          <p>마이페이지</p>
        </TopNavButton>
      </li>
    </ul>
  </nav>
  
  <!-- 로그인/로그아웃 버튼 -->
  <div class="auth-button" @click="toggleLoginStatus">
    <button class="login-logout-button">{{ isLoggedIn ? "로그아웃" : "로그인" }}</button>
  </div>
</template>

<script>
import axios from "axios";
import TopNavButton from "./TopNavButton.vue";
import Search from "./Search.vue";

export default {
  name: "TopNav",
  components: {
    TopNavButton,
    Search,
  },
  data() {
    return {
      searchData: [],
      isLoggedIn: false,
    };
  },
  mounted() {
    this.checkLoginStatus(); // 페이지 로드 시 로그인 상태 체크
    this.fetchStockData(); // 주식 데이터 로드
  },
  methods: {
    // 로그인 상태 확인 함수
    checkLoginStatus() {
      const token = localStorage.getItem("token");
      console.log("token:", token);
      const headers={
        "Content-Type": "application/json",
        Accept: "application/json",
        Authorization: `Bearer ${token}`,
      }
      if (token) {
        // 서버에 토큰 유효성 확인 요청 
        axios.post("https://port-0-capstonedesign-m3vkxnzga0885b97.sel4.cloudtype.app/user/api/token/verify/", {}, {headers})
        .then((response) => {
          if (response.data.valid) {
            console.log('로그인 성공');
            this.isLoggedIn = true;
            this.$forceUpdate();
          } else {
            this.removeToken();
            console.log('토큰이 유효하지 않습니다.');
            this.$forceUpdate();
          }
        })
        .catch((error) => {
          if (error.response) {
            console.log("서버 응답 에러", error.response.data); // 서버가 반환한 에러 메시지 출력
          } else if (error.request) {
            console.log("요청 에러", error.request); // 요청 자체에 문제가 있을 경우 출력
          } else {
            console.log("알 수 없는 에러", error.message); // 기타 에러
          }
          this.removeToken();
          this.$forceUpdate();
        });
      } else {
        this.isLoggedIn = false;
        console.log('로그인 실패')
        this.$forceUpdate();
      }
    },
    
    // 토큰 삭제 함수
    removeToken() {
      localStorage.removeItem("token"); 
      this.isLoggedIn = false;
    },

    // 홈으로 이동
    goToHome() {
      this.$router.push("/"); 
    },

    // 마이페이지로 이동 (로그인된 경우에만)
    goToMyPage() {
      if (this.isLoggedIn) {
        this.$router.push("/Mypage");
      } else {
        alert("로그인이 필요합니다.");
        this.$router.push("/login"); // 로그인 페이지로 리디렉션
      }
    },

    // 로그인/로그아웃 토글 함수
    toggleLoginStatus() {
      if (this.isLoggedIn) {
        this.logout(); // 로그인 상태일 때 로그아웃
      } else {
        this.$router.push("/login"); // 로그인 페이지로 이동
      }
    },

    // 로그아웃 처리
    logout() {
      this.removeToken(); // 토큰 삭제
      this.$router.push("/"); // 로그인 페이지로 리디렉션
    },

    // 주식 데이터 불러오기
    fetchStockData() {
      axios.get("https://port-0-capstonedesign-m3vkxnzga0885b97.sel4.cloudtype.app/stock/search_term/").then((response) => {
        this.searchData = response.data["output"];
      });
    },
  },
  watch: {
    // 로그인 상태 변경 시 콘솔에 로그 출력
    isLoggedIn(newValue) {
      if (newValue) {
        console.log("로그인 상태");
      } else {
        console.log("로그아웃 상태");
      }
    }
  }
};
</script>

<style scoped>
.TopNav {
  padding: 0px 20px;
  margin: 0px;
  display: flex;
  gap: 40px;
  height: 100px;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
  border-bottom: 1px solid lightgray;
  background-color: white;
  justify-content: center;
}

.TopNav ul {
  list-style: none;
  display: flex;
  gap: 40px;
  margin: 0;
  padding: 0;
}

.TopNav ul li {
  display: inline;
}

.auth-button {
  position: fixed;
  right: 5%;
  top: 2%;
  z-index: 1001;
}

.login-logout-button {
  background-color: #6dbdff;
  color: white;
  border: none;
  padding: 12px 24px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.3s, transform 0.2s;
}

.login-logout-button:hover {
  background-color: #6dbdff;
  transform: scale(1.05);
}

.login-logout-button:active {
  transform: scale(0.98);
}
</style>
