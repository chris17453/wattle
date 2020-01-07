//import router from './router.js'
import App from '/view/App.vue'

Vue.config.productionTip = false

new Vue({
//  router,
  render: h => h(App)
}).$mount('#app')
