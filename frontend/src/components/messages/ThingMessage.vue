<template>
  <form class="thing-message-form" @submit.prevent="postThingMessage()">
    <div class="mb-3">
        <textarea class="form-control" v-model="newCommentText" placeholder="Напишите продавцу"></textarea>
    </div>
    <button type="submit" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
      Отправить сообщение
    </button>
    <modal/>
  </form>
</template>

<script>
import Modal from '../modals/Modal.vue'
export default {
  components: { Modal },
  name: "thing-message",
  data() {
    return {
      newCommentText: ""
    }
  },
  methods: {
    postThingMessage(){
      this.$emit("postMessage", this.newCommentText)
      this.newCommentText = ""
    }
  },
}
</script>

<style>

</style>