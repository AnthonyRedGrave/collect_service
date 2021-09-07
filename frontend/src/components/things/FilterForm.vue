<template>
  <div class="filter-form">
      <form class="form-filter" action="">
        <div class="thing-title-check-form">
            <div class="form-check">
                <input class="form-check-input ordering" type="radio" name="flexRadioDefault" id="flexRadioOrderingTitle1" @click="simplefilteringThings('ordering','title')">
                <label class="form-check-label" for="flexRadioOrderingTitle1">
                    От А до Я
                </label>
            </div>
            <div class="form-check">
            <input class="form-check-input ordering" type="radio" name="flexRadioDefault" id="flexRadioOrderingTitle2" @click="simplefilteringThings('ordering','-title')">
            <label class="form-check-label" for="flexRadioOrderingTitle2">
                От Я до А
            </label>
            </div>
        </div>
        <select id="thing-state-select-form" class="form-select filtering" @change="simplefilteringThings('state', filterState)" v-model="filterState" aria-label="Default select example">
            <option v-for="state in this.state_list" :key="state.id" v-bind:value=state.value>{{state.label}}</option>
        </select>
        <select id="thing-section-select-form" class="form-select filtering" @change="simplefilteringThings('section', filterSection)" v-model="filterSection" aria-label="Default select example">
            <option v-for="section in this.$store.state.section_choices" :key="section.id" v-bind:value=section.id>{{section.title}}</option>
        </select>
        <div class="accordion accordion-flush tags-filter-block" id="accordionFlushExample">
            <div class="accordion-item">
                <h2 class="accordion-header" id="flush-headingOne">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
                    Выберите теги
                </button>
                </h2>
                <div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" data-bs-parent="#accordionFlushExample">
                <div class="accordion-body"><p class="accordion-tag-title" @click="simplefilteringThings('tags', tag.id)" v-bind:id="tag.id" v-for="tag in tags" :key="tag.id">{{tag.title}}</p></div>
                </div>
            </div>
        </div>
        <div class="drop-filters-button">
            <button type="button" class="btn btn-success" @click="dropFilters()">Сбросить фильтры</button>
        </div>
      </form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
    name: "filter-form",
    data() {
        return {
            filterState: "",
            filterSection: "",
            filters: {
                state: [],
                section: [],
                tags: [],
                ordering: ""
            },
            ordering: null,
            tags: [],
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
    mounted() {
        this.getThingTags()
    },
    methods:{
        getThingTags(){
            this.$store.dispatch("getThingTagsList", {
                token: this.$store.state.accessToken,
            })
            .then((response) => {
                this.tags = response.data
            })
                .catch((err) => {
                console.log(err);
                });
        },
        simplefilteringThings(filtername, value){
            let filter = {
                filtername: filtername,
                value: value
            }
            this.getCorrectFilters(filter)
            let tags = this.getFieldValue('tags')
            let state = this.getFieldValue('state')
            let section = this.getFieldValue('section')
            this.ordering = this.filters.ordering
            var qs = require('qs');
            axios
                .get(`http://0.0.0.0:8000/api/things/`, {
                headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
                params: {
                    tags: tags,
                    state: state,
                    section: section,
                    order_by: this.ordering
                },
                paramsSerializer: function(params) {
                    return qs.stringify(params, {arrayFormat: 'repeat'})
                },
                })
                .then((response) => {
                    this.$emit('filteringThings', response.data)
                })
                .catch((err) => {
                    console.log(err);
                });
        },
        getFieldValue(name){
            if (name == "tags"){
                let tags = []
                this.filters[name].forEach(element => {
                    tags.push(element.value)
                });
                return tags
            }
            else {
                if (this.filters[name].length == 0){
                    return null
                }
                return this.filters[name][0].value
            }
        },
        getCorrectFilters(filter){
            let filterValues = this.filters[filter.filtername].map(function (el) {return el.value})
            if (filterValues.includes(filter.value)){
                for(let i = 0;i<filterValues.length;i++){
                        if (this.filters[filter.filtername][i].value == filter.value){
                            this.filters[filter.filtername].splice(i, 1)
                        }
                }
            }
            else{
               if (filter.filtername == "tags"){
                    this.filters.tags.push(filter)   
                }
                else{
                    if (filter.filtername == "ordering"){
                        this.filters[filter.filtername] = filter.value
                        return
                    }
                    this.filters[filter.filtername].splice(0, 1)
                    this.filters[filter.filtername].push(filter)

                } 
            } 
        },
        dropFilters(){
            this.filters = {
                state: [],
                section: [],
                tags: [],
                ordering: ""
            }
            let orderings = document.querySelectorAll(".ordering")
            orderings.forEach(element => {
                element.checked = false
            });
            let filters = document.querySelectorAll(".filtering")
            filters.forEach(element => {
                element.value = ""
            });
            this.$emit('dropFilters')
        }
    }
}
</script>

<style>
    .form-filter{
        margin: 0 70px;
        display: flex;
        justify-content: space-between;
        width: 1000px;
        height: 45px;
        margin-bottom: 50px;
    }
    .thing-title-check-form{
        width: 200px;
    }
    #thing-state-select-form{
        width: 250px;
    }
    #thing-section-select-form{
        width: 250px;
    }
    .drop-filters-button{
        width: 210px;
        align-items: center;
        padding: 4px;
    }
    .tags-filter-block{
        width: 500px;
        z-index: 6;
    }
    .accordion-button{
        border: 1px solid #ced4da;
        width: 400px;
        height: 45px;
    }
    .accordion-tag-title{
        width: 100px;
        border: 1px solid black;
        padding: 0;
        margin: 0;
        margin-bottom: 10px;
        cursor: default;
    }
    .accordion-tag-title:hover{
        transition: all 0.5s ease;
        background:lightgrey;
    }
    .accordion-tag-title:active{
        background: #696969;
    }
    .accordion-body{
        display: flex;
        justify-content: space-between;
        width: 400px;
        flex-flow: wrap;
    }
</style>