import { createRouter, createWebHistory } from 'vue-router'
import Things from '@/components/Things.vue'
import ThingDetail from '@/views/ThingDetail.vue'

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
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router