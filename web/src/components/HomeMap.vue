<template>
  <v-flex xs12 md6 class="my-3">
    <v-card class="elevation-12">
      <v-card-row class="green darken-1">
        <v-card-title>
          <span class="white--text">The Map</span>
          <v-spacer></v-spacer>
        </v-card-title>
      </v-card-row>
      <v-card-text>
        <v-card-row height="auto" center>
          <gmap-map ref = "mymap" :center="local_center" :zoom="14" style="width: 100%; height: 400px" 
              @click="location = {lat: $event.latLng.lat(), lng:$event.latLng.lng()}; getLocation()">
            <gmap-marker v-if="location" :position="location" /></gmap-marker>
          </gmap-map>
        </v-card-row>
      </v-card-text>
    </v-card>
  </v-flex>
</template>

<script>
// To see how we use geojson in google maps, check out
// https://github.com/xkjyeah/vue-google-maps/issues/90 about how we use
// To see how we use the Direction api, refer to
// https://developers.google.com/maps/documentation/javascript/examples/directions-travel-modes

import CaseStudyDirection from '../assets/case_study_newyork_boston.json'

export default {
  name: 'HomeMap',
  data () {
    return {
      local_center: this.center,
      map_geojson: null,
      traffic_data_received: false,
      route: null,
      directionsDisplay: null,
      directionsService: null,
      location: null
    }
  },
  props: {
    center: Object,
    origin_obj: Object,
    destination_obj: Object,
    geojson_data: Object
  },
  methods: {
    getLocation() {
      let self = this
      this.$store.state.ws.send(JSON.stringify(['getRoadData', this.location, 10000, 10]))
      this.$store.state.ws.onmessage = function (event) {
        self.plotGeoJson(JSON.parse(event.data))
      }
    },
    plotGeoJson(geoJsonData) {
      /* input: geoJsonData(a geojson json object)

         This fucntion add the geoJson data to the google map object
      */
      /* eslint-disable */
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
    dsiplayRouting(origin_obj, destination_obj) {
      /* eslint-disable */
      console.log(google)
      this.directionsDisplay = new google.maps.DirectionsRenderer()
      this.directionsService = new google.maps.DirectionsService()
      this.directionsDisplay.setMap(this.$refs.mymap.$mapObject)
      this.calculateAndDisplayRoute(origin_obj, destination_obj)
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
    calculateAndDisplayRoute(origin_obj, destination_obj) {
      /* 
      example inputs:
      origin_obj = {lat: 33.736818, lng: -84.394652}
      destination_obj = {lat: 33.769922, lng: -84.377616}
      */
      console.log(origin_obj, destination_obj)
      let self = this
      /* eslint-disable */
      self.directionsService.route({
        origin: origin_obj,  // Haight
        destination: destination_obj,  // Ocean Beach
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
    /* eslint-disable */

    /* eslint-enable */
  },
  watch: {
    local_center(val) {
      this.$emit('update:center', val)
    },
    origin_obj(val) {
      if(val) {
        if (this.destination_obj){
          dsiplayRouting(val, this.destination_obj)
        }
      }
    },
    geojson_data(val) {
      plotGeoJson(val)
    }
  }
}
</script>