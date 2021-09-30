<template>
  <div v-if="username" class="">
    <div class="form-wrapper">
      <filter-form @filteringThings="filteringThings($event)" @dropFilters = "dropFilters($event)"/>
    </div>
    <div class="things-list" v-if="things.length !== 0">
      <ThingCard v-for="thing in things" :thing="thing" :key="thing.id"/>
    </div>
    <div v-else class="no-items-block">
        <h2>К сожалению, вещей не нашлось</h2>
    </div>
  </div>
  <div v-else class="">
    <h2>Пользоваться сервисом можно авторизованным пользователям!</h2>
  </div>
    

  
</template>

<script>
import axios from "axios";
import ThingCard from "./things/ThingCard.vue"
import FilterForm from "./things/FilterForm.vue"

export default {
  name: "Things",
  components: {
    ThingCard,
    FilterForm
  },
  data() {
    return {
      things: [],
      username: JSON.parse(localStorage.getItem('username'))
    }
  },
  created() {
    this.getThingList()
  },
  methods: {
    getThingList(){
      this.$store.dispatch("getThingList", {
        token: this.$store.state.accessToken,
      })
      .then((response) => {
        this.things = response.data
      })
        .catch((err) => {
          console.log(err);
        });
    },
    addThing(thing_data) {
      axios({
        method: "post",
        url: "http://localhost:8000/api/things/",
        data: thing_data,
        headers: {
          Authorization: `Bearer ${this.$store.state.accessToken}`,
        },
        credentials: "include",
      })
        .then((responce) => {
          console.log(responce);
          this.things.push(responce.data)
        })
        .catch((err) => {
          console.log(err);
        });
    },
    filteringThings(filtered_things){
      this.things = filtered_things
    },
    dropFilters(){
      this.things = this.$store.state.things
    }
  },
};
</script>

<style>
.things-list{
  display: flex;
  justify-content: space-between;
  margin: 0 auto;
  width: 900px;
  flex-flow: wrap;
  z-index: 1;
}
.form-wrapper{
  z-index: 6;
}
</style>