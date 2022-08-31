import { createWebHistory, createRouter } from "vue-router"

import Home from "@/views/Home.vue"
import Login from "@/views/Login.vue"
import PageNotFound from "@/views/PageNotFound.vue"
import AttendanceDashboard from "@/views/attendance/AttendanceDashboard.vue"
import AttendanceByCourse from "@/views/attendance/AttendanceByCourse.vue"
import AttendanceByCourseDetails from "@/views/attendance/AttendanceByCourseDetails.vue"
import StudentAttendanceReport from "@/views/attendance/StudentAttendanceReport.vue"
import StudentReportSearch from "@/views/attendance/StudentReportSearch.vue"
import DraggableDemo from "@/views/DraggableDemo.vue"
import Contact from "@/views/Contact.vue"
import ProductDetail from "@/views/ProductDetail.vue"
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
        name: "Draggable Demo",
        component: DraggableDemo,
    },
    {
        path: "/product-details",
        name: "Product Details",
        component: ProductDetail,
    },
    {
        path: "/contact",
        name: "Contact Us",
        component: Contact,
    },
    {
        path: "/attendance/download",
        name: "Attendance",
        component: AttendanceDashboard,

        meta: {
            requireLogin: true
        }
    },
    {
        path: "/attendance/by-course",
        name: "Attendance By Course",
        component: AttendanceByCourse,

        meta: {
            requireLogin: true
        }
    },
    {
        path: "/attendance/by-course/detail/:session/:course",
        name: "Attendance By Course Details",
        component: AttendanceByCourseDetails,

        meta: {
            requireLogin: true
        }
    },
    {
        path: "/attendance/student-report/",
        name: "Student Report Search",
        component: StudentReportSearch,

        meta: {
            requireLogin: true
        }
    },
    {
        path: "/attendance/student-report/:id(.*)",
        name: "Student Attendance Report",
        component: StudentAttendanceReport,

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
        name: "Page Not Found",
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