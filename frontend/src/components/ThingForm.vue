<template>
  <div class="v-main">
    <form @submit.prevent="addThing">
      <label class="form-label">Название</label>
      <input v-model="title" type="text" id="inputTitle" />

      <label class="form-label">Состояние</label>
      <select v-model="state">
        <option value="Awesome">Лучшее</option>
        <option value="Good">Хорошее</option>
        <option value="Shabby">Потрепанное</option>
        <option value="Bad">Плохое</option>
      </select>

      <label class="form-label">Описание</label>
      <input v-model="content" type="text" id="inputContent" />

      <label class="form-label">Раздел</label>
      <select v-model="section">
        <option v-for="section in sections" :key='section.id' v-bind:value=section.id>{{section.title}}</option>
      </select>

      <!-- <label class="form-label">Теги</label>
      <select v-model="tags">
        <option v-for="tag in tags" :key='tag.id' v-bind:value=tag.id>{{tag.title}}</option>
      </select> -->

      <label class="form-label">Теги</label>
      <select v-model="tags">
        <option value="1">Вещи</option>
        <option value="2">Монетки</option>
      </select>

      <label class="form-label">Картинка</label>
      <input type="file" id="inputFile" />
      <button type="submit">Добавить</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: "thing-form",
  data() {
    return {
      sections: [],
      tags: [],
      title: "",
      content: "",
      image: "",
      state: "",
      section: "",
    };
  },
  mounted() {
    this.getSectionsList()
    // this.getTagsList()
  },
  methods: {
    getSectionsList(){
      axios
        .get("http://0.0.0.0:8000/api/sections/", {
          headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
        })
        .then((response) => {
          this.sections = response.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getTagsList(){
      axios
        .get("http://0.0.0.0:8000/api/tags/", {
          headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
        })
        .then((response) => {
          this.tags = response.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    addThing() {
      let data = {
        title: this.title,
        content: this.content,
        state: this.state,
        section: this.section,
        tags: this.tags
      };
      this.$emit("addThing", data);
    },
  },
};
</script>

<style>
</style>