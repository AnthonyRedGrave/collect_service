import { createStore } from 'vuex'
import axios from 'axios'

const store = createStore({
    state: {
        accessToken: JSON.parse(localStorage.getItem('token')),
        refreshToken: null,
        username: JSON.parse(localStorage.getItem('username')),
        things: [],
        messages: [],
        chats: [],
        tags: JSON.parse(localStorage.getItem('tags')),
        section_choices: JSON.parse(localStorage.getItem('sections'))
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
        updateMessages(state, { messages }) {
            state.messages = messages
        },
        updateChats(state, { chats }) {
            state.chats = chats
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
                        localStorage.setItem("sections", JSON.stringify(responce.data))
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
                        localStorage.setItem("tags", JSON.stringify(responce.data))
                        resolve(responce)
                    })
                    .catch(err => {
                        console.log(err)
                        reject(err)
                    })
            })
        },
        getMessagesList(context, access) {
            return new Promise((resolve, reject) => {
                axios({
                        method: 'get',
                        url: 'http://0.0.0.0:8000/api/thing_messages/user_messages/',
                        headers: { Authorization: `Bearer ${access.token}` },
                        credentials: 'include',
                    }).then((responce) => {
                        context.commit('updateMessages', { messages: responce.data })
                        resolve(responce)
                    })
                    .catch(err => {
                        console.log(err)
                        reject(err)
                    })
            })
        },
        getChatsList(context, access) {
            return new Promise((resolve, reject) => {
                axios({
                        method: 'get',
                        url: 'http://0.0.0.0:8000/api/chats/',
                        headers: { Authorization: `Bearer ${access.token}` },
                        credentials: 'include',
                    }).then((responce) => {
                        context.commit('updateChats', { chats: responce.data })
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