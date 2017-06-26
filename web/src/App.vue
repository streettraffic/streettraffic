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
          <v-list-tile value="true">
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
        <router-view></router-view>
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
        { icon: 'bubble_chart', title: 'Inspire' }
      ],
      miniVariant: false,
      title: 'Histraffic'
    }
  }
}
</script>

<style lang="scss">
  // @import '../../node_modules/vuetify/dist/vuetify.min.css';
</style>
