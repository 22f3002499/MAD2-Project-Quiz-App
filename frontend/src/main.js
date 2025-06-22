import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createBootstrap } from 'bootstrap-vue-next' 

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

import App from './App.vue'
import router from './router'
import apiClient from './plugins/axios'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(createBootstrap())
app.provide("$http" , apiClient)

app.mount('#app')
