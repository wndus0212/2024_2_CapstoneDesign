<template>
    <div class="search">
      <input type="text" class="search__input" placeholder="Search...">
      <div class="search__icon">
        <ion-icon name="search"></ion-icon>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SearchBar'
  }
  </script>
  
  <style scoped>
  .search {
    grid-column: 3 / 4;
    grid-row: 2 / 3;
    position: relative;
    display: flex;
    align-items: center;
  }
  
  .search__input {
    width: 20.4rem;
    height: 4rem;
    border: none;
    border-radius: 1rem;
    font-size: 1.4rem;
    padding-left: 3.8rem;
    box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1); /* inner shadow 대신 */
    background: none;
    font-family: inherit;
    color: var(--greyDark);
  }
  
  .search__input::placeholder {
    color: var(--greyLight-3);
  }
  
  .search__input:focus {
    outline: none;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* shadow 대신 */
  }
  
  .search__input:focus + .search__icon {
    color: var(--primary);
  }
  
  .search__icon {
    height: 2rem;
    position: absolute;
    font-size: 2rem;
    padding: 0 1rem;
    display: flex;
    color: var(--greyDark);
    transition: color 0.3s ease;
  }
  </style>
  