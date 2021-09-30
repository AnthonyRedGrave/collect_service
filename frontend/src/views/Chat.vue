<template>
<div class="container content">
    <div class="row">
        <div class="col-xl-12 col-lg-12 col-md-12 col-sm-24 col-22">
            <div class="card">
            <div class="card-header">Chat</div>
                <div class="card-body height12">
                    <ul class="chat-list">
                        <li v-for="message in chat_messages" :class="chatMessageClass(message)" :key="message.id">
                            <div class="chat-img">
                                <img alt="Avtar" src="https://bootdey.com/img/Content/avatar/avatar1.png">
                            </div>
                            <div class="chat-body">
                                <div class="chat-message">
                                    <h5>{{message.user_name}}</h5>
                                    <p>{{message.content}}</p>
                                </div>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="message_input">
                <form class="thing-message-form" @submit.prevent="postMessage()">
                    <div class="mb-3">
                        <textarea class="form-control inputMessage" v-model="newMessageText" placeholder="Напишите сообщение"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
                    Отправить сообщение
                    </button>
                </form>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import axios from 'axios'
export default {
    name: "Chat",
    data() {
        return {
            chat_messages: [],
            newMessageText: "",
        }
    },
    created() {
        this.getChatMessages()
    },
    methods:{
        getChatMessages(){
            axios({
              method: "get",
              url: `http://localhost:8000/api/chats/${this.$route.query.chat_id}/messages/`,
              headers: {
              Authorization: `Bearer ${this.$store.state.accessToken}`,
              },
              })
              .then((response) => {
                  this.chat_messages = response.data
              })
              .catch((err) => {
              console.log(err);
              });
        },
        chatMessageClass(message){
            return{
                in: JSON.parse(localStorage.getItem('username')) === message.user_name,
                out: JSON.parse(localStorage.getItem('username')) !== message.user_name
            }
        },
        postMessage(){
            axios({
              method: "post",
              url: `http://localhost:8000/api/chats/${this.$route.query.chat_id}/messages/`,
              data:{
                  content: this.newMessageText,
                  chat: this.$route.query.chat_id
              },
              headers: {
              Authorization: `Bearer ${this.$store.state.accessToken}`,
              },
              })
              .then(() => {
                  this.newMessageText = ""
                  this.getChatMessages()
              })
              .catch((err) => {
              console.log(err);
              });
        }
    }

}
</script>

<style scoped>
.message_input{
    margin-top: 3px;
}
.chat-list {
    padding: 0;
    font-size: .8rem;
}

.chat-list li {
    margin-bottom: 10px;
    overflow: auto;
    color: #ffffff;
}

.chat-list .chat-img {
    float: left;
    width: 48px;
}

.chat-list .chat-img img {
    -webkit-border-radius: 50px;
    -moz-border-radius: 50px;
    border-radius: 50px;
    width: 100%;
}

.chat-list .chat-message {
    -webkit-border-radius: 50px;
    -moz-border-radius: 50px;
    border-radius: 50px;
    background: #5a99ee;
    display: inline-block;
    padding: 10px 20px;
    position: relative;
}

.chat-list .chat-message:before {
    content: "";
    position: absolute;
    top: 15px;
    width: 0;
    height: 0;
}

.chat-list .chat-message h5 {
    margin: 0 0 5px 0;
    font-weight: 600;
    line-height: 100%;
    font-size: .9rem;
}

.chat-list .chat-message p {
    line-height: 18px;
    margin: 0;
    padding: 0;
}

.chat-list .chat-body {
    margin-left: 20px;
    float: left;
    width: 15%;
}

.chat-list .in .chat-message:before {
    left: -12px;
    border-bottom: 20px solid transparent;
    border-right: 20px solid #5a99ee;
}

.chat-list .out .chat-img {
    float: right;
}

.chat-list .out .chat-body {
    float: right;
    margin-right: 20px;
    text-align: right;
}

.chat-list .out .chat-message {
    background: #fc6d4c;
}

.chat-list .out .chat-message:before {
    right: -12px;
    border-bottom: 20px solid transparent;
    border-left: 20px solid #fc6d4c;
}

.card .card-header:first-child {
    -webkit-border-radius: 0.3rem 0.3rem 0 0;
    -moz-border-radius: 0.3rem 0.3rem 0 0;
    border-radius: 0.3rem 0.3rem 0 0;
}
.card .card-header {
    background: #17202b;
    border: 0;
    font-size: 1rem;
    padding: .65rem 1rem;
    position: relative;
    font-weight: 600;
    color: #ffffff;
}

.content{
    margin-top:40px;    
}
</style>