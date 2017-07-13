<template>
  <v-layout row wrap>
    <HomeStepper 
      ref="HomeStepper"
      v-on:select_routes="HomeStepper_select_routes" 
      v-on:select_time="HomeStepper_select_time" 
      :traffic_data_received="traffic_data_received">
    </HomeStepper>
    <HomeMap 
      ref="HomeMap"
      :center.sync="center" 
      :origin_obj="origin_obj" 
      :destination_obj="destination_obj" 
      :geojson_data="geojson_data">
    </HomeMap>
    <v-flex xs12 class="my-3" v-show="trafficInfoSliderShow">
      <v-card>
        <v-card-row class="green darken-1">
          <v-card-title>
            <span class="white--text">Traffic Info Slider</span>
            <v-spacer></v-spacer>
          </v-card-title>
        </v-card-row>
        <v-card-text>
          <v-card-row>
            This will automatically show the geojson data that has been plotted into the map<br> <br>
          </v-card-row>
          <v-card-row height="auto">
            <div class="historic_slider">
              <vue-slider @callback="displaySelectedHistoric" :real-time="true" ref="historic_slider_ref" v-bind="historic_slider" v-model="historic_slider.value"></vue-slider>
              <br>
              <p>Currently Dsiplayed: {{ historic_slider.value }}</p>
              <p>Avrage Jamming Factor: {{ averageJammingFacotr }}</p>
              <div class="jammingFactorChart">
                <Chart v-if="chartFinished" :data="chartData" :labels="chartLabel" :chartTitle="'Average Jamming Factor at Each Time Period'"></Chart>
              </div>
            </div>
          </v-card-row>
        </v-card-text>
      </v-card>
    </v-flex>


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

import TestData from '../assets/level17.json'
import CaseStudyDirection from '../assets/case_study_newyork_boston.json'
import vueSlider from 'vue-slider-component'
import HistoricBatch from './HistoricBatch'
import HomeMap from './HomeMap.vue'
import { mapState } from 'vuex'

// import custom components
import Chart from './Chart.vue'
import HomeStepper from './HomeStepper.vue'

export default {
  name: 'Home',
  components: {
    vueSlider,
    Chart,
    HistoricBatch,
    HomeStepper,
    HomeMap
  },
  data () {
    return {
      // HomeMap related states
      center: {lat: 33.7601, lng: -84.37429},
      origin_obj: {},
      destination_obj: {},
      geojson_data: {},
      // other
      map_geojson: null,
      traffic_data_received: false,
      route: null,
      directionsDisplay: null,
      directionsService: null,
      location: null,
      testData: TestData,
      geojson_historic_collection: null,
      geojson_historic_collection_indices: {},
      trafficInfoSliderShow: false,
      historic_slider: {
        value: '',
        width: '90%',
        disabled: false,
        tooltip: 'hover',
        piecewise: true,
        data: []   // This will be initialized in the created() funciton
      },
      dateStartPicker: null,
      dateEndPicker: null,
      timeStartPicer: null,
      timeEndPicer: null,
      averageJammingFacotr: null,
      chartLabel: [],
      chartData: [],
      chartFinished: false
    }
  },
  methods: {
    HomeStepper_select_routes(starting_address_obj, destination_obj) {
      let HomeMap = this.$refs.HomeMap
      console.log(starting_address_obj)
      console.log(HomeMap)
      HomeMap.dsiplayRouting(starting_address_obj, destination_obj)
      // pass
    },
    HomeStepper_select_time() {
      // pass
    },
    displaySelectedHistoric(value) {
      let self = this
      console.log(value)
      console.log(self.geojson_historic_collection[self.geojson_historic_collection_indices[value]])
      self.averageJammingFacotr = self.geojson_historic_collection[self.geojson_historic_collection_indices[value]]['averageJammingFacotr']
      this.deleteGeoJsonPlot()
      self.plotGeoJson(self.geojson_historic_collection[self.geojson_historic_collection_indices[value]]['crawled_batch_id_traffic'])
    },
    getMultipleDaysRouteTraffic(dateStartPicker, dateEndPicker, timeStartPicer, timeEndPicer) {
      /* reference
          https://stackoverflow.com/questions/18109481/get-all-the-dates-that-fall-between-two-dates
      */
      let self = this
      self.trafficInfoSliderShow = true
      let dateStartTimeStart = new Date(dateStartPicker + 'T' + timeStartPicer)
      let dateStartTimeEnd = new Date(dateStartPicker + 'T' + timeEndPicer)
      let dateEndTimeStart = new Date(dateEndPicker + 'T' + timeStartPicer)
      let dateBetween = []
      while (dateStartTimeStart <= dateEndTimeStart) {
        dateBetween.push([new Date(dateStartTimeStart), new Date(dateStartTimeEnd)])
        dateStartTimeStart.setDate(dateStartTimeStart.getDate() + 1)
        dateStartTimeEnd.setDate(dateStartTimeEnd.getDate() + 1)
      }
      console.log(JSON.stringify(dateBetween))
      this.$store.state.ws.send(JSON.stringify(['getMultipleDaysRouteTraffic', this.route, dateBetween]))
      this.$store.state.ws.onmessage = function (event) {
        self.geojson_historic_collection = JSON.parse(event.data)
        // initialize local time within geojson_historic_collection
        let local_timestamp
        self.geojson_historic_collection.forEach((item, index) => {
          local_timestamp = new Date(item['crawled_timestamp'])
          // round time. For example: 9:01 will be round to 9:00
          if (local_timestamp.getMinutes() < 30) {
            local_timestamp.setMinutes(0)
            local_timestamp.setSeconds(0)
          }
          else {
            local_timestamp.setMinutes(30)
            local_timestamp.setSeconds(0)
          }
          console.log(local_timestamp)
          item['local_timestamp'] = local_timestamp
          item['averageJammingFacotr'] = self.calculateAverageJammingFactor(item)
        })

        console.log(self.geojson_historic_collection)
        console.log(self.geojson_historic_collection_indices)
        self.historic_slider['data'] = self.geojson_historic_collection.map((item, index) => {
          self.geojson_historic_collection_indices[item.local_timestamp.toLocaleDateString() + ' ' + item.local_timestamp.toLocaleTimeString()] = index
          return item.local_timestamp.toLocaleDateString() + ' ' + item.local_timestamp.toLocaleTimeString()
        })
        self.historic_slider['value'] = self.historic_slider['data'][0]
        let slider = self.$refs['historic_slider_ref']
        slider.refresh()
        self.displaySelectedHistoric(self.historic_slider['value'])
        self.traffic_data_received = true
        setTimeout(() => {
          self.traffic_data_received = false // reset traffic_data_received
        }, 1000)  
        self.displayGeoJson()
        self.calculateAverageJammingFactorForEachTime()
      }
    },
    calculateAverageJammingFactor(geojson_historic_collection_item) {
      let totalGeometryLength = 0
      geojson_historic_collection_item['crawled_batch_id_traffic']['features'].forEach((item) => { 
        totalGeometryLength += item['geometry']['coordinates'].length
      })
      let averageJammingFacotr = 0
      geojson_historic_collection_item['crawled_batch_id_traffic']['features'].forEach((item) => { 
        averageJammingFacotr += (item['geometry']['coordinates'].length / totalGeometryLength) * item['properties']['CF']['JF']
      })
      return averageJammingFacotr
    },
    calculateAverageJammingFactorForEachTime(){
      let self = this
      let eachTimeData = new Map()
      let currentTime
      self.geojson_historic_collection.forEach((item, index) => {
        currentTime = item['local_timestamp'].toLocaleTimeString()
        if (!eachTimeData.get(currentTime)) {
          eachTimeData.set(currentTime, [item['averageJammingFacotr']])
        }
        else {
          eachTimeData.get(currentTime).push(item['averageJammingFacotr'])
        }
      })
      console.log(eachTimeData)
      let total 
      for (let [timePoint, jammingFactorArray] of eachTimeData) {
        self.chartLabel.push(timePoint)
        total = 0
        jammingFactorArray.forEach((JammingFactor) => {
          total += JammingFactor
        })
        self.chartData.push(total / jammingFactorArray.length)
      }
      console.log(self.chartLabel)
      console.log(self.chartData)
      self.chartFinished = true
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

    /* eslint-enable */
  },
  computed: {
    historic_batch() {
      return this.$store.state.historic_batch
    }
  }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style lang="scss" scoped>

.geojson_output {
  width: 100%;
}
  textarea {
    border-style: solid;
  }

.historic_slider {
  width: 100%;
}
</style>
