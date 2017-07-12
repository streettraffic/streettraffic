<template>
  <v-flex xs12 md6>
    <v-stepper v-model="current_step" vertical>
      <v-stepper-step step="1" v-bind:complete="current_step > 1" editable>
        Introduction
      </v-stepper-step>
      <v-stepper-content step="1">
        <div class="mb-5">
          Histraffic.io enables you to visualzie the trafffic pattern on a selected route. Although we hope to support more geographical area, currently we only have data on Atlanta City.
        </div>
        <v-btn primary @click.native="current_step = 2" light>Continue</v-btn>
      </v-stepper-content>
      <v-stepper-step step="2" v-bind:complete="current_step > 2" editable>Select a desired route</v-stepper-step>
      <v-stepper-content step="2">
        <div class="mb-5">
          Simply pick a starting address and destination
          <br><br>
          <v-text-field
            label="Starting Address"
            class="input-group--focused"
            v-model="starting_address"
            id="starting_address"
          ></v-text-field>
          <v-text-field
            label="Destination"
            class="input-group--focused"
            v-model="destination"
            id="destination"
          ></v-text-field>
        </div>
        <v-btn primary @click.native="current_step = 3" light>Select Them</v-btn>
      </v-stepper-content>
      <v-stepper-step step="3" v-bind:complete="current_step > 3" editable>Select an ad format and name ad unit</v-stepper-step>
      <v-stepper-content step="3">
        <v-card class="grey lighten-1 z-depth-1 mb-5" height="200px"></v-card>
        <v-btn primary @click.native="current_step = 4" light>Continue</v-btn>
      </v-stepper-content>
      <v-stepper-step step="4">View setup instructions</v-stepper-step>
      <v-stepper-content step="4">
        <v-card class="grey lighten-1 z-depth-1 mb-5" height="200px"></v-card>
        <v-btn primary @click.native="current_step = 1" light>Continue</v-btn>
      </v-stepper-content>
    </v-stepper>
  </v-flex>
</template>

<script>
export default {
  name: 'HomeStepper',
  data () {
    return {
      current_step: 0,
      starting_address: '',
      destination: ''
    }
  },
  mounted() {
    /* 
    The following code add address autocompletion feature to the input boxes.
    */
    /* eslint-disable */
    let starting_address_input = document.getElementById('starting_address')
    let starting_address_autocomplete = new google.maps.places.Autocomplete(starting_address_input)
    starting_address_autocomplete.addListener('place_changed', function() {
      let place = starting_address_autocomplete.getPlace();
      console.log(place.geometry.location)
    });

    let destination_input = document.getElementById('destination')
    let destination_autocomplete = new google.maps.places.Autocomplete(destination_input)
    destination_autocomplete.addListener('place_changed', function() {
      let place = destination_autocomplete.getPlace();
      console.log(place.geometry)
    });
    /* eslint-enable */
  }
}
</script>
