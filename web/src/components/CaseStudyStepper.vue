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
        </div>
        <v-btn primary @click.native="current_step = 3;select_routes()" light>Select Them</v-btn>
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
        <v-dialog v-model="retrieving_dialog" persistent>
          <v-btn primary slot="activator" @click.native="current_step = 5; select_time()" light>Query Data</v-btn>
          <v-card>
            <v-card-row>
              <v-card-title>Retrieving data from the server</v-card-title>
            </v-card-row>
            <v-card-row>
              <v-card-text>Please be patient :)</v-card-text>
            </v-card-row>
          </v-card>
        </v-dialog>
        
      </v-stepper-content>
      <v-stepper-step step="5">View setup instructions</v-stepper-step>
      <v-stepper-content step="5">
        <div class="mb-5">
          Great! Now you have query your first data, if you want to try a different time range, hit the try again button.
        </div>
        <v-btn primary @click.native="current_step = 3" light>Try Again</v-btn>
      </v-stepper-content>
    </v-stepper>
  </v-flex>
</template>

<script>
import CaseStudyDirection from '../assets/case_study_newyork_boston.json'

export default {
  name: 'CaseStudyStepper',
  data () {
    return {
      current_step: 0,
      // data related to selecting desired routes
      // data related to selecting time
      caseStudyRoute: CaseStudyDirection,
      dateStartPicker: null,
      dateStartPickerMenu: false,
      dateEndPicker: null,
      dateEndPickerMenu: false,
      timeStartPicer: null,
      timeStartPicerMenu: false,
      timeEndPicer: null,
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
      this.$emit('CaseStudyStepper_select_routes')
    },
    select_time() {
      this.$emit('CaseStudyStepper_select_time', this.dateStartPicker, this.dateEndPicker, this.timeStartPicer, this.timeEndPicer)
    },
    finished_querying_data() {
      this.retrieving_dialog = false
    }
  }
}
</script>
