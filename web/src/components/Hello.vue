<template>
  <div class="hello">
    <div class="container">
      <div class="map">
        <gmap-map
          ref = "mymap"
          :center="center"
          :zoom="14"
          style="width: 800px; height: 700px"
        >
<!--           <gmap-marker
            :key="index"
            v-for="(m, index) in markers"
            :position="m.position"
            :clickable="true"
            :draggable="true"
            @click="center=m.position"
          ></gmap-marker> -->
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
import * as VueGoogleMaps from 'vue2-google-maps'
import Vue from 'vue'

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
      paths: [
          [ {lat: 1.380, lng: 103.800}, {lat: 1.380, lng: 103.810}, {lat: 1.390, lng: 103.810}, {lat: 1.390, lng: 103.800} ],
          [ {lat: 1.382, lng: 103.802}, {lat: 1.382, lng: 103.808}, {lat: 1.388, lng: 103.808}, {lat: 1.388, lng: 103.802} ]
      ],
      geojson: null
    }
  },
  methods: {
    loadControls() {
      var value = JSON.parse('{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"coordinates": [[-82.42968, 34.92954], [-82.43003, 34.92729]], "type": "LineString"}, "properties": {"TMC": {"DE": "US-25-BR/US-276/Poinsett Hwy", "LE": 1.87469, "PC": 10933, "QD": "+"}, "CF": {"CN": 0.7, "FF": 41.01, "JF": 1.89393, "LN": [], "SP": 31.69, "SU": 31.69, "TY": "TR"}}}, {"type": "Feature", "geometry": {"coordinates": [[-82.42907, 34.91623], [-82.42911, 34.91647], [-82.42917, 34.91684]], "type": "LineString"}, "properties": {"TMC": {"DE": "Old Buncombe Rd", "LE": 1.67396, "PC": 10934, "QD": "-"}, "CF": {"CN": 0.7, "FF": 42.25, "JF": 1.71568, "LN": [], "SP": 33.55, "SU": 33.55, "TY": "TR"}}}]}')
      this.$refs.mymap.$mapObject.data.addGeoJson(value)
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
