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
    checkLoginStatus() {
      const token = localStorage.getItem("token");
      if (token) {
        // 서버에 토큰 유효성 확인 요청 (예시)
        axios
          .post("http://127.0.0.1:8000/api/token/verify/", { token })
          .then((response) => {
            if (response.data.valid) {
              this.isLoggedIn = true;
            } else {
              localStorage.removeItem("token"); // 유효하지 않으면 토큰 삭제
              this.isLoggedIn = false;
            }
          })
          .catch(() => {
            localStorage.removeItem("token"); // 오류 시 토큰 삭제
            this.isLoggedIn = false;
          });
      } else {
        this.isLoggedIn = false;
      }
    },
    goToHome() {
      this.$router.push("/");
    },
    goToMyPage() {
      if (this.isLoggedIn) {
        this.$router.push("/Mypage");
      } else {
        alert("로그인이 필요합니다.");
        this.$router.push("/login"); // 로그인 페이지로 리디렉션
      }
    },
    toggleLoginStatus() {
      if (this.isLoggedIn) {
        this.logout();
      } else {
        this.$router.push("/login");
      }
    },
    login() {
      // 로그인 처리 (예시)
      this.isLoggedIn = true;
      localStorage.setItem("token", "user-token"); // 실제 토큰을 저장해야 합니다.
      this.$router.push("/Mypage");
    },
    logout() {
      localStorage.removeItem("token");
      this.isLoggedIn = false;
      this.$router.push("/login");
    },
    fetchStockData() {
      axios.get("http://127.0.0.1:8000/stock/search_term/").then((response) => {
        this.searchData = response.data["output"];
      });
    },
  },
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
  background-color: #6dbdff; /* 초록색 배경 */
  color: white; /* 흰색 텍스트 */
  border: none;
  padding: 12px 24px; /* 버튼 크기 */
  font-size: 16px; /* 텍스트 크기 */
  cursor: pointer; /* 클릭 가능 포인터 */
  border-radius: 8px; /* 둥근 모서리 */
  transition: background-color 0.3s, transform 0.2s; /* 배경 색과 크기 변화에 애니메이션 추가 */
}

.login-logout-button:hover {
  background-color: #6dbdff; /* 호버 시 배경 색 변화 */
  transform: scale(1.05); /* 클릭 시 약간 커짐 */
}

.login-logout-button:active {
  transform: scale(0.98); /* 클릭 시 약간 작아짐 */
}
</style>
