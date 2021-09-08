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
              </div>
              
          </div>
          <div class="thing-detail-content-block">
                    <div class="thing-detail-content">
                        <h4>{{thing.content}}</h4>
                    </div>
            <hr>
          </div>
      </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'ThingDetail',
    data() {
        return {
            thing: {},
            thing_rates: []
        }
    },
    created() {
        this.getThing()
        this.getRates()
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
        getRates(){
            let data = JSON.stringify({value: "like"})
            axios({
                method: "get",
                url: `http://localhost:8000/api/things/${this.$route.query.thing_id}/rate/`,
                params: data,
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                
                })
                .then((responce) => {
                this.thing_rates = responce.data
                })
                .catch((err) => {
                console.log(err);
                });
        }
    }
    
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
</style>