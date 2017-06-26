<template>
  <v-layout>
    <v-flex xs12>
      <v-card>
        <v-card-row class="green darken-1">
          <v-card-title>
            <span class="white--text">The Map</span>
            <v-spacer></v-spacer>
          </v-card-title>
        </v-card-row>
        <v-card-text>
          <v-card-row height="auto" center>
            <gmap-map ref = "mymap" :center="center" :zoom="14" style="width: 50%; height: 400px" 
                @click="location = {lat: $event.latLng.lat(), lng:$event.latLng.lng()}; getLocation()">
              <gmap-marker v-if="location" :position="location" />
            </gmap-map>
            <div class="geojson_output">
              <p>Click displayGeoJson to see what happens</p>
              <textarea style="width: 100%; height: 380px" v-model="geojson"></textarea>
            </div>
          </v-card-row>
        </v-card-text>
      </v-card>
      
      <v-divider class="my-4"></v-divider>

      <v-btn dark default @click.native="plotGeoJson(testData)">plotGeoJson(testData)</v-btn>
      <v-btn dark default @click.native="displayGeoJson">displayGeoJson</v-btn>
      <v-btn dark default @click.native="dsiplayRouting">dsiplayRouting</v-btn>
      <v-btn dark default @click.native="getHistoric">getHistoric</v-btn>
      <v-btn dark default @click.native="toManhattan">toManhattan</v-btn>
      <v-btn dark default @click.native="test">test</v-btn>

<!--         <button @click="plotGeoJson(testData)">
          Plot Atlanta Data
        </button>
        <button @click="displayGeoJson">
          Display GeoJSON Text 
        </button>
        <button @click="dsiplayRouting">
          Display Routing
        </button>
        <button @click="getHistoric">
          Get Historic Traffic info
        </button>
        <button @click="toManhattan">
          To Manhattan
        </button>
        <button @click = "test">
          Test
        </button> -->

      <h3>Select your desired dates:</h3>
      <v-data-table
        v-bind:headers="headers"
        v-bind:items="historic_batch"
        v-bind:search="search"
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
      <div class="test">
        
        <h3>other</h3>
        <select v-model="selected_batch" @change="getSelectedBatch">
          <option v-for="item in historic_batch" :value="item.id"> {{item.crawled_timestamp}} </option>
        </select>
        <div>Selected: {{ selected_batch }}</div>
      </div>
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
import TestData from './level17.json'

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyAucd0sk7vH1NjQyh3b2kN8qYKhdu4S1Ss'
    // libraries: 'places', //// If you need to use place input
  }
})

export default {
  name: 'hello',
  data () {
    return {
      center: {lat: 33.7601, lng: -84.37429}, // {lat: 34.91623, lng: -82.42907}  Furman   {lat: 33.7601, lng: -84.37429} Atlanta
      geojson: null,
      ws: null,
      route: null,
      directionsDisplay: null,
      directionsService: null,
      location: null,
      locationData: null,
      testData: TestData,
      selected_batch: '',
      historic_batch: ['A', 'B', 'C'],
      geojson_data: null,
      ex1: 'haha',
      ex2: 'xixi',
      search: '',
      selected: [],
      headers: [
        {
          text: 'crawled_batch_id',
          left: true,
          sortable: false,
          value: 'name'
        },
        { text: 'crawled_timestamp', sortable: false, value: 'calories' }
      ],
      items: [
        {
          name: 'Frozen Yogurt',
          calories: 159
        },
        {
          name: 'Ice cream sandwich',
          calories: 237
        },
        {
          name: 'Eclair',
          calories: 262
        }
      ]
    }
  },
  methods: {
    getLocation() {
      let scope = this
      this.locationData = JSON.stringify(this.location)
      this.ws.send(JSON.stringify(['getRoadData', this.location, 10000, 10]))
      this.ws.onmessage = function (event) {
        scope.plotGeoJson(JSON.parse(event.data))
      }
    },
    getSelectedBatch() {
      let scope = this
      this.deleteGeoJsonPlot()
      this.ws.send(JSON.stringify(['getSelectedBatch', this.route, this.selected_batch]))
      this.ws.onmessage = function (event) {
        console.log(JSON.parse(event.data))
        scope.plotGeoJson(JSON.parse(event.data))
      }
    },
    toManhattan() {
      this.center = {lat: 40.725306, lng: -73.988913}
    },
    test(){
      /* eslint-disable */
      console.log(this.selected)
      console.log(this.historic_batch)
      /* eslint-enable */
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
          strokeWeight: 2
        })
      })
      /* eslint-enable */
    },
    deleteGeoJsonPlot() {
      /*  inputs: None
          This funciton clears the geojson plotting in the google maps
          return None
      */
      // this.geojson_data.setMap(null)
      // this.geojson_data = null
      let scope = this
      scope.$refs.mymap.$mapObject.data.forEach(function (feature) {
        scope.$refs.mymap.$mapObject.data.remove(feature)
      })

      // reset map directionDisplay, otherwise, the direction layer might be on the top of
      // our traffic geojson layer.
      this.directionsDisplay.setMap(null)
      this.directionsDisplay.setMap(this.$refs.mymap.$mapObject)
    },
    displayGeoJson() {
      let results
      this.$refs.mymap.$mapObject.data.toGeoJson((geojson) => {
        results = JSON.stringify(geojson, null, 2)
      })
      this.geojson = results
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
      let scope = this
      this.ws.send(JSON.stringify(['getHistoric', this.route]))
      this.ws.onmessage = function (event) {
        console.log(JSON.parse(event.data))
        scope.plotGeoJson(JSON.parse(event.data))
      }
    },
    calculateAndDisplayRoute() {
      let scope = this
      /* eslint-disable */
      scope.directionsService.route({
        origin: {lat: 33.736818, lng: -84.394652},  // Haight.
        destination: {lat: 33.769922, lng: -84.377616},  // Ocean Beach.
        // Note that Javascript allows us to access the constant
        // using square brackets and a string value as its
        // "property."
        travelMode: google.maps.TravelMode['DRIVING']     // There are multiple travel mode such as biking walking
      }, function(response, status) {
        if (status == 'OK') {
          scope.route = response
          scope.directionsDisplay.setDirections(response)
        } else {
          window.alert('Directions request failed due to ' + status)
        }
      })
      /* eslint-enable */
    }
  },
  created() {
    let scope = this
    this.ws = new WebSocket('ws://localhost:8765/')
    console.log('connecting websocket', this.ws)
    this.ws.onopen = function (){
      scope.ws.send(JSON.stringify(['getHistoricBatch']))
    }
    this.ws.onmessage = function (event) {
      console.log('received')
      console.log(JSON.parse(event.data))
      scope.historic_batch = JSON.parse(event.data)
    }
  },
  mounted() {
    // pass
  }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style lang="scss" scoped>

.geojson_output {
  width: 40%;
  margin-left: 20px;
}
  textarea {
    border-style: solid;
  }
</style>
