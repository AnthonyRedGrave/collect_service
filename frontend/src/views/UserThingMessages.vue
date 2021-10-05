<template>
  <div class="userThingMessages-block">
      <h1>Ваши сообщения:</h1>
      <br>
      <div v-for="message in this.userThingMessage" :key="message.id" class="userThingMessages-card">
          <div class="userThingMessage-content">
              <h3>{{message.content}}</h3>
          <hr>
          </div>
          <div class="userThingMessage-thing">
              <h4>Под какой вещью оставлен: <p @click="showItem(message.thing)">{{message.thing_title}}</p></h4>    
          </div>
          <button style="margin: 15px;" class="btn btn-danger" @click="deleteMessage(message.id)">Удалить</button>
      </div>
      <br>
      <br>
      <h1>Ваши комментарии: </h1>
      <br>
      <div v-for="comment in this.userThingComments" :key="comment.id" class="userThingMessages-card">
          <div class="userThingMessage-content">
              <h3>{{comment.content}}</h3>
          <hr>
          </div>
          <div class="userThingMessage-thing">
              <h4><a @click="showItem(comment.object_id)">Вещь, под которой оставлен</a></h4>    
          </div>
          <button style="margin: 15px;" class="btn btn-danger" @click="deleteComment(comment.id)">Удалить</button>
      </div>
  </div>

</template>

<script>
import axios from 'axios'
export default {
    name: 'user_thing_messages',
    data() {
        return {
            userThingMessage: [],
            userThingComments: []
        }
    },
    created() {
        this.getUserThingMessages()
        this.getUserThingComments()
    },
    methods:{
        getUserThingMessages(){
            axios({
                method: "get",
                url: "http://localhost:8000/api/thing_messages/",
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
                })
                .then((responce) => {
                    this.userThingMessage = responce.data
                })
                .catch((err) => {
                console.log(err);
                });
        },
        showItem(thing_id){
            this.$router.push({path: 'thing-detail', query: {'thing_id': thing_id}})
        },
        getUserThingComments(){
            axios({
                method: "get",
                url: "http://localhost:8000/api/comments/",
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
                })
                .then((responce) => {
                    this.userThingComments = responce.data
                })
                .catch((err) => {
                console.log(err);
                });
        },
        deleteMessage(id){
            axios({
                method: "delete",
                url: `http://localhost:8000/api/thing_messages/${id}`,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
                })
                .then(() => {
                    this.getUserThingMessages()
                })
                .catch((err) => {
                console.log(err);
                });
        },
        deleteComment(id){
            axios({
                method: "delete",
                url: `http://localhost:8000/api/comments/${id}`,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
                })
                .then(() => {
                    this.getUserThingComments()
                })
                .catch((err) => {
                console.log(err);
                });
        }
    },
}
</script>

<style>
.userThingMessages-content{
}
.userThingMessages-card{
    border: 1px solid black;
    width: 500px;
    margin: 0 auto;
    background: #f0e4e4;   
}
.userThingMessages-card{
    height: auto;
}
</style>