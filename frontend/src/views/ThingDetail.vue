<template>
  <div class="thing-detail-block">
      <div class="thing-detail-wrapper">
          <div class="thing-detail-header">
              <div class="thing-detail-image-block">
                  <img v-bind:src="thing.image" class="thing-detail-image" alt="...">
              </div>
              <div class="thing-detail-info-block">
                  <div class="thing-detail-title-block">
                    <div v-if="username == thing.owner_name" class="thing-detail-title">
                        <input class="form-control title" :value=thing.title>
                        <button style="margin-top: 10px;" @click="changeElement('title')" class="btn btn-primary ">Изменить</button>
                    </div>
                    <div v-else class="thing-detail-title">
                        <h1>{{thing.title}}</h1>
                    </div>
                </div>
                <hr>
                <div v-if="username == thing.owner_name"  class="thing-detail-section">
                    <h1>{{thing.section_name}}</h1>
                    <select class="form-select section" aria-label="Default select example">
                    <option v-for="section in this.$store.state.section_choices" :key="section.id" :value=section.id>{{section.title}}</option>
                    </select>
                    <button style="margin-top: 15px; margin-bottom: 15px;" @click="changeElement('section')"  class="btn btn-primary">Изменить</button>
                </div>
                <div v-else class="thing-detail-section">
                    <h3>{{thing.section_name}}</h3>
                </div>
                <div v-if="username == thing.owner_name"  class="thing-detail-section">
                    <h1>Качество: {{thing.state}}</h1>
                    <select class="form-select state" aria-label="Default select example">
                    <option v-for="state in this.state_list" :key="state.id" :value=state.value>{{state.label}}</option>
                    </select>
                    <button style="margin-top: 15px; margin-bottom: 15px;" @click="changeElement('state')"  class="btn btn-primary">Изменить</button>
                </div>
                <div v-else class="thing-detail-section">
                    <h3>Качество: {{thing.state}}</h3>
                </div>
                <div class="thing-detail-tags-block">
                    <div v-if="username == thing.owner_name" style="margin-bottom: 15px;" class="thing-detail-tags">
                        <h3>Теги:</h3>
                        <p class="thing-detail-tag" v-for="tag in thing.tags" :key="tag.id">{{tag.title}}</p>
                        <div class="accordion-tag-block"><p class="accordion-tag-title" @click="chooseTags(tag.id)" v-for="tag in this.$store.state.tags" :key="tag.id">{{tag.title}}</p></div>
                        <button style="margin-top: 15px; margin-bottom: 15px;" @click="changeTags()" class="btn btn-primary">Изменить</button>
                    </div>
                    <div v-else class="thing-detail-tags">
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
                <div v-if="username == thing.owner_name" class="thing-detail-content">
                    <textarea class="form-control content" cols="80" rows="2" :value=thing.content></textarea>
                    <button style="margin-top: 15px;" @click="changeElement('content')" class="btn btn-primary">Изменить</button>
                </div>
                <div v-else class="thing-detail-content">
                    <h4>{{thing.content}}</h4>
                </div>
            <hr>
          </div>
          <div class="thing-detail-comments">
              <div class="thing-detail-comments-block">
                <comment-card v-for="comment in thing.comments" :key="comment.id" :comment="comment"/>
              </div>
              <div v-if="username !== thing.owner_name" class="thing-detail-comments-create">
                <comment-form @postComment = "postComment($event)"/>
              </div>
          </div>
          <hr>
          <div v-if="username !== thing.owner_name" class="thing-detail-call-owner-block">
              <h3>Свяжитесь с продавцом</h3>
              <thing-message @postMessage = "postMessage($event)"/>
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
            thing_title: "",
            thing_content: "",
            thing_state: "",
            thing_rates: {
                like: [],
                dislike: []
            },
            username: JSON.parse(localStorage.getItem('username')),
            chosed_tags: [],
            state_list: [{
                label: "Лучшее",
                value: "Awesome",
            },
            {
                label: "Хорошее",
                value: "Good",
            },
            {
                label: "Потрепанное",
                value: "Shabby",
            },
            {
                label: "Плохое",
                value: "Bad",
            }]
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
        },
        postMessage(newCommentText){
            axios({
                method: "post",
                url: `http://localhost:8000/api/things/${this.$route.query.thing_id}/message/`,
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
        },
        changeElement(thing_field){
            let element = document.querySelector(`.${thing_field}`)
            let data = {}
            data[thing_field] = element.value
            axios({
                method: "patch",
                url: `http://localhost:8000/api/things/${this.$route.query.thing_id}/`,
                data:data,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                })
                .then(() => {
                    this.getThing()
                })
                .catch((err) => {
                console.log(err);
                });
        },
        chooseTags(tag_id){
            this.chosed_tags.push(`${tag_id}`)
        },
        changeTags(){
            let data = {}
            data['tags'] = [...this.chosed_tags].toString()
            axios({
                method: "patch",
                url: `http://localhost:8000/api/things/${this.$route.query.thing_id}/`,
                data:data,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                })
                .then(() => {
                    this.getThing()
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

    .accordion-tag-block{
        display: flex;

    }

    .accordion-tag-title{
        margin: 5px;
    }
</style>