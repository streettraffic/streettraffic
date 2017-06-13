<template>
  <div class="hello">
    <h1>Hello World</h1>
    <div class="container">
      <div class="map">
        <gmap-map
          :center="center"
          :zoom="7"
          style="width: 800px; height: 800px"
        >
          <gmap-marker
            :key="index"
            v-for="(m, index) in markers"
            :position="m.position"
            :clickable="true"
            :draggable="true"
            @click="center=m.position"
          ></gmap-marker>
        </gmap-map>
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
      center: {lat: 10.0, lng: 10.0},
      markers: [{
        position: {lat: 10.0, lng: 10.0}
      }, {
        position: {lat: 11.0, lng: 11.0}
      }]
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.container {
  position: relative;
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
