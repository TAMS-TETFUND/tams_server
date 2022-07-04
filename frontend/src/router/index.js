import { createWebHistory, createRouter } from "vue-router"

import Home from "@/views/Home.vue"
import Login from "@/views/Login.vue"

import store from "../store"

const routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
    },
    {
        path: "/login",
        name: "Login",
        component: Login,

        meta: {
            disableIfLoggedIn: true
        }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach((to, from , next) => {
    if(to.matched.some(record => record.meta.requiredLogin) && !StorageEvent.state.isAuthenticated){
        next({name: 'Login', query: {to: to.path} })
    } else {
        next()
    }
})
export default router