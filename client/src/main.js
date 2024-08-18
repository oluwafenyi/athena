import './assets/main.css'
import 'vue-loading-overlay/dist/css/index.css'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)

const toastOptions = {
  position: 'top-right',
  timeout: 2000,
  closeOnClick: true
}

app.use(Toast, toastOptions)

app.mount('#app')
