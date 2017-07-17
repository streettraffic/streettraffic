<template>
  <v-flex xs12 md6>
    <v-stepper v-model="current_step" vertical>
      <v-stepper-step step="1" v-bind:complete="current_step > 1" editable>
        Introduction
      </v-stepper-step>
      <v-stepper-content step="1">
        <div class="mb-5">
          Route Lab component enables you to specify a collection of route object
        </div>
        <v-btn primary @click.native="current_step = 2" light>Continue</v-btn>
      </v-stepper-content>
      <v-stepper-step step="2" v-bind:complete="current_step > 2" editable>Select a desired route</v-stepper-step>
      <v-stepper-content step="2">
        <div class="mb-5">
          Enter a collection of route object
          <br></br>
          <v-text-field
            label="Collection of route object"
            class="input-group--focused"
            v-model="route_collection_json"
          ></v-text-field>
        </div>
        <v-btn primary @click.native="current_step = 3" light>Select Them</v-btn>
      </v-stepper-content>
      <v-stepper-step step="3" v-bind:complete="current_step > 3" editable>Select a time interval</v-stepper-step>
      <v-stepper-content step="3">
        <div class="mb-5">
          What is the time interval of the day that intrigues/annoys you the most? For example, you could choose the rush hours from 8:00 to 10:00
          <br></br>
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
        <v-btn primary @click.native="current_step = 4" light>Continue</v-btn>
        
      </v-stepper-content>
      <v-stepper-step step="4" v-bind:complete="current_step > 3" editable>Choose a date interval</v-stepper-step>
      <v-stepper-content step="4">
        <div class="mb-5">
          Now that you have selected the time interval of day, you can query the that interval for multiple dates. Pick a start date and an end data.
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
        </div>
        <v-dialog v-model="retrieving_dialog" width="600px">
          <v-btn primary slot="activator" @click.native="current_step = 5; select_time()" light>Query Data</v-btn>
          <v-card>
            <v-card-row>
              <v-card-title>Retrieving data from the server</v-card-title>
            </v-card-row>
            <v-card-row>
              <v-card-text v-show="!finished_data">Please be patient :)</v-card-text>
              <v-card-text v-show="finished_data">Finished, now if you want to save the data, simply copy and paste</v-card-text>
            </v-card-row>
            <v-card-row>
              <v-text-field class="mx-3" multi-line :value="JSON.stringify(traffic_pattern)" id="traffic_pattern_input"></v-text-field>
              </div>
            </v-card-row>
            <v-card-row>
              <v-card-text>
                <v-btn v-show="finished_data"  @click.native="copy_to_clipboard" >Copy to ClipBoard</v-btn>
                <v-btn v-show="finished_data" primary @click.native="retrieving_dialog = false" light>Close the dialog</v-btn>
              </v-card-text>
            </v-card-row>
          </v-card>
        </v-dialog>
        
      </v-stepper-content>
      <v-stepper-step step="5">View setup instructions</v-stepper-step>
      <v-stepper-content step="5">
        <div class="mb-5">
          Finished.
        </div>
      </v-stepper-content>
    </v-stepper>
  </v-flex>
</template>

<script>
export default {
  name: 'RouterLabStepper',
  data () {
    return {
      current_step: 0,
      // data related to selecting desired routes
      route_collection_json: '',
      // data related to selecting time
      dateStartPicker: null,
      dateStartPickerMenu: false,
      dateEndPicker: null,
      dateEndPickerMenu: false,
      timeStartPicer: null,
      timeStartPicerMenu: false,
      timeEndPicer: null,
      timeEndPicerMenu: false,
      finished_data: false,
      retrieving_dialog: false
    }
  },
  props: {
    traffic_pattern: {}
  },
  methods: {
    select_time() {
      this.$emit('HomeStepper_select_time', this.dateStartPicker, this.dateEndPicker, this.timeStartPicer, this.timeEndPicer, JSON.parse(this.route_collection_json))
    },
    finished_querying_data() {
      this.finished_data = true
    },
    copy_to_clipboard() {
      let copyTextarea = document.getElementById('traffic_pattern_input')
      console.log(copyTextarea)
      copyTextarea.select()
      document.execCommand('copy')
    }
  },
  computed: {
    download_link() {
      return 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(this.traffic_pattern))
    }
  },
  mounted() {
    /* 
    The following code add address autocompletion feature to the input boxes.
    */
    /* eslint-disable */
    let self = this
    /* eslint-enable */
  }
}
</script>
