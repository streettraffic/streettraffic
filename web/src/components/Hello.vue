<template>
  <div class="hello">
    <div class="container">
      <div class="map">
        <gmap-map ref = "mymap" :center="center" :zoom="14" style="width: 800px; height: 700px">
          <gmap-polygon :paths="paths" :editable="true" @paths_changed="updateEdited($event)">
          </gmap-polygon>
        </gmap-map>
        <button @click="loadControls">
          Load Drawing Controls
        </button>
        <button @click="displayGeoJson">
          Display GeoJSON Data
        </button>
      </div>
      <div class="test">

        <textarea cols="50" rows="50" v-model="geojson"></textarea>
      </div>
    </div>

  </div>
</template>

<script>
// Check out https://github.com/xkjyeah/vue-google-maps/issues/90 about how we use
// geojson in google maps

import * as VueGoogleMaps from 'vue2-google-maps'
import Vue from 'vue'
import RandomTestData from './random_test_data'

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
      center: {lat: 34.91623, lng: -82.42907},
      markers: [],
      geojson: null
    }
  },
  methods: {
    loadControls() {
      var value = JSON.parse(RandomTestData)
      this.$refs.mymap.$mapObject.data.addGeoJson(value)
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
    }
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
