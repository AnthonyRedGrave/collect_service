<template>
    <div class="container">
      <div class="messaging">
        <div class="inbox_people">
          <div class="headind_srch">
            <div class="recent_heading">
              <h4>Чаты</h4>
            </div>
            <div class="srch_bar">
              <div class="stylish-input-group">
                <input type="text" class="search-bar"  placeholder="Поиск чатов">
                <span class="input-group-addon">
                <button type="button"> <i class="fa fa-search" aria-hidden="true"></i> </button>
                </span> </div>
            </div>
          </div>
          <div class="inbox_chat">
            <div v-for="chat in chats" :key="chat.id" class="chat_list">
              <div class="chat_people">
                <div class="chat_img"> <img src="https://ptetutorials.com/images/user-profile.png" alt="sunil"> </div>
                <div class="chat_ib">
                  <h6>Вещь разговора <b>{{chat.thing}}</b></h6>
                  <h5>{{chat.member_1}}</h5>
                  <h5>{{chat.member_2}}</h5>
                  <div class="start_chat">
                  <button type="button" @click="continueChat(chat.id)" class="btn btn-primary">Продолжить чат</button>
                </div>
                </div>
                
              </div>
            </div>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
export default {
    name: 'ThingChatsList',
    data(){
      return{
        chats: []
      }
    },
    created() {
      this.getChatsList()
    },
    methods:{
      getChatsList(){
        this.$store.dispatch("getChatsList", {
        token: this.$store.state.accessToken,
      })
      .then((response) => {
        this.chats = response.data
      })
        .catch((err) => {
          console.log(err);
        });
      },
      continueChat(chat_id){
        this.$router.push({path: 'chat', query: {'chat_id': chat_id}})
        
      }
    }
}
</script>

<style>

</style>