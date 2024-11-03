<template>
    <div class="searchBar">
      <input type="text" class="textInput"/>
      <span class="search-icon">🔍</span>
    </div>
  </template>
  <script>
  
  export default {
    name: 'SearchBar'
  }
  </script>
  <style>
    .searchBar{
        margin-bottom: 20px;
        background-color: white;
        height: 40px;
        width: 250px;
        border-radius: 10px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
    }
    
    .textInput{
      border: none;
      outline: none;
      width: 80%;
      height: 90%;
      font-size: 20px;
    }
  </style>