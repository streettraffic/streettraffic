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
          <br></br>
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
        <v-btn primary @click.native="current_step = 3;select_routes()" light>Select Them</v-btn>
      </v-stepper-content>
      <v-stepper-step step="3" v-bind:complete="current_step > 3" editable>Select a desired start date, end date, start time, and end time</v-stepper-step>
      <v-stepper-content step="3">
        <div class="mb-5">
          For Example, if the start date is 2017-07-05, end date is 2017-07-13, start time is 09:00, and end time is 12:00, our program would pull the traffic data from 09:00 to 12:00 on each day bewteen 2017-07-05 and 2017-07-13
          <br></br>
          <v-menu
            lazy
            :close-on-content-click="false"
            v-model="dateStartPickerMenu"
            offset-y
            full-width
            :nudge-left="40"
            max-width="290px"
          >
            <v-text-field
              slot="activator"
              label="Start Date"
              v-model="dateStartPicker"
              prepend-icon="event"
              readonly
            ></v-text-field>
            <v-date-picker v-model="dateStartPicker" no-title scrollable autosave>
            </v-date-picker>
          </v-menu>
          <v-menu
            lazy
            :close-on-content-click="false"
            v-model="dateEndPickerMenu"
            offset-y
            full-width
            :nudge-left="40"
            max-width="290px"
          >
            <v-text-field
              slot="activator"
              label="End Date"
              v-model="dateEndPicker"
              prepend-icon="event"
              readonly
            ></v-text-field>
            <v-date-picker v-model="dateEndPicker" no-title scrollable autosave>
            </v-date-picker>
          </v-menu>
          <v-menu
            lazy
            :close-on-content-click="false"
            v-model="timeStartPicerMenu"
            offset-y
            :nudge-left="40"
          >
            <v-text-field
              slot="activator"
              label="Start Time"
              v-model="timeStartPicer"
              prepend-icon="access_time"
              readonly
            ></v-text-field>
            <v-time-picker v-model="timeStartPicer" autosave format="24hr"></v-time-picker>
          </v-menu>
          <v-menu
            lazy
            :close-on-content-click="false"
            v-model="timeEndPicerMenu"
            offset-y
            :nudge-left="40"
          >
            <v-text-field
              slot="activator"
              label="End Time"
              v-model="timeEndPicer"
              prepend-icon="access_time"
              readonly
            ></v-text-field>
            <v-time-picker v-model="timeEndPicer" autosave format="24hr"></v-time-picker>
          </v-menu>
        </div>
        <v-btn primary @click.native="current_step = 4; select_time()" light>Continue</v-btn>
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
      timeEndPicerMenu: false
    }
  },
  methods: {
    select_routes() {
      this.$emit('select_routes', this.starting_address_obj, this.destination_obj)
      this.$emit('xixi')
    },
    select_time() {
      this.$emit('select_time', this.dateStartPicker, this.dateEndPicker, this.timeStartPicer, this.timeEndPicer)
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
