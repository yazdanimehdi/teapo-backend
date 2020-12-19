import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import vuetify from './plugins/vuetify';
import axios from 'axios';

Vue.config.productionTip = false
const token = localStorage.getItem('user-token');

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

if (token) {
  axios.defaults.headers.common['Authorization'] = `Token ${token}`
}

new Vue({
  store,
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
