<template>
    <div style="display: flex; justify-content: center;">
        <div class="spinner"></div>
        <div>
           
            
        </div>
        
    </div>
    <div style="display: flex; justify-content: center;">
        <p>데이터를 불러오는 중입니다...</p>
    </div>
  </template>
  
  <script>
  export default {
  };
  </script>
  
  <style scoped>
  .loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.8);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .spinner {
    width: 40px;
    height: 40px;
    border: 5px solid rgba(0, 0, 0, 0.1);
    border-top: 5px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
  
  p {
    margin-top: 15px;
    font-size: 16px;
    color: #333;
  }
  </style>
  