import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import router from './router'

axios.defaults.baseURL = 'http://localhost:8000'
const app = createApp(App)
app.use(router, axios)
app.mount('#app')
