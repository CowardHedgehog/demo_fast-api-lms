/**
 * plugins/index.ts
 *
 * Automatically included in `./src/main.ts`
 */

// Plugins
import vuetify from '@/plugins/vuetify'
import store from '@/plugins/store'
import router from '@/router'
import VueCookies from 'vue-cookies'

// Types
import type { App } from 'vue'

export function registerPlugins (app: App) {
  app.use(vuetify)
  app.use(store)
  app.use(router)
  app.use(VueCookies)
}
