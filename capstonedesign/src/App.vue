<template>
  <TopNav/>
  <div>
    <containerBox>
      <p>
        hello
      </p>
    </containerBox>
    <containerBox>
      <p>
        hello
      </p>
    </containerBox>
    <containerBox>
      <p>
        hello
      </p>
    </containerBox>
  </div>
</template>

<script>
import TopNav from './components/Top.vue'
import containerBox from './components/Box.vue'
export default {
  name: 'App',
  components: {
    TopNav,
    containerBox
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0px;
  padding: 0px;
}
</style>
