/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'
import VueUploadComponent from 'vue-upload-component'
//import { VueLoading } from 'vue-loading-template'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'


const app = createApp(App)
app.component('file-upload', VueUploadComponent)
//app.component('vue-loading', VueLoading)
registerPlugins(app)

app.mount('#app')
