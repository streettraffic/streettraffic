<template lang="pug">
  v-layout(row wrap)
    RegisterRouteStepper(
      ref="RegisterRouteStepper"
      @RegisterRouteStepper_select_routes="RegisterRouteStepper_select_routes"
    )
    HomeMap(
      ref="HomeMap"
      :center.sync="center"
      :route.sync="route"
    )
</template>

<script>
// import custom components
import RegisterRouteStepper from './RegisterRouteStepper.vue'
import HomeMap from '../HomeMap.vue'

export default {
  name: 'RegisterRoute',
  components: {
    RegisterRouteStepper,
    HomeMap
  },
  data () {
    return {
      // HomeMap related states
      center: {lat: 33.7601, lng: -84.37429},
      route: {},
      // References to components
      RegisterRouteStepper: null,
      HomeMap: null,
      HomeSlider: null
    }
  },
  methods: {
    RegisterRouteStepper_select_routes(starting_address_obj, destination_obj) {
      this.HomeMap.displayRouting(starting_address_obj, destination_obj)
    },
    registerRoute() {
      this.$store.state.ws.send(JSON.stringify(['registerRoute', this.route]))
      this.$store.state.ws.onmessage = function (event) { }
    }
  },
  created() {
    // pass
  },
  watch: {
    route(val) {
      console.log(val)
      this.registerRoute()
    }
  },
  mounted() {
    /* eslint-disable */
    this.RegisterRouteStepper = this.$refs.RegisterRouteStepper
    this.HomeMap = this.$refs.HomeMap
    this.HomeSlider = this.$refs.HomeSlider
    /* eslint-enable */
  }
}
</script>
