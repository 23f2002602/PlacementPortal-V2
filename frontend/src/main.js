import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App    from './App.vue'
import router from './router/index.js'
import axios  from 'axios'
import '@/assets/main.css'
import "./assets/theme.css"
import "./assets/global.css"

// Attach JWT token to every outgoing request
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('ppa_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

const app = createApp(App)

app.use(createPinia())  // register Pinia store
app.use(router)
app.mount('#app')