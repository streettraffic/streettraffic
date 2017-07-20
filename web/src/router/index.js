import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/Main'
import Landing from '@/components/Landing'

Vue.use(Router)

const Home = () => ({
  // The component to load. Should be a Promise
  component: import('@/components/Home')
})

const Analytics = () => ({
  // The component to load. Should be a Promise
  component: import('@/components/Analytics')
})

const Polygon = () => ({
  // The component to load. Should be a Promise
  component: import('@/components/Polygon')
})

const RouteLab = () => ({
  // The component to load. Should be a Promise
  component: import('@/components/RouteLab')
})

const CaseStudy = () => ({
  // The component to load. Should be a Promise
  component: import('@/components/CaseStudy')
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
          path: 'RouteLab',
          name: 'RouteLab',
          component: RouteLab,
          meta: {
            title: 'Histraffic RouteLab'
          }
        },
        {
          path: 'Polygon',
          name: 'Polygon',
          component: Polygon,
          meta: {
            title: 'Histraffic Polygon'
          }
        },
        {
          path: 'CaseStudy',
          name: 'CaseStudy',
          component: CaseStudy,
          meta: {
            title: 'Histraffic CaseStudy'
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
