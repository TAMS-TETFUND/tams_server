import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
axios.defaults.baseURL = "http://localhost:8009"
axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')

createApp(App)
.use(router)
.use(store)
.mount('#app')
