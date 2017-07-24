<template>
  <v-parallax src="https://raw.githubusercontent.com/vuetifyjs/docs/master/static/doc-images/parallax/material.jpg" class="elevation-12">
    <v-layout column align-center justify-center>
      <h1 class="white--text">Histraffic.io</h1>
      <h4 class="white--text">Use historic traffic to plan traveling!</h4>
      <div class="mt-5">
        <v-btn dark large router :to="'/Main'" class="green lighten-2">Get Started</v-btn>
      </div>
    </v-layout>
  </v-parallax>
</template>

<script>
export default {
  name: 'Landing',
  data () {
    return {
      center: {lat: 33.7601, lng: -84.37429}, // {lat: 34.91623, lng: -82.42907}  Furman   {lat: 33.7601, lng: -84.37429} Atlanta
      map_geojson: null,
      dialog: false
    }
  },
  methods: {
    // pass
  },
  created() {
    // pass
  },
  mounted() {
    // pass
  }
}
</script>
