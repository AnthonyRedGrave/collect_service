import { createStore } from 'vuex'
import axios from 'axios'

const store = createStore({
    state: {
        accessToken: JSON.parse(localStorage.getItem('token')),
        refreshToken: null,
        username: JSON.parse(localStorage.getItem('username')),
        things: [],
        tags: [],
        section_choices: []
    },
    mutations: {
        updateAuthCredentials(state, { access, refresh, username }) {
            state.accessToken = access
            state.refreshToken = refresh
            state.username = username
        },
        updateSectionFilterChoices(state, { section_choices }) {
            state.section_choices = section_choices
        },
        updateThings(state, { things }) {
            state.things = things
        },
        updateTags(state, { tags }) {
            state.tags = tags
        },
        destroyToken(state) {
            state.accessToken = null
            state.refreshToken = null
            state.username = null
            localStorage.removeItem('token')
            localStorage.removeItem('username')
        }
    },
    getters: {
        loggedIn(state) {
            return state.accessToken != null
        }
    },
    actions: {
        userLogin(context, usercredential) {
            return new Promise((resolve, reject) => {
                axios({
                        method: 'post',
                        url: 'http://localhost:8000/api/token/',
                        data: {
                            username: usercredential.username,
                            password: usercredential.password
                        },
                        credentials: 'include',
                    }).then((responce) => {
                        context.commit('updateAuthCredentials', { access: responce.data.access, refresh: responce.data.refresh, username: usercredential.username })
                        localStorage.setItem('token', JSON.stringify(responce.data.access))
                        localStorage.setItem('username', JSON.stringify(usercredential.username))

                        resolve(responce)
                    })
                    .catch(err => {
                        console.log(err)
                        reject(err)
                    })
            })

        },
        userLogout(context) {
            if (context.getters.loggedIn) {
                context.commit('destroyToken')
            }
        },
        thingSectionChoices(context, access) {
            return new Promise((resolve, reject) => {
                axios({
                        method: 'get',
                        url: 'http://localhost:8000/api/sections/',
                        headers: { Authorization: `Bearer ${access.token}` },
                        credentials: 'include',
                    }).then((responce) => {
                        context.commit('updateSectionFilterChoices', { section_choices: responce.data })
                        resolve(responce)
                    })
                    .catch(err => {
                        console.log(err)
                        reject(err)
                    })
            })
        },
        getThingList(context, access) {
            return new Promise((resolve, reject) => {
                axios({
                        method: 'get',
                        url: 'http://localhost:8000/api/things/',
                        headers: { Authorization: `Bearer ${access.token}` },
                        credentials: 'include',
                    }).then((responce) => {
                        context.commit('updateThings', { things: responce.data })
                        resolve(responce)
                    })
                    .catch(err => {
                        console.log(err)
                        reject(err)
                    })
            })
        },
        getThingTagsList(context, access) {
            return new Promise((resolve, reject) => {
                axios({
                        method: 'get',
                        url: 'http://localhost:8000/api/tags/',
                        headers: { Authorization: `Bearer ${access.token}` },
                        credentials: 'include',
                    }).then((responce) => {
                        context.commit('updateTags', { tags: responce.data })
                        resolve(responce)
                    })
                    .catch(err => {
                        console.log(err)
                        reject(err)
                    })
            })
        },

    },
    modules: {}
})

export default store;