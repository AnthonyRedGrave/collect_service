<template>
  <NavBar/>
  <router-view/>
</template>

<script>
import NavBar from './components/NavBar.vue'

export default {
  name: 'App',
  components: {
    NavBar
  },
  created() {
    this.getAccessToken()
    
    this.getSectionChoices()
  },
  methods:{
    getAccessToken() {
      this.$store
        .dispatch("userLogin", {
          username: "admin",
          password: 12345,
        })
        .then(() => {})
        .catch((err) => {
          console.log(err);
        });
    },
    
    getSectionChoices(){
      this.$store
        .dispatch("thingSectionChoices", {
          token: this.$store.state.accessToken,
        })
        .then(() => {})
        .catch((err) => {
          console.log(err);
        });
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
