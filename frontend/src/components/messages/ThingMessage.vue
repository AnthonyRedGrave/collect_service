<template>
  <form class="thing-message-form" @submit.prevent="postThingMessage()">
    <div class="mb-3">
        <textarea class="form-control" v-model="newCommentText" placeholder="Напишите продавцу"></textarea>
    </div>
    <button type="submit" class="btn btn-primary">Отправить сообщение</button>
  </form>
</template>

<script>
export default {

}
</script>

<style>

</style>