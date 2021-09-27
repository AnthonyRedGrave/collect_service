<template>
  <div class="comment-card-block">
      <div class="comment-card-block-title">
          <div class="comment-card-user">
            {{comment.user_name}} 
          </div>
          <div class="comment-card-time">
            16:21 17-11-2000
          </div>
      </div>
      
      <div class="comment-card-content">
          {{comment.content}}
      </div>
  </div>
</template>

<script>
export default {
    name: 'CommentCard',
    props: {
        comment:{
            type: Object,
            default: ()=>{}
        }
    }
}
</script>

<style>
    .comment-card-block{
        border: 1px solid black;
        border-radius: 15px 15px 0 0;
        margin: 0 0 15px 25px;
        min-height: 90px;
        min-width: 270px;
    }
    .comment-card-block-title{
        display: flex;
        padding: 10px;
        justify-content: space-between;
        border-bottom: 1px solid black;
    }
    .comment-card-user{
        font-size: 19px;
    }
    .comment-card-content{
        height: 90px;
        padding: 10px;
        text-align: left;
        background: #ced4da;
    }
</style>