<template>
  <form class="comment-form" @submit.prevent="postComment()">
    <div class="mb-3">
        <label for="exampleInputEmail1" class="form-label">Текст комментария</label>
        <textarea class="form-control" v-model="newCommentText" placeholder="Текст комментария"></textarea>
    </div>
    <button type="submit" class="btn btn-primary">Опубликовать комментарий</button>
  </form>
</template>

<script>
export default {
    name: 'CommentForm',
    data() {
        return {
            newCommentText: ""
        }
    },
    methods:{
        postComment(){
            this.$emit("postComment", this.newCommentText)
        }
    }
}
</script>

<style>
    .comment-form{
        width: 500px;
    }
</style>