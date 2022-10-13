import {createRouter,createWebHistory} from 'vue-router'

import InputPage from './components/InputPage.vue'
import MainPage from './components/MainPage.vue'
import GraphView from './components/GraphView.vue'
import FilterView from './components/FilterView.vue'

const routes = [
    {
        path: '/',
        component: InputPage,
        name: 'InputPage'
    },

    {
        path: '/app',
        component: MainPage,
        name: 'App',
        children: [
            {
                path: 'graph',
                component: GraphView,
                name: 'GraphView'
            },
        
            {
                path: 'filter',
                component: FilterView,
                name: 'FilterView'
            }
        ]
    }
]

const router = createRouter({

    history: createWebHistory(),
    routes
}
)

export default router