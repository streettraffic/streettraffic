<template>
  <div>
    <v-data-table
      v-bind:headers="headers"
      v-bind:items="historic_batch"
      v-model="selected"
      selected-key="crawled_batch_id"
      select-all
    >
      <template slot="headers" scope="props">
        <span v-tooltip:bottom="{ 'html': props.item.text }">
          {{ props.item.text }}
        </span>
      </template>
      <template slot="items" scope="props">
        <td>
          <v-checkbox
            primary
            hide-details
            v-model="props.selected"
          ></v-checkbox>
        </td>
        <td>{{ props.item.crawled_batch_id }}</td>
        <td  class="text-xs-right">{{ props.item.crawled_timestamp }}</td>
      </template>
    </v-data-table>
    <v-btn dark default @click.native="getSelectedBatchList">Submit</v-btn>
  </div>
</template>

<script>
export default {
  name: 'HistoricBatch',
  data () {
    return {
      selected: [],
      headers: [
        {
          text: 'crawled_batch_id',
          left: true,
          sortable: false,
          value: 'name'
        },
        { text: 'crawled_timestamp', sortable: false, value: 'calories' }
      ]
    }
  },
  methods: {
    getLocation() {
      let self = this
      this.$store.state.ws.send(JSON.stringify(['getRoadData', this.location, 10000, 10]))
      this.$store.state.ws.onmessage = function (event) {
        self.plotGeoJson(JSON.parse(event.data))
      }
    },
    getSelectedBatch() {
      let self = this
      this.$store.state.ws.send(JSON.stringify(['getSelectedBatch', this.route, this.selected_batch]))
      this.$store.state.ws.onmessage = function (event) {
        console.log(JSON.parse(event.data))
        self.plotGeoJson(JSON.parse(event.data))
      }
    },
    getSelectedBatchList() {
      let self = this
      this.$store.state.ws.send(JSON.stringify(['getSelectedBatchList', this.route, this.selected]))
      this.$store.state.ws.onmessage = function (event) {
        console.log(JSON.parse(event.data))
        self.geojson_historic_collection = JSON.parse(event.data)
        self.historic_slider['data'] = self.geojson_historic_collection
        self.historic_slider['value'] = self.historic_slider['data'][0]
      }
    },
    displaySelectedHistoric(value) {
      let self = this
      console.log(value)
      console.log(self.geojson_historic_collection[self.geojson_historic_collection_indices[value]])
      self.averageJammingFacotr = self.geojson_historic_collection[self.geojson_historic_collection_indices[value]]['averageJammingFacotr']
      this.deleteGeoJsonPlot()
      self.plotGeoJson(self.geojson_historic_collection[self.geojson_historic_collection_indices[value]]['crawled_batch_id_traffic'])
    },
    getMultipleDaysRouteTraffic() {
      /* reference
          https://stackoverflow.com/questions/18109481/get-all-the-dates-that-fall-between-two-dates
      */
      let self = this
      self.trafficInfoSliderShow = true
      let dateStartTimeStart = new Date(this.dateStartPicker + 'T' + this.timeStartPicer)
      let dateStartTimeEnd = new Date(this.dateStartPicker + 'T' + this.timeEndPicer)
      let dateEndTimeStart = new Date(this.dateEndPicker + 'T' + this.timeStartPicer)
      let dateBetween = []
      while (dateStartTimeStart <= dateEndTimeStart) {
        dateBetween.push([new Date(dateStartTimeStart), new Date(dateStartTimeEnd)])
        dateStartTimeStart.setDate(dateStartTimeStart.getDate() + 1)
        dateStartTimeEnd.setDate(dateStartTimeEnd.getDate() + 1)
      }
      console.log(JSON.stringify(dateBetween))
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
        self.trafficInfoSliderDialog = false
        self.displayGeoJson()
      }
    },
    toManhattan() {
      this.center = {lat: 40.725306, lng: -73.988913}
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
    },
    test(){
      /* eslint-disable */
      // this.calculateAverageJammingFactorForEachTime()
      this.directionsDisplay.setMap(null)
      /* eslint-enable */
    },
    getDateBetween(startDate, endDate){
      // pass
    },
    plotGeoJson(geoJsonData) {
      /* input: geoJsonData(a geojson json object)

         This fucntion add the geoJson data to the google map object
      */
      /* eslint-disable */
      // this.geojson_data = new google.maps.Data()
      // this.geojson_data.addGeoJson(geoJsonData)
      // this.geojson_data.setMap(this.$refs.mymap.$mapObject)
      // this.geojson_data.setStyle(function(feature) {
      //   return ({
      //     strokeColor: feature.getProperty('color'),
      //     strokeWeight: 2
      //   })
      // })
      let self = this
      self.$refs.mymap.$mapObject.data.addGeoJson(geoJsonData)
      self.$refs.mymap.$mapObject.data.setStyle(function(feature) {
        return ({
          strokeColor: feature.getProperty('color'),
          strokeWeight: 2,
          zIndex: 5
        })
      })
      this.displayGeoJson()
      /* eslint-enable */
    },
    deleteGeoJsonPlot() {
      /*  inputs: None
          This funciton clears the geojson plotting in the google maps
          return None
      */
      // this.geojson_data.setMap(null)
      // this.geojson_data = null
      let self = this
      self.$refs.mymap.$mapObject.data.forEach(function (feature) {
        self.$refs.mymap.$mapObject.data.remove(feature)
      })
      this.displayGeoJson()
    },
    displayGeoJson() {
      let results
      this.$refs.mymap.$mapObject.data.toGeoJson((geojson) => {
        results = JSON.stringify(geojson, null, 2)
      })
      this.map_geojson = results
    },
    dsiplayRouting() {
      /* eslint-disable */
      console.log(google)
      this.directionsDisplay = new google.maps.DirectionsRenderer()
      this.directionsService = new google.maps.DirectionsService()
      this.directionsDisplay.setMap(this.$refs.mymap.$mapObject)
      this.calculateAndDisplayRoute()
      /* eslint-enable */
    },
    dsiplayRoutingCaseStudy() {
      /* eslint-disable */
      console.log(google)
      this.directionsDisplay = new google.maps.DirectionsRenderer()
      this.directionsService = new google.maps.DirectionsService()
      this.directionsDisplay.setMap(this.$refs.mymap.$mapObject)
      this.calculateAndDisplayRouteCaseStudy()
      /* eslint-enable */
    },
    getHistoric (){
      let self = this
      this.$store.state.ws.send(JSON.stringify(['getHistoric', this.route]))
      this.$store.state.ws.onmessage = function (event) {
        console.log(JSON.parse(event.data))
        self.plotGeoJson(JSON.parse(event.data))
      }
    },
    calculateAndDisplayRoute() {
      let self = this
      /* eslint-disable */
      self.directionsService.route({
        origin: {lat: 33.736818, lng: -84.394652},  // Haight
        destination: {lat: 33.769922, lng: -84.377616},  // Ocean Beach
        // Note that Javascript allows us to access the constant
        // using square brackets and a string value as its
        // "property."
        travelMode: google.maps.TravelMode['DRIVING']     // There are multiple travel mode such as biking walking
      }, function(response, status) {
        if (status == 'OK') {
          self.route = response
          self.directionsDisplay.setDirections(response)
        } else {
          window.alert('Directions request failed due to ' + status)
        }
      })
      /* eslint-enable */
    },
    calculateAndDisplayRouteCaseStudy() {
      let self = this
      /* eslint-disable */
      self.route = CaseStudyDirection
      self.directionsDisplay.setDirections(CaseStudyDirection)
      /* eslint-enable */
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
