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
        route('Query/', 'FlowQuery', 'Streettraffic traffic flow query'),
        route('Query/', 'HistoryBatch', 'Streettraffic traffic flow query'),
        route('Analytics/', 'TrafficPattern', 'Streettraffic traffic pattern analytics'),
        route('Research/', 'RouteLab', 'Streettraffic Multiple Routes Analysis'),
        route('Research/', 'CaseStudy', 'Streettraffic Long Distance Route Study')
      ]
    }
  ]
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title
  next()
})

export default router
