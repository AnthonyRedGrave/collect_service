import { createRouter, createWebHistory } from 'vue-router'
import Things from '@/components/Things.vue'
import ThingDetail from '@/views/ThingDetail.vue'
import ThingMessagesList from '@/views/ThingMessagesList.vue'
import ThingChatsList from '@/views/ThingChatsList.vue'
import Chat from '@/views/Chat.vue'


const routes = [{
        path: '/',
        name: 'Things',
        component: Things
    },
    {
        path: '/thing-detail/',
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
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router