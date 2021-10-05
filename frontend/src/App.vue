<template>
  <div v-if="username" class="">
    <Main/>
  </div>
  <div v-else class="">
    <h2>Пользоваться сервисом можно авторизованным пользователям!</h2>
    <login/>
  </div>
</template>

<script>
import Login from './views/Login.vue';
import Main from './views/Main.vue';

export default {
  name: 'App',
  components: {
    Main,
    Login
  },
  data() {
    return {
      username: JSON.parse(localStorage.getItem('username'))
    }
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
}
</style>
