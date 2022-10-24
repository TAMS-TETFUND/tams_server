import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
axios.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem('token')
const app = createApp(App)
.use(router)
.use(store)

app.config.globalProperties.axios = axios

app.mount('#app')
