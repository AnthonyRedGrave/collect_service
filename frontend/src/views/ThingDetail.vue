<template>
  <div class="thing-detail-block">
      <div class="thing-detail-wrapper">
          <div class="thing-detail-header">
              <div class="thing-detail-image-block">
                  <img v-bind:src="thing.image" class="thing-detail-image" alt="...">
              </div>
              <div class="thing-detail-info-block">
                  <div class="thing-detail-title-block">
                    <div class="thing-detail-title">
                        <h1>{{thing.title}}</h1>
                    </div>
                </div>
                <hr>
                <div class="thing-detail-section">
                    <h3>{{thing.section_name}}</h3>
                </div>
                <div class="thing-detail-tags-block">
                    <div class="thing-detail-tags">
                        <h3>Теги:</h3>
                        <p class="thing-detail-tag" v-for="tag in thing.tags" :key="tag.id">{{tag.title}}</p>
                    </div>
                </div>
                <div class="thing-detail-rates-block">
                    <div class="thing-detail-likes">
                        <button @click="postRates('like')" class="btn btn-success">Понравилось: {{thing_rates.like.length}}</button>
                    </div>
                    <div class="thing-detail-dislikes">
                        <button @click="postRates('dislike')" class="btn btn-danger">Не понравилось: {{thing_rates.dislike.length}}</button>
                    </div>
                </div>
              </div>
              
          </div>
          <div class="thing-detail-content-block">
                <div class="thing-detail-content">
                    <h4>{{thing.content}}</h4>
                </div>
            <hr>
          </div>
          <div class="thing-detail-comments">
              <div class="thing-detail-comments-block">
                <comment-card v-for="comment in thing.comments" :key="comment.id" :comment="comment"/>
              </div>
              <div class="thing-detail-comments-create">
                <comment-form @postComment = "postComment($event)"/>
              </div>
          </div>
          <hr>
          <div class="thing-detail-call-owner-block">
              <h3>Свяжитесь с продавцом</h3>
              <thing-message/>
          </div>
          
      </div>
  </div>
</template>

<script>
import axios from 'axios'
import CommentCard from '../components/comments/CommentCard.vue'
import CommentForm from '../components/comments/CommentForm.vue'
import ThingMessage from '../components/messages/ThingMessage.vue'
export default {
    name: 'ThingDetail',
    components:{
        CommentCard,
        CommentForm,
        ThingMessage
    },
    data() {
        return {
            thing: {},
            thing_rates: {
                like: [],
                dislike: []
            }
        }
    },
    created() {
        this.getThing()
        this.getRates('like')
        this.getRates('dislike')
    },
    methods:{
        getThing(){
            axios({
                method: "get",
                url: `http://localhost:8000/api/things/${this.$route.query.thing_id}`,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
                })
                .then((responce) => {
                this.thing = responce.data
                })
                .catch((err) => {
                console.log(err);
                });
        },
        getRates(rate){
            axios({
                method: "get",
                url: `http://localhost:8000/api/things/${this.$route.query.thing_id}/rate/?value=${rate}`,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                })
                .then((responce) => {
                    this.thing_rates[rate] = (responce.data)
                })
                .catch((err) => {
                console.log(err);
                });
        },
        postRates(rate){
            axios({
                method: "post",
                url: `http://localhost:8000/api/things/${this.$route.query.thing_id}/rate/`,
                data:{
                    value: rate
                },
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                
                })
                .then((responce) => {
                this.pushThingRate(responce.data, rate)
                })
                .catch((err) => {
                console.log(err);
                });
        },
        pushThingRate(new_rate, rate){
            if (new_rate.value == null){
                let rate_id_to_delete = this.thing_rates[rate].indexOf(this.thing_rates[rate].find(x => x.username = this.$store.state.username))
                this.thing_rates[rate].splice(rate_id_to_delete, 1)
            }
            else{
                this.thing_rates[rate].push(new_rate)
                if (rate == 'like'){
                    let rate_id_to_delete = this.thing_rates['dislike'].indexOf(this.thing_rates['dislike'].find(x => x.username = this.$store.state.username))
                    this.thing_rates['dislike'].splice(rate_id_to_delete, 1)
                }
                else{
                    let rate_id_to_delete = this.thing_rates['like'].indexOf(this.thing_rates['like'].find(x => x.username = this.$store.state.username))
                    this.thing_rates['like'].splice(rate_id_to_delete, 1)
                }
                
            }
        },
        getComments(){
            axios({
                method: "get",
                url: `http://localhost:8000/api/things/${this.$route.query.thing_id}/comment/`,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                
                })
                .then((responce) => {
                this.thing.comments = responce.data
                })
                .catch((err) => {
                console.log(err);
                });
        },
        postComment(newCommentText){
            axios({
                method: "post",
                url: `http://localhost:8000/api/things/${this.$route.query.thing_id}/comment/`,
                data:{
                    content: newCommentText
                },
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                
                })
                .then(() => {
                this.getComments()
                })
                .catch((err) => {
                console.log(err);
                });
        }
    },
    
    
}
</script>

<style>
    .thing-detail-block{
        width: 1920px;
    }
    .thing-detail-wrapper{
        margin: 0% 15%;
    }

    .thing-detail-header{
        display: flex;
        margin-top: 25px;
    }
    .thing-detail-image{
        width: 400px;
        margin: 0px 15px 15px 0px;
    }
    .thing-detail-title{
        margin-bottom: 15px;
        text-align: left;
    }

    .thing-detail-section{
        text-align: left;
    }

    .thing-detail-tags-block{
        text-align: left;

    }
    .thing-detail-tags{
        display: flex;
    }
    .thing-detail-tag{
        padding: 5px;
    }

    .thing-detail-content-block{
        margin-top: 50px;
    }

    .thing-detail-rates-block{
        display: flex;
        width: 330px;
        justify-content: space-between;

    }

    .thing-detail-comments-block{
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    .thing-detail-comments{
        display: flex;
    }
    .thing-detail-comments-create{
        margin-left: 150px;
    }
</style>