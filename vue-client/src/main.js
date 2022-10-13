
import Backend from './services/backend'
import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import router from './router'



const app = createApp(App)

app.use(router)
app.config.globalProperties.axios = axios
app.config.globalProperties.$backend = new Backend();

app.mount('#app')
