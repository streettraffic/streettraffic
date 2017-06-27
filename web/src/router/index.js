import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'

Vue.use(Router)

const Analytics = () => ({
  // The component to load. Should be a Promise
  component: import('@/components/Analytics')
})

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/analytics',
      name: 'Analytics',
      component: Analytics
    }
  ]
})
