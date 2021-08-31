<template>
  <div class="thing-card">
      <div class="card" style="width: 18rem;">
  <img v-bind:src="thing.image" class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">{{thing.title}}</h5>
    <p class="card-text">{{thing.content}}.</p>
  </div>
  <ul class="list-group list-group-flush">
    <li v-for="tag in thing.tags" :key="tag.id" class="list-group-item">{{tag.title}}</li>
  </ul>
  <div class="card-body">
    <a href="#" class="card-link">Подробнее</a>
  </div>
  <div class="card-body">
    <li class="list-group-item">Коментариев: {{thing.comments.length}}</li>
  </div>
</div>
  </div>
</template>

<script>
export default {
    name: "ThingCard",
    props:{
      thing:{
        type: Object,
        default: ()=>{}
      }
    },
    created() {
      
    },
}
</script>

<style>

</style>