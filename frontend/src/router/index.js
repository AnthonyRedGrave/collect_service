import { createRouter, createWebHistory } from 'vue-router'
import Things from '@/components/Things.vue'
import ThingDetail from '@/views/ThingDetail.vue'
import ThingMessagesList from '@/views/ThingMessagesList.vue'
import ThingChatsList from '@/views/ThingChatsList.vue'
import OwnerThings from '@/views/OwnerThings.vue'
import Chat from '@/views/Chat.vue'
import Login from '@/views/Login.vue'
import store from '@/store/index.js'


const routes = [{
        path: '/',
        name: 'Things',
        component: Things
    },
    {
        path: '/thing-detail',
        name: 'ThingDetail',
        component: ThingDetail,
        props: true
    },
    {
        path: '/messages/',
        name: 'ThingMessagesList',
        component: ThingMessagesList,
    },
    {
        path: '/chats/',
        name: 'ThingChatsList',
        component: ThingChatsList,
        props: true
    },
    {
        path: '/chat/',
        name: 'Chat',
        component: Chat
    },
    {
        path: '/login/',
        name: 'login',
        component: Login
    },
    {
        path: '/own_things',
        name: 'own_things',
        component: OwnerThings
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresLogin)) {
        if (!store.getters.loggedIn) {
            next({ name: 'login' })
        } else {
            next()
        }
    } else {
        next()
    }
})

export default router