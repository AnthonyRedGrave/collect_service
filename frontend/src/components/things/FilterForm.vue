<template>
  <div class="filter-form">
      <form class="form-filter" action="">
        <div class="thing-title-check-form">
            <div class="form-check">
                <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1">
                <label class="form-check-label" for="flexRadioDefault1">
                    От А до Я
                </label>
            </div>
            <div class="form-check">
            <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault2" checked>
            <label class="form-check-label" for="flexRadioDefault2">
                От Я до А
            </label>
            </div>
        </div>
        <select id="thing-state-select-form" class="form-select" @change="filteringThings(filterState)" v-model="filterState" aria-label="Default select example">
            <option v-for="state in this.state_list" :key="state.id" v-bind:value=state.value>{{state.label}}</option>
        </select>
        <select id="thing-section-select-form" class="form-select" @change="filteringThings(filterSection)" v-model="filterSection" aria-label="Default select example">
            <option v-for="section in this.$store.state.section_choices" :key="section.id" v-bind:value=section.id>{{section.title}}</option>
        </select>
        <div class="search-button">
            <button type="button" class="btn btn-success">Искать</button>
        </div>
      </form>
  </div>
</template>

<script>
export default {
    name: "filter-form",
    data() {
        return {
            filterState: "",
            filterSection: "",
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
    methods:{
        filteringThings(value){
            console.log(value)
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
</style>