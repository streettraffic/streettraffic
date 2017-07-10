<template>
  <v-layout row wrap>
    <v-flex xs12 md6 class="my-3">
      <v-card>
        <v-card-row class="green darken-1">
          <v-card-title>
            <span class="white--text">The Map</span>
            <v-spacer></v-spacer>
          </v-card-title>
        </v-card-row>
        <v-card-text>
          <v-card-row>
            Randomly click on the map is going to show the traffic of a nearest road <br><br>
          </v-card-row>
          <v-card-row height="auto" center>
            <gmap-map ref = "mymap" :center="center" :zoom="14" style="width: 100%; height: 400px" 
                @click="location = {lat: $event.latLng.lat(), lng:$event.latLng.lng()}; getLocation()">
              <gmap-marker v-if="location" :position="location" /></gmap-marker>
            </gmap-map>
          </v-card-row>
        </v-card-text>
      </v-card>
    </v-flex>
    <v-flex xs12 md6 class="my-3">
      <v-card>
        <v-card-row class="green darken-1">
          <v-card-title>
            <span class="white--text">Geojson</span>
            <v-spacer></v-spacer>
          </v-card-title>
        </v-card-row>
        <v-card-text>
          <v-card-row>
            This will automatically show the geojson data that has been plotted into the map<br> <br>
          </v-card-row>
          <v-card-row height="auto" center>
            <div class="geojson_output">
              <textarea style="width: 100%; height: 390px" v-model="map_geojson"></textarea>
            </div>
          </v-card-row>
        </v-card-text>
      </v-card>
    </v-flex>
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
    <v-flex xs12 class="my-3">
      <v-card>
        <v-card-row class="green darken-1">
          <v-card-title>
            <span class="white--text">Route Traffic on a Given Day</span>
            <v-spacer></v-spacer>
          </v-card-title>
        </v-card-row>
        <v-card-text>
          Display routing. Then pick a date, start time, and end time
        </v-card-text>
        <v-card-text>
          <v-btn dark default @click.native="dsiplayRouting">dsiplay Routing</v-btn>
          <v-btn dark default @click.native="dsiplayRoutingCaseStudy">dsiplay Routing Case Study</v-btn>
          <v-layout row wrap>
            <v-flex xs12 md4 class="my-3">
              <h6>Pick a start date</h6>
              <v-date-picker v-model="dateStartPicker"></v-date-picker>
            </v-flex>
            <v-flex xs12 md4 class="my-3">
              <h6>Pick an end date</h6>
              <v-date-picker v-model="dateEndPicker"></v-date-picker>
            </v-flex>

            <v-flex xs12 md4 class="my-3">
              <h6>Pick a start time</h6>
              <v-time-picker v-model="timeStartPicer" format="24hr"></v-time-picker>
            </v-flex>

            <v-flex xs12 md4 class="my-3">
              <h6>Pick an end time</h6>
              <v-time-picker v-model="timeEndPicer" format="24hr"></v-time-picker>
            </v-flex>
          </v-layout>
          <v-dialog v-model="trafficInfoSliderDialog" persistent>
            <v-btn primary light slot="activator" @click.native="getMultipleDaysRouteTraffic">Open Dialog</v-btn>
            <v-card>
              <v-card-row>
                <v-card-title>Retrieving data from the server</v-card-title>
              </v-card-row>
              <v-card-row>
                <v-card-text>Please be patient :)</v-card-text>
              </v-card-row>
            </v-card>
          </v-dialog>
        </v-card-text>
      </v-card>
    </v-flex>



    <v-flex xs12>
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
      <v-data-table
        v-bind:headers="headers"
        v-bind:items="historic_batch"
        v-model="selected"
        selected-key="crawled_batch_id"
        select-all
      >
        <template slot="headers" scope="props">
          <span v-tooltip:bottom="{ 'html': props.item.text }">
            {{ props.item.text }}
          </span>
        </template>
        <template slot="items" scope="props">
          <td>
            <v-checkbox
              primary
              hide-details
              v-model="props.selected"
            ></v-checkbox>
          </td>
          <td>{{ props.item.crawled_batch_id }}</td>
          <td  class="text-xs-right">{{ props.item.crawled_timestamp }}</td>
        </template>
      </v-data-table>
      <v-btn dark default @click.native="getSelectedBatchList">Submit</v-btn>
    </v-flex>
  </v-layout>
</template>

<script>
// To see how we use geojson in google maps, check out
// https://github.com/xkjyeah/vue-google-maps/issues/90 about how we use
// To see how we use the Direction api, refer to
// https://developers.google.com/maps/documentation/javascript/examples/directions-travel-modes

import * as VueGoogleMaps from 'vue2-google-maps'
import Vue from 'vue'
import TestData from '../assets/level17.json'
import CaseStudyDirection from '../assets/case_study_newyork_boston.json'
import vueSlider from './vue2-slider'
import { mapState } from 'vuex'
import Chart from './Chart.vue'

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyAucd0sk7vH1NjQyh3b2kN8qYKhdu4S1Ss'
    // libraries: 'places', //// If you need to use place input
  }
})

export default {
  name: 'Home',
  components: {
    vueSlider,
    Chart
  },
  data () {
    return {
      center: {lat: 33.7601, lng: -84.37429}, // {lat: 34.91623, lng: -82.42907}  Furman   {lat: 33.7601, lng: -84.37429} Atlanta
      map_geojson: null,
      trafficInfoSliderDialog: false,
      route: null,
      directionsDisplay: null,
      directionsService: null,
      location: null,
      testData: TestData,
      geojson_data: null,   // maybe not needed
      geojson_historic_collection: null,
      geojson_historic_collection_indices: {},
      selected: [],
      trafficInfoSliderShow: false,
      headers: [
        {
          text: 'crawled_batch_id',
          left: true,
          sortable: false,
          value: 'name'
        },
        { text: 'crawled_timestamp', sortable: false, value: 'calories' }
      ],
      historic_slider: {
        value: '',
        width: '90%',
        disabled: false,
        tooltip: 'hover',
        piecewise: true,
        data: [
          '2016-10-01',
          '2016-10-02',
          '2016-10-03'
        ]   // This will be initialized in the created() funciton
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
    getLocation() {
      let self = this
      this.$store.state.ws.send(JSON.stringify(['getRoadData', this.location, 10000, 10]))
      this.$store.state.ws.onmessage = function (event) {
        self.plotGeoJson(JSON.parse(event.data))
      }
    },
    getSelectedBatch() {
      let self = this
      this.$store.state.ws.send(JSON.stringify(['getSelectedBatch', this.route, this.selected_batch]))
      this.$store.state.ws.onmessage = function (event) {
        console.log(JSON.parse(event.data))
        self.plotGeoJson(JSON.parse(event.data))
      }
    },
    getSelectedBatchList() {
      let self = this
      this.$store.state.ws.send(JSON.stringify(['getSelectedBatchList', this.route, this.selected]))
      this.$store.state.ws.onmessage = function (event) {
        console.log(JSON.parse(event.data))
        self.geojson_historic_collection = JSON.parse(event.data)
        self.historic_slider['data'] = self.geojson_historic_collection
        self.historic_slider['value'] = self.historic_slider['data'][0]
      }
    },
    displaySelectedHistoric(value) {
      let self = this
      console.log(value)
      console.log(self.geojson_historic_collection[self.geojson_historic_collection_indices[value]])
      self.averageJammingFacotr = self.geojson_historic_collection[self.geojson_historic_collection_indices[value]]['averageJammingFacotr']
      this.deleteGeoJsonPlot()
      self.plotGeoJson(self.geojson_historic_collection[self.geojson_historic_collection_indices[value]]['crawled_batch_id_traffic'])
    },
    getMultipleDaysRouteTraffic() {
      /* reference
          https://stackoverflow.com/questions/18109481/get-all-the-dates-that-fall-between-two-dates
      */
      let self = this
      self.trafficInfoSliderShow = true
      let dateStartTimeStart = new Date(this.dateStartPicker + 'T' + this.timeStartPicer)
      let dateStartTimeEnd = new Date(this.dateStartPicker + 'T' + this.timeEndPicer)
      let dateEndTimeStart = new Date(this.dateEndPicker + 'T' + this.timeStartPicer)
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
        self.trafficInfoSliderDialog = false
        self.displayGeoJson()
      }
    },
    toManhattan() {
      this.center = {lat: 40.725306, lng: -73.988913}
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
      this.directionsDisplay.setMap(null)
      /* eslint-enable */
    },
    getDateBetween(startDate, endDate){
      // pass
    },
    plotGeoJson(geoJsonData) {
      /* input: geoJsonData(a geojson json object)

         This fucntion add the geoJson data to the google map object
      */
      /* eslint-disable */
      // this.geojson_data = new google.maps.Data()
      // this.geojson_data.addGeoJson(geoJsonData)
      // this.geojson_data.setMap(this.$refs.mymap.$mapObject)
      // this.geojson_data.setStyle(function(feature) {
      //   return ({
      //     strokeColor: feature.getProperty('color'),
      //     strokeWeight: 2
      //   })
      // })
      let self = this
      self.$refs.mymap.$mapObject.data.addGeoJson(geoJsonData)
      self.$refs.mymap.$mapObject.data.setStyle(function(feature) {
        return ({
          strokeColor: feature.getProperty('color'),
          strokeWeight: 2,
          zIndex: 5
        })
      })
      this.displayGeoJson()
      /* eslint-enable */
    },
    deleteGeoJsonPlot() {
      /*  inputs: None
          This funciton clears the geojson plotting in the google maps
          return None
      */
      // this.geojson_data.setMap(null)
      // this.geojson_data = null
      let self = this
      self.$refs.mymap.$mapObject.data.forEach(function (feature) {
        self.$refs.mymap.$mapObject.data.remove(feature)
      })
      this.displayGeoJson()
    },
    displayGeoJson() {
      let results
      this.$refs.mymap.$mapObject.data.toGeoJson((geojson) => {
        results = JSON.stringify(geojson, null, 2)
      })
      this.map_geojson = results
    },
    dsiplayRouting() {
      /* eslint-disable */
      console.log(google)
      this.directionsDisplay = new google.maps.DirectionsRenderer()
      this.directionsService = new google.maps.DirectionsService()
      this.directionsDisplay.setMap(this.$refs.mymap.$mapObject)
      this.calculateAndDisplayRoute()
      /* eslint-enable */
    },
    dsiplayRoutingCaseStudy() {
      /* eslint-disable */
      console.log(google)
      this.directionsDisplay = new google.maps.DirectionsRenderer()
      this.directionsService = new google.maps.DirectionsService()
      this.directionsDisplay.setMap(this.$refs.mymap.$mapObject)
      this.calculateAndDisplayRouteCaseStudy()
      /* eslint-enable */
    },
    getHistoric (){
      let self = this
      this.$store.state.ws.send(JSON.stringify(['getHistoric', this.route]))
      this.$store.state.ws.onmessage = function (event) {
        console.log(JSON.parse(event.data))
        self.plotGeoJson(JSON.parse(event.data))
      }
    },
    calculateAndDisplayRoute() {
      let self = this
      /* eslint-disable */
      self.directionsService.route({
        origin: {lat: 33.736818, lng: -84.394652},  // Haight
        destination: {lat: 33.769922, lng: -84.377616},  // Ocean Beach
        // Note that Javascript allows us to access the constant
        // using square brackets and a string value as its
        // "property."
        travelMode: google.maps.TravelMode['DRIVING']     // There are multiple travel mode such as biking walking
      }, function(response, status) {
        if (status == 'OK') {
          self.route = response
          self.directionsDisplay.setDirections(response)
        } else {
          window.alert('Directions request failed due to ' + status)
        }
      })
      /* eslint-enable */
    },
    calculateAndDisplayRouteCaseStudy() {
      let self = this
      /* eslint-disable */
      self.route = CaseStudyDirection
      self.directionsDisplay.setDirections(CaseStudyDirection)
      /* eslint-enable */
    },
    loadControls() {
      this.$refs.mymap.$mapObject.data.setControls(['Polygon'])
    }
  },
  created() {
    // pass
  },
  mounted() {
    // pass
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
