<template lang="pug">
  v-flex(xs12 md6)
    v-stepper(v-model="current_step" vertical)
      
      // first step
      v-stepper-step(step="1" v-bind:complete="current_step > 1" editable) Select a desired route
      v-stepper-content(step="1")
        div.mb-5
          | Simply pick a starting address and destination
          <br></br>
          v-text-field(
            label="Starting Address"
            class="input-group--focused"
            v-model="starting_address"
            id="starting_address"
          )
          v-text-field(
            label="Destination"
            class="input-group--focused"
            v-model="destination"
            id="destination"
          )
        v-btn(primary @click.native="current_step = 2;select_routes()" light) Select Them
        
      v-stepper-step(step="2") View setup instructions
      v-stepper-content(step="2")
        div.mb-5
          | Great! Now you have query your first data, if you want to try a different time range, hit the try again button.
          a#test(:href="datajson" download="scene.json") test
        v-btn(primary @click.native="current_step = 1" light) Try Again


</template>

<script>
export default {
  name: 'RegisterRouteStepper',
  data () {
    return {
      current_step: 0,
      // data related to selecting desired routes
      starting_address: '',
      destination: '',
      starting_address_obj: {},
      destination_obj: {},
      // data related to selecting time
      dateStartPicker: null,
      dateStartPickerMenu: false,
      dateEndPicker: null,
      dateEndPickerMenu: false,
      timeStartPicer: null,
      timeStartPicerMenu: false,
      timeEndPicer: null,
      timeEndPicerMenu: false,
      retrieving_dialog: false,
      datajson: ''
    }
  },
  props: {
    traffic_data_received: {
      type: Boolean
    }
  },
  methods: {
    select_routes() {
      this.datajson = 'data:text/json;charset=utf-8,' + JSON.stringify(this.starting_address_obj)
      this.$emit('RegisterRouteStepper_select_routes', this.starting_address_obj, this.destination_obj)
    },
    finished_querying_data() {
      this.retrieving_dialog = false
    }
  },
  mounted() {
    /* 
    The following code add address autocompletion feature to the input boxes.
    */
    /* eslint-disable */
    let self = this
    let starting_address_input = document.getElementById('starting_address')
    let starting_address_autocomplete = new google.maps.places.Autocomplete(starting_address_input)
    starting_address_autocomplete.addListener('place_changed', function() {
      let place = starting_address_autocomplete.getPlace();
      self.starting_address_obj = {
        lat: place.geometry.location.lat(),
        lng: place.geometry.location.lng()
      }
    });

    let destination_input = document.getElementById('destination')
    let destination_autocomplete = new google.maps.places.Autocomplete(destination_input)
    destination_autocomplete.addListener('place_changed', function() {
      let place = destination_autocomplete.getPlace();
      self.destination_obj = {
        lat: place.geometry.location.lat(),
        lng: place.geometry.location.lng()
      }
    });
    /* eslint-enable */
  }
}
</script>
