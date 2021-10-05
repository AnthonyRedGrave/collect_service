<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="container-fluid">
    <a class="navbar-brand" href="/">Коллекционерное бюро</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNavDropdown">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="/">Главная</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" @click="showUserThingMessages()">Ваши предложения</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Pricing</a>
        </li>
        <li v-if="username"  class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Связь
          </a>
          <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
            <li><a class="dropdown-item" @click="showMessages()">Сообщения</a></li>
            <li><a class="dropdown-item" @click="showChats()">Чаты</a></li>
          </ul>
        </li>
        <li v-if="username" class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Добрый день, {{username}}
          </a>
          <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
            <li><a class="dropdown-item" @click="ownerThings()">Ваши вещи</a></li>
            <li><a class="dropdown-item" @click="logOut()">Выйти</a></li>
          </ul>
        </li>
        <li v-else class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Войдите в аккаунт или зарегестрируйтесь!
          </a>
          <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
            <li><a class="dropdown-item" @click="login()">Войти</a></li>
            <li><a class="dropdown-item" @click="register()">Зарегестрироваться</a></li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</nav>
</template>

<script>
export default {
    name: "navbar",
    data() {
      return {
        username: JSON.parse(localStorage.getItem('username'))
      }
    },
    methods: {
      showMessages(){
        this.$router.push({path: 'messages'})
      },
      showChats(){
        this.$router.push({path: 'chats'})
      },
      login(){
        this.$router.push({path: 'login'})
      },
      logOut(){
        this.$store.dispatch('userLogout')
        this.$router.push({name: 'Things'})

      },
      ownerThings(){
        this.$router.push({name: 'own_things'})
      },
      showUserThingMessages(){
        this.$router.push({name: 'user_thing_messages'})
      }
    },
}
</script>

<style>

</style>