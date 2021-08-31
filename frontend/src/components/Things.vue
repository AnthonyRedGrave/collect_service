<template>
  <div class="things">
    <div class="thing" v-for="thing in things" :key="thing.id">
      {{ thing }}
    </div>
  </div>
  <ThingForm @addThing="addThing($event)"/>
</template>

<script>
import axios from "axios";
import ThingForm from "@/components/ThingForm.vue";
export default {
  name: "Things",
  components: {
    ThingForm,
  },
  data() {
    return {
      things: [],
    };
  },
  mounted() {
    this.getAccessToken();
    this.getThingsList();
  },
  methods: {
    getAccessToken() {
      this.$store
        .dispatch("userLogin", {
          username: "admin",
          password: 12345,
        })
        .then(() => {})
        .catch((err) => {
          console.log(err);
        });
    },
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
</style>