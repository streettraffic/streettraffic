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
      component: Main,
      meta: {
        title: 'Streettraffic Main'
      },
      children: [
        {
          name: 'demo',
          path: '/',
          meta: { title: 'Streettraffic Demo' },
          component: () => import(`@/components/Query/FlowQuery`)
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
