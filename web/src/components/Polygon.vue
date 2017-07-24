<template>
  <v-layout row wrap>
    <v-flex xs8 class="my-3">
      <h6>Histraffic Polygon section</h6>
      <p>In this section, you can draw a polygon in the map to specify an area of which you will download traffic data from. To start, simply click the <span style="font-weight:bold">'Load Drawing Tools'</span> button below, and start drawing. After you are finished, click the <span style="font-weight:bold">'Finished Drawing Polygon'</span> button</p>
      <p>Note: right now we don't support self-intersecting polygon or multiple polygons</p>
      <div>
        <v-btn dark left default @click.native="loadControls" class="ml-0 mt-3">1. Load Drawing Tools</v-btn>
        <v-dialog v-model="dialog" width="600px">
          <v-btn dark left default @click.native="displayGeoJson" class="ml-0 mt-3" slot="activator">2. Finished Drawing Polygon</v-btn>
          <v-card>
            <v-card-title>
              <div class="headline">Geojson Format (prettified)</div>
            </v-card-title>
            <v-card-text>
              <div class="geojson_output">
                <textarea style="width: 100%; height: 300px" v-model="map_geojson"></textarea>
              </div>
            </v-card-text>
            <v-card-title>
              <div class="headline">Geojson Format (uglified)</div>
            </v-card-title>
            <v-card-text>
              <p>Now, simply copy the following json encoded string, and use map_resource.ultil.read_geojson_polygon() to generate a polygon</p>
              <div class="geojson_output">
                <div>'{{map_geojson}}'</div>
              </div>
            </v-card-text>
          </v-card>
        </v-dialog>
      </div>
    </v-flex>
    <v-flex xs12 class="my-3">
      <v-card>
        <v-card-row class="green darken-1">
          <v-card-title>
            <span class="white--text">The Map</span>
            <v-spacer></v-spacer>
          </v-card-title>
        </v-card-row>
        <v-card-text>
          <v-card-row height="auto" center>
            <gmap-map ref = "mymap" :center="center" :zoom="14" style="width: 100%; height: 500px">
            </gmap-map>
          </v-card-row>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
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
  name: 'Polygon',
  data () {
    return {
      center: {lat: 33.7601, lng: -84.37429}, // {lat: 34.91623, lng: -82.42907}  Furman   {lat: 33.7601, lng: -84.37429} Atlanta
      map_geojson: null,
      dialog: false
    }
  },
  methods: {
    displayGeoJson() {
      let results
      this.$refs.mymap.$mapObject.data.toGeoJson((geojson) => {
        results = JSON.stringify(geojson, null, 2)
      })
      this.map_geojson = results
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
</style>
