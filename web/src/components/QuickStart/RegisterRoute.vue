<template lang="pug">
  v-layout(row wrap)
    HomeStepper(
      ref="HomeStepper"
      @HomeStepper_select_routes="HomeStepper_select_routes" 
      @HomeStepper_select_time="HomeStepper_select_time"
    )
    HomeMap(
      ref="HomeMap"
      :center.sync="center"
      :route.sync="route"
    )
</template>

<script>
// import custom components
import HomeStepper from '../HomeStepper.vue'
import HomeMap from '../HomeMap.vue'

export default {
  name: 'Home',
  components: {
    HomeStepper,
    HomeMap
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
