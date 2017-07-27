<template>
  <v-layout row wrap>
    <HomeStepper 
      ref="HomeStepper"
      @HomeStepper_select_routes="HomeStepper_select_routes" 
      @HomeStepper_select_time="HomeStepper_select_time" >
    </HomeStepper>
    <HomeMap 
      ref="HomeMap"
      :center.sync="center"
      :route.sync="route">
    </HomeMap>
    <HomeSlider 
      ref="HomeSlider"
      :route="route"
      @HomeSlider_plotGeoJson="HomeSlider_plotGeoJson"
      @HomeSlider_deleteGeoJsonPlot="HomeSlider_deleteGeoJsonPlot"
      @HomeSlider_displayGeoJson="HomeSlider_displayGeoJson"
      @HomeSlider_finishedQueryingData="HomeSlider_finishedQueryingData">
    </HomeSlider>
  </v-layout>
</template>

<script>
// To see how we use geojson in google maps, check out
// https://github.com/xkjyeah/vue-google-maps/issues/90 about how we use
// To see how we use the Direction api, refer to
// https://developers.google.com/maps/documentation/javascript/examples/directions-travel-modes
import HomeStepper from './FlowQueryStepper'
import HomeSlider from '../HomeSlider'
import HomeMap from '../HomeMap.vue'

export default {
  name: 'FlowQuery',
  components: {
    HomeStepper,
    HomeMap,
    HomeSlider
  },
  data () {
    return {
      // HomeMap related states
      center: {lat: 33.7601, lng: -84.37429},
      route: {},
      // References to components
      HomeStepper: null,
      HomeMap: null,
      HomeSlider: null
    }
  },
  methods: {
    HomeStepper_select_routes(starting_address_obj, destination_obj) {
      console.log(this)
      this.HomeMap.displayRouting(starting_address_obj, destination_obj)
      // pass
    },
    HomeStepper_select_time(dateStartPicker, dateEndPicker, timeStartPicer, timeEndPicer) {
      this.HomeSlider.getMultipleDaysRouteTraffic(dateStartPicker, dateEndPicker, timeStartPicer, timeEndPicer)
    },
    HomeSlider_requestingRoutes() {
      this.HomeSlider
    },
    HomeSlider_plotGeoJson(geojson) {
      this.HomeMap.plotGeoJson(geojson)
    },
    HomeSlider_deleteGeoJsonPlot() {
      this.HomeMap.deleteGeoJsonPlot()
    },
    HomeSlider_displayGeoJson() {
      this.HomeMap.displayGeoJson()
    },
    HomeSlider_finishedQueryingData() {
      this.HomeStepper.finished_querying_data()
    },
    test(){
      /* eslint-disable */
      console.log('haha')
      /* eslint-enable */
    }
  },
  created() {
    // pass
  },
  mounted() {
    /* eslint-disable */
    this.HomeStepper = this.$refs.HomeStepper
    this.HomeMap = this.$refs.HomeMap
    this.HomeSlider = this.$refs.HomeSlider
    /* eslint-enable */
  }
}
</script>
