<template lang="pug">
  v-layout(row wrap)
    v-flex.my-3(xs8)
      h6 Histraffic Polygon section
      p
        | In this section, you can draw a polygon in the map to specify an area of which you will download traffic data from. To start, simply click the 
        span(style='font-weight:bold') 'Load Drawing Tools'
        |  button below, and start drawing. After you are finished, click the 
        span(style='font-weight:bold') 'Finished Drawing Polygon'
        |  button
      p Note: right now we don't support self-intersecting polygon or multiple polygons
      div
        v-btn.ml-0.mt-3(dark left default @click.native='loadControls') 1. Load Drawing Tools
        v-dialog(v-model='dialog', width='600px')
          v-btn.ml-0.mt-3(dark left default @click.native='displayGeoJson', slot='activator') 2. Finished Drawing Polygon
          v-card
            v-card-title
              .headline Geojson Format (prettified)
            v-card-text
              .geojson_output
                textarea(style='width: 100%; height: 300px', v-model='map_geojson')
            v-card-title
              .headline Geojson Format (uglified)
            v-card-text
              p
                | Now, simply copy the following json encoded string, and use map_resource.ultil.read_geojson_polygon() to generate a polygon
              .geojson_output
                div '{{map_geojson}}'
    v-flex.my-3(xs12='')
      v-card
        v-card-row.green.darken-1
          v-card-title
            span.white--text The Map
            v-spacer
        v-card-text
          v-card-row(height='auto', center='')
            gmap-map(ref='mymap', :center='center', :zoom='14', style='width: 100%; height: 500px')

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
