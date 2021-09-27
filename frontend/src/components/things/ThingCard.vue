<template>
  <div class="thing-card">
      <div class="card" style="width: 18rem;">
  <img @click="showItem(thing.id)" v-bind:src="thing.image" class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">{{thing.title}}</h5>
    <p class="card-text">{{thing.content}}.</p>
  </div>
  <ul class="list-group list-group-flush">
    <li class="list-group-item">{{thing.section_name}}</li>
  </ul>
  <div class="card-body thing-tags-block">
    <p v-for="tag in thing.tags" :key="tag.id" class="tag-item">{{tag.title}}</p>
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
    methods:{
      showItem(thing_id){
        this.$router.push({path: 'thing-detail', query: {'thing_id': thing_id}, props: {thing: this.thing}})
      }
    }
}
</script>

<style>
  .thing-tags-block{
    display: flex;
    padding: 10px;
    justify-content: space-between;
    width: 268px;
    flex-flow: wrap;

  }
  .tag-item{
    border: 1px solid black;
    border-radius: 3px;
    padding: 3px;
    margin: 3px;
  }
</style>