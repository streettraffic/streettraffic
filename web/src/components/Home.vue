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


<!--     <v-flex xs12>
      <v-divider class="my-4"></v-divider>
      <section>
        <v-btn dark default @click.native="plotGeoJson(testData)">plot GeoJson(testData)</v-btn>
        <v-btn dark default @click.native="displayGeoJson">display GeoJson</v-btn>
        <v-btn dark default @click.native="getHistoric">get Historic</v-btn>
        <v-btn dark default @click.native="toManhattan">to Manhattan</v-btn>
        <v-btn dark default @click.native="test">test</v-btn>
        <v-btn dark default @click.native="loadControls">Load Drawing Tools</v-btn>
      </section>
      

      <v-divider class="my-4"></v-divider>


      <h6>Select your desired historic traffic:</h6>
      <HistoricBatch></HistoricBatch>
    </v-flex> -->
  </v-layout>
</template>

<script>
// To see how we use geojson in google maps, check out
// https://github.com/xkjyeah/vue-google-maps/issues/90 about how we use
// To see how we use the Direction api, refer to
// https://developers.google.com/maps/documentation/javascript/examples/directions-travel-modes

import CaseStudyDirection from '../assets/case_study_newyork_boston.json'
import { mapState } from 'vuex'

// import custom components
import HomeStepper from './HomeStepper.vue'
import HomeSlider from './HomeSlider'
import HistoricBatch from './HistoricBatch'
import HomeMap from './HomeMap.vue'

export default {
  name: 'Home',
  components: {
    HistoricBatch,
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
      // this.calculateAverageJammingFactorForEachTime()
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
  },
  computed: {
    historic_batch() {
      return this.$store.state.historic_batch
    }
  }
}
</script>
