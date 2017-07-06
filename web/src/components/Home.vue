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
            <v-btn primary light slot="activator" @click.native="getRouteTraffic">Open Dialog</v-btn>
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
import vueSlider from './vue2-slider'
import { mapState } from 'vuex'

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyAucd0sk7vH1NjQyh3b2kN8qYKhdu4S1Ss'
    // libraries: 'places', //// If you need to use place input
  }
})

export default {
  name: 'Home',
  components: {
    vueSlider
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
      timeEndPicer: null
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
      self.deleteGeoJsonPlot()
      self.plotGeoJson(self.geojson_historic_collection[self.geojson_historic_collection_indices[self.historic_slider.value]]['crawled_batch_id_traffic'])
    },
    getRouteTraffic() {
      let self = this
      self.trafficInfoSliderShow = true
      let startTime = new Date(this.dateStartPicker + 'T' + this.timeStartPicer)
      let endTime = new Date(this.dateStartPicker + 'T' + this.timeEndPicer)
      console.log(startTime.toISOString())
      console.log(endTime.toISOString())
      this.$store.state.ws.send(JSON.stringify(['getRouteTraffic', this.route, startTime, endTime]))
      this.$store.state.ws.onmessage = function (event) {
        self.geojson_historic_collection = JSON.parse(event.data)
        // initialize local time within geojson_historic_collection
        self.geojson_historic_collection.forEach((item, index) => {
          item['local_timestamp'] = new Date(item['crawled_timestamp'])
        })

        console.log(self.geojson_historic_collection)
        console.log(self.geojson_historic_collection_indices)
        self.historic_slider['data'] = self.geojson_historic_collection.map((item, index) => {
          // if hours == 0 and minutes == 0, it must be a whole date
          if (item.local_timestamp.getHours() == 0 && item.local_timestamp.getMinutes() == 0){
            self.geojson_historic_collection_indices[item.local_timestamp.toLocaleDateString()] = index
            return item.local_timestamp.toLocaleDateString()
          }
          // else it must be a intraday hours and minutes
          else {
            self.geojson_historic_collection_indices[item.local_timestamp.toLocaleTimeString()] = index
            return item.local_timestamp.toLocaleTimeString()
          }
        })
        self.historic_slider['value'] = self.historic_slider['data'][0]
        let slider = self.$refs['historic_slider_ref']
        slider.refresh()
        self.displaySelectedHistoric(self.historic_slider['value'])
        self.trafficInfoSliderDialog = false
      }
    },
    toManhattan() {
      this.center = {lat: 40.725306, lng: -73.988913}
    },
    test(){
      /* eslint-disable */
      console.log(this.historic_slider.data)
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
      this.$refs.mymap.$mapObject.data.addGeoJson(geoJsonData)
      this.$refs.mymap.$mapObject.data.setStyle(function(feature) {
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

      // reset map directionDisplay, otherwise, the direction layer might be on the top of
      // our traffic geojson layer.
      this.directionsDisplay.setMap(null)
      this.directionsDisplay.setMap(this.$refs.mymap.$mapObject)
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
        origin: {lat: 33.736818, lng: -84.394652},  // Haight.
        destination: {lat: 33.769922, lng: -84.377616},  // Ocean Beach.
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
