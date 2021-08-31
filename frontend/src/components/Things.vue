<template>
  <div class="form-wrapper">
    <filter-form/>
  </div>
  <div class="things-list">
    <ThingCard v-for="thing in things" :thing="thing" :key="thing.id"/>
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
    };
  },
  mounted() {
    
    this.getThingsList();
  },
  methods: {
    getThingsList() {
      axios
        .get("http://0.0.0.0:8000/api/things/", {
          headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
        })
        .then((response) => {
          this.things = response.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    addThing(thing_data) {
      console.log(thing_data);

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
}
</style>