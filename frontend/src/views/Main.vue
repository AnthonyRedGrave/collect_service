<template>
    <nav-bar/>
    <router-view/>
</template>

<script>
import NavBar from '../components/NavBar.vue'
export default {
    name: 'main',
    components: { NavBar },
    created() {
        this.getSectionChoices() // получение всех разделов
        this.getThingTags() // получение всех тегов
    },
    methods:{
        getSectionChoices(){
        this.$store
            .dispatch("thingSectionChoices", {
            token: this.$store.state.accessToken,
            })
            .then(() => {})
            .catch((err) => {
            console.log(err);
            });
    },
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
    }
}
</script>

<style>

</style>