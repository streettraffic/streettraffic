<template lang="pug">
  #intro
    v-layout(column align-center justify-center)
      h2.white--text StreetTraffic Web UI
      h6.white--text Monitor the traffic flow of your favorite routes, cities and more!
      div.mt-5
        v-btn(large tag="a" href="https://github.com/streettraffic/streettraffic").grey.lighten-2 Github
        v-btn(large router :to="'/Main/QuickStart/RegisterRoute'").green.lighten-2 Enter

</template>

<script>
export default {
  name: 'Landing',
  data () {
    return {
      center: {lat: 33.7601, lng: -84.37429}, // {lat: 34.91623, lng: -82.42907}  Furman   {lat: 33.7601, lng: -84.37429} Atlanta
      map_geojson: null,
      dialog: false
    }
  },
  methods: {
    // pass
  },
  created() {
    // pass
  },
  mounted() {
    // pass
  }
}
</script>

<style lang="sass">
#intro
  height: 100vh
  background-color: #303030
  padding-top: 15vh

  .btn
    width: 150px
</style>
