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
  methods: {
    // Google 로그인 초기화
    initializeGoogleLogin() {
      google.accounts.id.initialize({
        client_id: "411762794275-vpjchb1sc9dgpu2ar25tkbb60u82o52o.apps.googleusercontent.com",
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

    // Google 인증 응답 처리
    handleCredentialResponse(response) {
      console.log("Google Credential Response:", response);

      fetch("http://localhost:8000/api/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ credential: response.credential }),
      })
        .then((res) => {
          if (res.ok) {
            return res.json();
          } else {
            return res.json().then((data) => {
              console.error("Failed to save user:", data);
              alert("Failed to save user information: " + (data.error || "Unknown error"));
            });
          }
        })
        .then((data) => {
          if (data) {
            console.log("User saved successfully:", data);
            alert("Login successful!");
            this.$router.push("/Mypage"); // 로그인 성공 시 마이페이지로 이동
          }
        })
        .catch((error) => {
          console.error("Network Error:", error);
          alert("An error occurred while saving user information.");
        });
    },
  },
  mounted() {
    this.initializeGoogleLogin(); // Google 로그인 초기화
  },
};
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #74ebd5, #acb6e5);
  font-family: 'Arial', sans-serif;
}

.login-container {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
  text-align: center;
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
