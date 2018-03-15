<template lang="pug">
  v-app
    
    v-toolbar(light)
      v-toolbar-title(v-text="title")
      v-spacer


    main
      v-container(fluid)
        transition(name="slide" mode="out-in")
          router-view


    v-footer
      span &copy; 2017
</template>

<script>
export default {
  name: 'Main',
  data () {
    return {
      drawer: true,
      mini: false,
      items: [
        { header: 'Welcome to StreetTraffic Web UI' },
        {
          title: 'Quick Start',
          action: 'apps',
          group: 'QuickStart',
          items: [
            { href: '/Main/QuickStart/RegisterRoute', title: 'Register a route' },
            { href: '/Main/QuickStart/Polygon', title: 'Register an area' },
            { href: '/Main/QuickStart/RunCrawler', title: 'Run the crawler' }
          ]
        },
        {
          title: 'Query',
          action: 'devices',
          group: 'Query',
          items: [
            { href: '/Main/Query/FlowQuery', title: 'Traffic flow Query' },
            { href: '/Main/Query/HistoryBatch', title: 'Historical Batch' }
          ]
        },
        {
          title: 'Analytics',
          action: 'insert_chart',
          group: 'Analytics',
          items: [
            { href: '/Main/Analytics/TrafficPattern', title: 'Traffic Pattern' }
          ]
        },
        {
          title: 'Research',
          action: 'build',
          group: 'Research',
          items: [
            { href: '/Main/Research/RouteLab', title: 'Route Lab' },
            { href: '/Main/Research/CaseStudy', title: 'Case Study' }
          ]
        },
        { action: 'home', title: 'Home', href: '/#/Main' }
      ],
      items2: [
        {
          icon: 'home',
          title: 'Vuetify',
          action: 'apps',
          group: 'vuetify',
          routerAddress: '/Main'
          // children: [
          //   { href: '/vuetify/quick-start', title: 'Quick start' },
          //   { href: '/vuetify/sandbox', title: 'Sandbox' },
          //   { href: '/vuetify/frequently-asked-questions', title: 'Frequently asked questions' },
          //   { href: '/vuetify/sponsors-and-backers', title: 'Sponsors and backers' }
          // ]
        },
        { icon: 'home', title: 'Home', routerAddress: '/Main' },
        { icon: 'insert_chart', title: 'Analytics', routerAddress: '/Main/Analytics' },
        { icon: 'create', title: 'Polygon', routerAddress: '/Main/Polygon' },
        { icon: 'build', title: 'RouteLab', routerAddress: '/Main/RouteLab' },
        { icon: 'build', title: 'CaseStudy', routerAddress: '/Main/CaseStudy' }
      ],
      miniVariant: false,
      title: 'StreetTraffic Demo'
    }
  },
  mounted() {
    // pass
  }
}
</script>

<style lang="scss">
.slide-enter-active, .slide-enter {
  transition: all .3s ease
}
  
.slide-enter, .slide-leave-to{
  opacity: 0
}
  
.slide-enter{
  transform: translateX(-3rem)
}
  
.slide-leave, .slide-leave-active{
  transition: all .4s ease
}
  
.slide-leave-to{
  transform: translateX(3rem)
}

</style>
