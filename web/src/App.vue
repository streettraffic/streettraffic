<template>
  <v-app>
    <v-navigation-drawer
      persistent
      v-model="drawer"
    >
      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
        >
          <v-list-tile value="true" router :to="item.routerAddress">
            <v-list-tile-action>
              <v-icon light v-html="item.icon"></v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title v-text="item.title"></v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar light>
      <v-toolbar-side-icon @click.native.stop="drawer = !drawer" light></v-toolbar-side-icon>
      <v-toolbar-title v-text="title" ></v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <main>
      <v-container fluid>
        <transition name="slide" mode="out-in">
          <router-view></router-view>
        </transition>
      </v-container>
    </main>
    <v-footer>
      <span>&copy; 2017</span>
    </v-footer>
  </v-app>
</template>

<script>

export default {
  data () {
    return {
      drawer: true,
      items: [
        { icon: 'home', title: 'Home', routerAddress: '/' },
        { icon: 'insert_chart', title: 'Analytics', routerAddress: '/Analytics' }
      ],
      miniVariant: false,
      title: 'Histraffic'
    }
  },
  created() {
    // test
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
