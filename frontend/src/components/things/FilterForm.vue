<template>
  <div class="filter-form">
      <form class="form-filter" action="">
        <div class="thing-title-check-form">
            <div class="form-check">
                <input class="form-check-input ordering" type="radio" name="flexRadioDefault" id="flexRadioOrderingTitle1" @click="orderingThingsTitle('title')">
                <label class="form-check-label" for="flexRadioOrderingTitle1">
                    От А до Я
                </label>
            </div>
            <div class="form-check">
            <input class="form-check-input ordering" type="radio" name="flexRadioDefault" id="flexRadioOrderingTitle2" @click="orderingThingsTitle('-title')">
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
                    Accordion Item #1
                </button>
                </h2>
                <div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" data-bs-parent="#accordionFlushExample">
                <div class="accordion-body"><code v-for="tag in tags" :key="tag.id"></code></div>
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
            filters: [],
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
        filteringThings(value){
            let url = this.getCorrectUrl(value);
            axios
                .get(url, {
                headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
                })
                .then((response) => {
                    this.$emit('filteringThings', response.data)
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
            this.getCorrectUrl(filter)
            let state = this.getFieldValue('state')
            let section = this.getFieldValue('section')
            axios
                .get(`http://0.0.0.0:8000/api/things/`, {
                headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
                params: {
                    state:state, 
                    section: section, 
                    order_by: this.ordering},
                })
                .then((response) => {
                    this.$emit('filteringThings', response.data)
                })
                .catch((err) => {
                    console.log(err);
                });
        },
        getFieldValue(name){
            if (this.filters.some(item => item.filtername === name)){
                return this.filters.find(element => element.filtername === name).value
            }
            else{
                return null
            }
        },
        getCorrectUrl(filter){
            let filterkeys = this.filters.map(function (el) {return el.filtername})
            if (this.filters.length < 2 && !filterkeys.includes(filter.filtername)){
                this.filters.push(filter)
            }
            this.filters.forEach(element => {
            if (element.filtername == filter.filtername){
                element.value = filter.value
            }
            });

        },
        orderingThingsTitle(ordering){
            this.ordering = ordering
            axios
                .get(`http://0.0.0.0:8000/api/things/`, {
                headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
                params: {
                    order_by: ordering,
                    state: this.getFieldValue('state'),
                    section: this.getFieldValue('section')
                    },
                })
                .then((response) => {
                    this.$emit('filteringThings', response.data)
                })
                .catch((err) => {
                    console.log(err);
                });
        },
        dropFilters(){
            this.filters = []
            this.ordering = null
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
        width: 800px;
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
</style>