<template>
  <div class="hello">
    <div class="container">
      <div class="map">
        <gmap-map
          ref = "mymap"
          :center="center"
          :zoom="4"
          style="width: 800px; height: 800px"
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
      </div>

    </div>
    <button @click="loadControls">
      Load Drawing Controls
    </button>
    <button @click="displayGeoJson">
      Display GeoJSON Data
    </button>
    <textarea cols="300" rows="50" v-model="geojson"></textarea>
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
      center: {lat: -22.14, lng: 123.61},
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
      this.$refs.mymap.$mapObject.data.loadGeoJson('https://storage.googleapis.com/mapsdevsite/json/google.json')
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
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
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
