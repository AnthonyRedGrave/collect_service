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
        <select id="thing-state-select-form" class="form-select" aria-label="Default select example">
            <option value="Awesome">Лучшее</option>
            <option value="Good">Хорошее</option>
            <option value="Shabby">Потрепанное</option>
            <option value="Bad">Плохое</option>
        </select>
        <select id="thing-section-select-form" class="form-select" aria-label="Default select example">
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
    name: "filter-form"
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