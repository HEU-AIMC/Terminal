import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import Terminal from 'vue-web-terminal'
//  亮色主题：vue-web-terminal/lib/theme/light.css
import 'vue-web-terminal/lib/theme/dark.css'
// createApp(App)
// app.use(hljsVuePlugin)
createApp(App).use(Terminal).mount('#app')
