<template>
  <v-layout row wrap>
    <RouteLabStepper 
      ref="RouteLabStepper"
      @HomeStepper_select_time="HomeStepper_select_time" 
      :traffic_pattern="traffic_pattern">
    </RouteLabStepper>
    <HomeMap 
      ref="HomeMap"
      :center.sync="center"
      :route.sync="route">
    </HomeMap>
    <RouteLabSlider 
      ref="RouteLabSlider"
      @RouteLabSlider_ChartFinished="RouteLabSlider_ChartFinished"
      :route="route">
    </RouteLabSlider>


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

import CaseStudyDirection from '@/assets/case_study_newyork_boston.json'
import { mapState } from 'vuex'

// import custom components
import RouteLabStepper from './RouteLabStepper'
import RouteLabSlider from './RouteLabSlider'
import HomeMap from '../HomeMap.vue'

export default {
  name: 'RouteLab',
  components: {
    RouteLabStepper,
    HomeMap,
    RouteLabSlider
  },
  data () {
    return {
      // HomeMap related states
      center: {lat: 33.7601, lng: -84.37429},
      route: {},
      current_origin_destination: {},
      current_route: {},
      // References to components
      RouteLabStepper: null,
      HomeMap: null,
      RouteLabSlider: null,
      traffic_pattern: []
    }
  },
  methods: {
    HomeStepper_select_time: async function(dateStartPicker, dateEndPicker, timeStartPicer, timeEndPicer, route_collection) {
      let self = this
      for (let item of route_collection) {
        self.HomeMap.displayRouting(item[0], item[1])
        console.log('displayed', item[0], item[1])
        await self.sleep(1000)  // wait the direction to load 
        self.current_origin_destination = item
        self.current_route = self.route
        await self.RouteLabSlider.getMultipleDaysRouteTraffic(dateStartPicker, dateEndPicker, timeStartPicer, timeEndPicer)
      }
      self.RouteLabStepper.finished_querying_data()
    },
    RouteLabSlider_ChartFinished() {
      this.traffic_pattern.push({
        origin_destination: this.current_origin_destination,
        route: this.current_route,
        chartLabel: this.RouteLabSlider.chartLabel,
        chartData: this.RouteLabSlider.chartData
      })
      console.log(this.traffic_pattern)
    },
    test(){
      /* eslint-disable */
      // this.calculateAverageJammingFactorForEachTime()
      console.log('haha')
      /* eslint-enable */
    },
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    }
  },
  created() {
    // pass
  },
  mounted() {
    /* eslint-disable */
    this.RouteLabStepper = this.$refs.RouteLabStepper
    this.HomeMap = this.$refs.HomeMap
    this.RouteLabSlider = this.$refs.RouteLabSlider
    var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({hello:'test', xixi:'kaka'}));
    console.log(dataStr)
    /* eslint-enable */
  }
}
</script>
