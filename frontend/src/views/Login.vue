<template>
  <div class="v-login">
      <div v-if="inCorrectAuth" class="alert alert-danger" role="alert">
        Неправильные логин или пароль - проверьте правильность введенных вами данных!
      </div>
    <form @submit.prevent="login">
        <div class="mb-3">
            <label for="exampleInputEmail1" class="form-label">Логин</label>
            <input v-model="username" type="text" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
        </div>
        <div class="mb-3">
            <label for="exampleInputPassword1" class="form-label">Пароль</label>
            <input v-model="password" type="password" class="form-control" id="exampleInputPassword1">
        </div>
        
        <button type="submit" class="btn btn-primary">Войти</button>
    </form>
  </div>
</template>

<script>
export default {
    name: 'Login',
    data(){
        return {
            username: '',
            password: '',
            inCorrectAuth: false
        }
    },
    methods:{
        login(){
            this.$store.dispatch('userLogin', {
                username: this.username,
                password: this.password
            })
            .then(()=>{
                this.$router.push({name: 'Things'})
            })
            .catch(err =>{
                console.log(err)
                this.inCorrectAuth = true
            })
        } 
    }
}
</script>

<style>
</style>