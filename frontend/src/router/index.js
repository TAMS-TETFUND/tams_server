import { createWebHistory, createRouter } from "vue-router"

import Home from "@/views/Home.vue"
import Login from "@/views/Login.vue"
import PageNotFound from "@/views/PageNotFound.vue"
import AttendanceDashboard from "@/views/AttendanceDashboard.vue"
import AttendanceByCourse from "@/views/AttendanceByCourse.vue"
import DraggableDemo from "@/views/DraggableDemo.vue"
import store from "../store"
import NProgress from "nprogress"

const routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
    },
    {
        path: "/draggable",
        name: "DraggableDemo",
        component: DraggableDemo,
    },
    {
        path: "/attendance",
        name: "Attendance",
        component: AttendanceDashboard,

        meta: {
            requireLogin: true
        }
    },
    {
        path: "/attendance/by-course",
        name: "AttendanceByCourse",
        component: AttendanceByCourse,

        meta: {
            requireLogin: true
        }
    },
    {
        path: "/login",
        name: "Login",
        component: Login,

        meta: {
            disableIfLoggedIn: true
        }
    },
    {
        path: "/:catchAll(.*)",
        name: "PageNotFound",
        component: PageNotFound,
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeResolve((to, from, next) => {
    if (to.name) {
        NProgress.start()
    }
    next()
})

router.beforeEach((to, from , next) => {
    if(to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated){
        next({name: 'Login', query: {to: to.path} })
    } else {
        next()
    }
})

router.afterEach(() =>{
    NProgress.done()
})
export default router