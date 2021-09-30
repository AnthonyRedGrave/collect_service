<template>
  <div class="owner-things-block">
      <h2>Ваши вещи</h2>
      <div class="things-list" v-if="owner_things.length !== 0">
        <thing-card v-for="thing in owner_things" :thing="thing" :key="thing.id"/>
        </div>
  </div>
</template>

<script>
import axios from 'axios'
import ThingCard from '../components/things/ThingCard.vue'
export default {
  components: { ThingCard },
    name: 'owner-things',
    data() {
        return {
            owner_things: []
        }
    },
    created() {
        this.getOwnerThings()
    },
    methods:{
        getOwnerThings(){
            axios({
                method: "get",
                url: "http://localhost:8000/api/things/own/",
                headers: {
                Authorization: `Bearer ${this.$store.state.accessToken}`,
                },
                credentials: "include",
                })
                .then((responce) => {
                this.owner_things = responce.data
                })
                .catch((err) => {
                console.log(err);
                });
        }
    }
}
</script>

<style>

</style>