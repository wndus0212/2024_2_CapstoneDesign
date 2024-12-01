<template>
  <div>
    <h1>Google Login</h1>
    <!-- Google 로그인 버튼이 렌더링될 DOM 요소 -->
    <div id="google-login-button"></div>
  </div>
</template>

<script>
/* global google */ // google 전역 객체를 ESLint에 선언

export default {
  methods: {
    initializeGoogleLogin() {
      // GIS 초기화
      google.accounts.id.initialize({
        client_id: "411762794275-vpjchb1sc9dgpu2ar25tkbb60u82o52o.apps.googleusercontent.com",
        callback: this.handleCredentialResponse, // 인증 후 실행할 콜백 함수
      });

      // Google 로그인 버튼 렌더링
      google.accounts.id.renderButton(
        document.getElementById("google-login-button"), // 버튼을 렌더링할 DOM 요소
        {
          theme: "outline", // 버튼 테마
          size: "large",    // 버튼 크기
        }
      );

      // 자동 로그인 프롬프트 (선택 사항)
      google.accounts.id.prompt();
    },
    handleCredentialResponse(response) {
      console.log("Google Credential Response:", response);

      // Google ID 토큰을 Django 백엔드로 전송
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
          }
        })
        .catch((error) => {
          console.error("Network Error:", error);
          alert("An error occurred while saving user information.");
        });
    },
  },
  mounted() {
    this.initializeGoogleLogin(); // 컴포넌트가 마운트될 때 Google 로그인 초기화
  },
};
</script>

<style scoped>
#google-login-button {
  margin: 20px 0;
}
</style>


