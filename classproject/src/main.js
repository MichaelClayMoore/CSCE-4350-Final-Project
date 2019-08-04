import Vue from 'vue'
import './plugins/vuetify'
import Vuex from 'vuex'
import App from './App.vue'
import router from './router'
import store from './store'
import "vue-material-design-icons/styles.css"
import FlashMessage from '@smartweb/vue-flash-message';

Vue.config.productionTip = false
Vue.use(FlashMessage);
Vue.use(Vuex)

new Vue({
  render: h => h(App),
  router,
  store
}).$mount('#app')
