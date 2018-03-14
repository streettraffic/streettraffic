<template lang="pug">
  v-flex(xs12 md6)
    v-stepper(v-model="current_step" vertical)
      v-stepper-step(step="1" v-bind:complete="current_step > 1" editable) Introduction
      v-stepper-content(step="1")
        div.mb-5 
          | StreetTraffic package enables you to visualzie the trafffic pattern on a selected route. 
          | Although we hope to support more geographical area, currently we only have data on Atlanta City.
        v-btn(primary @click.native="current_step = 2" light) Continue
      v-stepper-step(step="2" v-bind:complete="current_step > 2" editable) Select a desired route
      
      v-stepper-content(step="2")
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
        v-btn(primary @click.native="current_step = 3;select_routes()" light) Select Them

      v-stepper-step(step="3" v-bind:complete="current_step > 3" editable) Select a time interval
      v-stepper-content(step="3")
        div.mb-5
          | What is the time interval of the day that intrigues/annoys you the most? For example, you could choose the rush hours from 8:00 to 10:00
          br
          v-menu(
            lazy
            :close-on-content-click="false"
            v-model="timeStartPicerMenu"
            offset-y
            :nudge-left="40"
          )
            v-text-field(
              slot="activator"
              label="Start Time"
              v-model="timeStartPicer"
              prepend-icon="access_time"
              readonly
            )
            v-time-picker(v-model="timeStartPicer" autosave format="24hr")
          v-menu(
            lazy
            :close-on-content-click="false"
            v-model="timeEndPicerMenu"
            offset-y
            :nudge-left="40"
          )
            v-text-field(
              slot="activator"
              label="End Time"
              v-model="timeEndPicer"
              prepend-icon="access_time"
              readonly
            )
            v-time-picker(v-model="timeEndPicer" autosave format="24hr")
        v-btn(primary @click.native="current_step = 4" light) Continue
        
      v-stepper-step(step="4" v-bind:complete="current_step > 3" editable) Choose a date interval
      v-stepper-content(step="4")
        div.mb-5
          | Now that you have selected the time interval of day, you can query the that interval for multiple dates. Pick a start date and an end data.
          br
          v-menu(
            lazy
            :close-on-content-click="false"
            v-model="dateStartPickerMenu"
            offset-y
            full-width
            :nudge-left="40"
            max-width="290px"
          )
            v-text-field(
              slot="activator"
              label="Start Date"
              v-model="dateStartPicker"
              prepend-icon="event"
              readonly
            )
            v-date-picker(v-model="dateStartPicker" no-title scrollable autosave)
          v-menu(
            lazy
            :close-on-content-click="false"
            v-model="dateEndPickerMenu"
            offset-y
            full-width
            :nudge-left="40"
            max-width="290px"
          )
            v-text-field(
              slot="activator"
              label="End Date"
              v-model="dateEndPicker"
              prepend-icon="event"
              readonly
            )
            v-date-picker(v-model="dateEndPicker" no-title scrollable autosave)
        v-dialog(v-model="retrieving_dialog" persistent)
          v-btn(primary slot="activator" @click.native="current_step = 5; select_time()" light) Query Data
          v-card
            v-card-row
              v-card-title Retrieving data from the server
            v-card-row
              v-card-text Please be patient :)
        
      v-stepper-step(step="5") View setup instructions
      v-stepper-content(step="5")
        div.mb-5
          | Great! Now you have query your first data, if you want to try a different time range, hit the try again button.
        v-btn(primary @click.native="current_step = 3" light) Try Again


</template>

<script>
export default {
  name: 'HomeStepper',
  data () {
    return {
      current_step: 0,
      // data related to selecting desired routes
      starting_address: 'Sweet Auburn Market, Edgewood Avenue',
      destination: 'The Fox Theatre',
      starting_address_obj: {'lat': 33.7544084, 'lng': -84.3799879},
      destination_obj: {'lat': 33.7725845, 'lng': -84.38560280000002},
      // data related to selecting time
      dateStartPicker: '2017-06-24',
      dateStartPickerMenu: false,
      dateEndPicker: '2017-06-25',
      dateEndPickerMenu: false,
      timeStartPicer: '16:00',
      timeStartPicerMenu: false,
      timeEndPicer: '20:00',
      timeEndPicerMenu: false,
      retrieving_dialog: false
    }
  },
  props: {
    traffic_data_received: {
      type: Boolean
    }
  },
  methods: {
    select_routes() {
      this.$emit('HomeStepper_select_routes', this.starting_address_obj, this.destination_obj)
    },
    select_time() {
      this.$emit('HomeStepper_select_time', this.dateStartPicker, this.dateEndPicker, this.timeStartPicer, this.timeEndPicer)
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
