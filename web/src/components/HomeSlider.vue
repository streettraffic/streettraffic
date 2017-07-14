<template>
  <v-flex xs12 class="my-3" v-show="trafficInfoSliderShow">
    <v-card>
      <v-card-row class="green darken-1">
        <v-card-title>
          <span class="white--text">Traffic Info Slider</span>
          <v-spacer></v-spacer>
        </v-card-title>
      </v-card-row>
      <v-card-text>
        <v-card-row>
          This will automatically show the geojson data that has been plotted into the map<br> <br>
        </v-card-row>
        <v-card-row height="auto">
          <div class="historic_slider">
            <vue-slider @callback="displaySelectedHistoric" :real-time="true" ref="historic_slider_ref" v-bind="historic_slider" v-model="historic_slider.value"></vue-slider>
            <br>
            <p>Currently Dsiplayed: {{ historic_slider.value }}</p>
            <p>Avrage Jamming Factor: {{ averageJammingFacotr }}</p>
            <div class="jammingFactorChart">
              <Chart v-if="chartFinished" :data="chartData" :labels="chartLabel" :chartTitle="'Average Jamming Factor at Each Time Period'"></Chart>
            </div>
          </div>
        </v-card-row>
      </v-card-text>
    </v-card>
  </v-flex>
</template>

<script>
import Chart from './Chart.vue'
import vueSlider from 'vue-slider-component'

export default {
  name: 'HomeSlider',
  components: {
    vueSlider,
    Chart
  },
  data() {
    return {
      trafficInfoSliderShow: false,
      historic_slider: {
        value: '',
        width: '90%',
        disabled: false,
        tooltip: 'hover',
        piecewise: true,
        data: []   // This will be initialized in the created() funciton
      },
      geojson_historic_collection: null,
      geojson_historic_collection_indices: {},
      averageJammingFacotr: null,
      chartLabel: [],
      chartData: [],
      chartFinished: false
    }
  },
  props: {
    route: {
      type: Object
    }
  },
  methods: {
    getMultipleDaysRouteTraffic(dateStartPicker, dateEndPicker, timeStartPicer, timeEndPicer) {
      /* reference
          https://stackoverflow.com/questions/18109481/get-all-the-dates-that-fall-between-two-dates
      */
      let self = this
      self.trafficInfoSliderShow = true
      let dateStartTimeStart = new Date(dateStartPicker + 'T' + timeStartPicer)
      let dateStartTimeEnd = new Date(dateStartPicker + 'T' + timeEndPicer)
      let dateEndTimeStart = new Date(dateEndPicker + 'T' + timeStartPicer)
      let dateBetween = []
      while (dateStartTimeStart <= dateEndTimeStart) {
        dateBetween.push([new Date(dateStartTimeStart), new Date(dateStartTimeEnd)])
        dateStartTimeStart.setDate(dateStartTimeStart.getDate() + 1)
        dateStartTimeEnd.setDate(dateStartTimeEnd.getDate() + 1)
      }
      console.log(JSON.stringify(dateBetween))
      this.$emit('HomeSlider_requestingRoutes')
      this.$store.state.ws.send(JSON.stringify(['getMultipleDaysRouteTraffic', this.route, dateBetween]))
      this.$store.state.ws.onmessage = function (event) {
        self.geojson_historic_collection = JSON.parse(event.data)
        // initialize local time within geojson_historic_collection
        let local_timestamp
        self.geojson_historic_collection.forEach((item, index) => {
          local_timestamp = new Date(item['crawled_timestamp'])
          // round time. For example: 9:01 will be round to 9:00
          if (local_timestamp.getMinutes() < 30) {
            local_timestamp.setMinutes(0)
            local_timestamp.setSeconds(0)
          }
          else {
            local_timestamp.setMinutes(30)
            local_timestamp.setSeconds(0)
          }
          console.log(local_timestamp)
          item['local_timestamp'] = local_timestamp
          item['averageJammingFacotr'] = self.calculateAverageJammingFactor(item)
        })

        console.log(self.geojson_historic_collection)
        console.log(self.geojson_historic_collection_indices)
        self.historic_slider['data'] = self.geojson_historic_collection.map((item, index) => {
          self.geojson_historic_collection_indices[item.local_timestamp.toLocaleDateString() + ' ' + item.local_timestamp.toLocaleTimeString()] = index
          return item.local_timestamp.toLocaleDateString() + ' ' + item.local_timestamp.toLocaleTimeString()
        })
        self.historic_slider['value'] = self.historic_slider['data'][0]
        let slider = self.$refs['historic_slider_ref']
        slider.refresh()
        self.displaySelectedHistoric(self.historic_slider['value'])
        self.$emit('HomeSlider_finishedQueryingData')
        self.$emit('HomeSlider_displayGeoJson')
        self.calculateAverageJammingFactorForEachTime()
      }
    },
    displaySelectedHistoric(value) {
      let self = this
      console.log(value)
      console.log(self.geojson_historic_collection[self.geojson_historic_collection_indices[value]])
      self.averageJammingFacotr = self.geojson_historic_collection[self.geojson_historic_collection_indices[value]]['averageJammingFacotr']
      this.$emit('HomeSlider_deleteGeoJsonPlot')
      this.$emit('HomeSlider_plotGeoJson', self.geojson_historic_collection[self.geojson_historic_collection_indices[value]]['crawled_batch_id_traffic'])
    },
    calculateAverageJammingFactor(geojson_historic_collection_item) {
      let totalGeometryLength = 0
      geojson_historic_collection_item['crawled_batch_id_traffic']['features'].forEach((item) => { 
        totalGeometryLength += item['geometry']['coordinates'].length
      })
      let averageJammingFacotr = 0
      geojson_historic_collection_item['crawled_batch_id_traffic']['features'].forEach((item) => { 
        averageJammingFacotr += (item['geometry']['coordinates'].length / totalGeometryLength) * item['properties']['CF']['JF']
      })
      return averageJammingFacotr
    },
    calculateAverageJammingFactorForEachTime(){
      let self = this
      let eachTimeData = new Map()
      let currentTime
      self.geojson_historic_collection.forEach((item, index) => {
        currentTime = item['local_timestamp'].toLocaleTimeString()
        if (!eachTimeData.get(currentTime)) {
          eachTimeData.set(currentTime, [item['averageJammingFacotr']])
        }
        else {
          eachTimeData.get(currentTime).push(item['averageJammingFacotr'])
        }
      })
      console.log(eachTimeData)
      let total 
      self.chartData = []
      self.chartLabel = []
      for (let [timePoint, jammingFactorArray] of eachTimeData) {
        self.chartLabel.push(timePoint)
        total = 0
        jammingFactorArray.forEach((JammingFactor) => {
          total += JammingFactor
        })
        self.chartData.push(total / jammingFactorArray.length)
      }
      console.log(self.chartLabel)
      console.log(self.chartData)
      self.chartFinished = true
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

.historic_slider {
  width: 100%;
}
</style>
