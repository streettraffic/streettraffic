import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/Main'
import Landing from '@/components/Landing'

Vue.use(Router)

function route (path, name, title) {
  return {
    name: name,
    path: path + '/' + name,
    meta: { title: title },
    component: () => import(`@/components/${path}${name}`)
  }
}

const Home = () => ({
  // The component to load. Should be a Promise
  component: import('@/components/Home')
})

const Analytics = () => ({
  // The component to load. Should be a Promise
  component: import('@/components/Analytics')
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
        title: 'Streettraffic Landing'
      }
    },
    {
      path: '/Main',
      component: Main,
      meta: {
        title: 'Streettraffic Main'
      },
      children: [
        route('QuickStart/', 'RegisterRoute', 'Streettraffic Register a Route'),
        route('QuickStart/', 'RunCrawler', 'Streettraffic run the traffic crawler'),
        route('QuickStart/', 'Polygon', 'Streettraffic Register a city'),
        {
          path: '',
          name: 'Home',
          component: Home,
          meta: {
            title: 'Streettraffic Home'
          }
        },
        {
          path: 'Analytics',
          name: 'Analytics',
          component: Analytics,
          meta: {
            title: 'Streettraffic Analytics'
          }
        },
        {
          path: 'RouteLab',
          name: 'RouteLab',
          component: RouteLab,
          meta: {
            title: 'Streettraffic RouteLab'
          }
        },
        {
          path: 'CaseStudy',
          name: 'CaseStudy',
          component: CaseStudy,
          meta: {
            title: 'Streettraffic CaseStudy'
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
