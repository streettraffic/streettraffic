import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const Home = () => ({
  // The component to load. Should be a Promise
  component: import('@/components/Home')
})

const Landing = () => ({
  // The component to load. Should be a Promise
  component: import('@/components/Landing')
})

const Main = () => ({
  // The component to load. Should be a Promise
  component: import('@/components/Main')
})

const Analytics = () => ({
  // The component to load. Should be a Promise
  component: import('@/components/Analytics')
})

const Polygon = () => ({
  // The component to load. Should be a Promise
  component: import('@/components/Polygon')
})

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Landing',
      component: Landing,
      meta: {
        title: 'Histraffic Landing'
      }
    },
    {
      path: '/Main',
      component: Main,
      meta: {
        title: 'Histraffic Main'
      },
      children: [
        {
          path: '',
          name: 'Home',
          component: Home,
          meta: {
            title: 'Histraffic Home'
          }
        },
        {
          path: 'Analytics',
          name: 'Analytics',
          component: Analytics,
          meta: {
            title: 'Histraffic Analytics'
          }
        },
        {
          path: 'Polygon',
          name: 'Polygon',
          component: Polygon,
          meta: {
            title: 'Histraffic Polygon'
          }
        }
      ]
    }
  ]
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title
  next()
})

export default router
