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
            <div v-for="message in messages" :key="message.id" class="chat_list">
              <div class="chat_people">
                <div class="chat_img"> <img src="https://ptetutorials.com/images/user-profile.png" alt="sunil"> </div>
                <div class="chat_ib">
                  <h6>Оставлен под вещью <b>{{message.thing_title}}</b></h6>
                  <h5>{{message.user_name}}</h5>
                  <p>{{message.content}}</p>
                  <div class="start_chat">
                  <button type="button" class="btn btn-primary">Начать чат</button>
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
}
</script>

<style>

</style>