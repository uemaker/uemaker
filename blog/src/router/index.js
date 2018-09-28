import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/modules/home/Index'
import HeaderView from '@/components/v-header'
Vue.component('v-header', HeaderView)

Vue.use(Router)
export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    }
  ]
})
