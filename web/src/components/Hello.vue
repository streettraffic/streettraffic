<template>
  <div class="hello">
    <div class="container">
      <div class="map">
        <gmap-map ref = "mymap" :center="center" :zoom="14" style="width: 800px; height: 700px">
        </gmap-map>
        <button @click="loadControls">
          Load Drawing Controls
        </button>
        <button @click="displayGeoJson">
          Display GeoJSON Data
        </button>
        <button @click="dsiplayRouting">
          Display Routing
        </button>
        <button @click="getHistoric">
          Get Historic Traffic info
        </button>
      </div>
      <div class="test">

        <textarea cols="50" rows="50" v-model="geojson"></textarea>
      </div>
    </div>

  </div>
</template>

<script>
// To see how we use geojson in google maps, check out
// https://github.com/xkjyeah/vue-google-maps/issues/90 about how we use
// To see how we use the Direction api, refer to
// https://developers.google.com/maps/documentation/javascript/examples/directions-travel-modes

import * as VueGoogleMaps from 'vue2-google-maps'
import Vue from 'vue'
import TestData from './history_traffic_route.json'

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
      scope: this
    }
  },
  methods: {
    loadControls() {
      console.log(this == this.scope)
      this.$refs.mymap.$mapObject.data.addGeoJson(TestData)
      this.$refs.mymap.$mapObject.data.setStyle(function(feature) {
        return ({
          strokeColor: feature.getProperty('color'),
          strokeWeight: 3
        })
      })
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
      // console.log(google)
      this.directionsDisplay = new google.maps.DirectionsRenderer()
      this.directionsService = new google.maps.DirectionsService()
      this.directionsDisplay.setMap(this.$refs.mymap.$mapObject)
      this.calculateAndDisplayRoute()

      /* eslint-enable */
    },
    getHistoric (){
      let scope = this
      this.ws.send('getHistoric')
      this.ws.send(JSON.stringify(this.route))
      this.ws.onmessage = function (event) {
        scope.$refs.mymap.$mapObject.data.addGeoJson(JSON.parse(event.data))
        scope.$refs.mymap.$mapObject.data.setStyle(function(feature) {
          return ({
            strokeColor: feature.getProperty('color'),
            strokeWeight: 3
          })
        })
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
    this.ws = new WebSocket('ws://127.0.0.1:8765/')
    console.log('connecting websocket', this.ws)
  }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped>
.container {
  position: relative;
  height: 90vh;
}

.map {
  display: inline-block;
}

.test {
  display: inline-block;
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
