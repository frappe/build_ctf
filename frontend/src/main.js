
import { createApp } from 'vue'
import router from './router'
import App from './App.vue'
import { FrappeUI, Button, frappeRequest, setConfig } from 'frappe-ui'

import './index.css'


const app = createApp(App)
app.use(router)
setConfig('resourceFetcher', frappeRequest)
app.use(FrappeUI, { socketio: false })
app.component("Button", Button)
app.mount('#app')
