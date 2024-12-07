<template>
  <div class="login-page">
    <div class="login-container">
      <h1 class="title">환영합니다</h1>
      <p class="subtitle">계속하려면 로그인하세요</p>
      <!-- Google 로그인 버튼이 렌더링될 DOM 요소 -->
      <div id="google-login-button"></div>
    </div>
  </div>
</template>

<script>
/* global google */ // google 전역 객체를 ESLint에 선언

export default {
  data() {
    return {
      isLoggedIn: false,  // 로그인 상태를 추적
    };
  },
  methods: {
    // Google 로그인 초기화
    initializeGoogleLogin() {
      google.accounts.id.initialize({
        client_id: "700784575917-c4vrf3c2gf7auollkkonsgrao3sr6191.apps.googleusercontent.com",
        callback: this.handleCredentialResponse, // 인증 후 실행할 콜백 함수
      });

      // Google 로그인 버튼 렌더링
      google.accounts.id.renderButton(
        document.getElementById("google-login-button"),
        {
          theme: "outline", // 버튼 테마
          size: "large",    // 버튼 크기
        }
      );

      google.accounts.id.prompt(); // 자동 로그인 프롬프트
    },
    login(token) {
      this.isLoggedIn = true;  // 로그인 상태 변경
      localStorage.setItem("token", token);  // 실제 토큰을 저장
      this.$router.push("/Mypage");  // 마이페이지로 리디렉션
    },
    // Google 인증 응답 처리
    handleCredentialResponse(response) {


      // 서버로 사용자 인증 정보를 전송하여 토큰을 받음
      fetch("http://127.0.0.1:8000/user/api/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ credential: response.credential }),
      })
        .then((res) => res.json()) // 응답 받은 데이터
        .then((data) => {
          if (data) {
            console.log("User saved successfully:", data);
            // 서버에서 받은 token을 로컬 스토리지에 저장하고 로그인 상태 갱신
            localStorage.setItem("token", data.token); 
            this.login(data.token);  // login 함수 호출
          }
        })
        .catch((error) => {
          console.error("Network Error:", error);
          alert("An error occurred while saving user information.");
        });
    }
  },
  mounted() {
    this.initializeGoogleLogin();  // Google 로그인 초기화
  },
};
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-family: 'Arial', sans-serif;
}

.login-container {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
  text-align: center;
  width: 500px;
}

.title {
  font-size: 2.5em;
  color: #333;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.2em;
  color: #666;
  margin-bottom: 30px;
}

#google-login-button {
  margin-top: 20px;
}
</style>
