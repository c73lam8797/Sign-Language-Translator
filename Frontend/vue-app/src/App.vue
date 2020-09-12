<template>
  <div id="app">
    <Title msg="Sign Language Translator"/>
    <Navbar />
    <Home />
  </div>
</template>

<script>
import Title from './components/Title.vue';
import Navbar from './components/Navbar.vue';
import Home from './components/Home.vue';

export default {
  name: 'App',
  components: {
    Title,
    Navbar,
    Home
  }
}

console.log(process.env.NODE_ENV)
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
