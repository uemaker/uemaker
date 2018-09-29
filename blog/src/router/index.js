import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/modules/home/Index'
import ArticleDetail from '@/modules/article/Detail'

Vue.use(Router)
export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/article/:id',
      name: 'ArticleDetail',
      component: ArticleDetail
    }
  ]
})
