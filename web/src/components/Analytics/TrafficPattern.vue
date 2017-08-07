<template lang="pug">
  v-layout(row wrap)
    v-flex.my-3(xs8)
      h6 StreetTraffic Traffic Pattern
      p
        | In this section, you can pick a date at the calendar below and the site will generate a graph of average jamming factor of the city you are monitoring
      p Now pick a city that we monitored
      v-select.input-group--focused(v-bind:items='analytics_monitored_area_description_collection' v-model='selected_area_description' label='Select')
    
    chart(:data='quantileData' :chartTitle="'Quantile'" chartId='quantile')

    v-flex.ma-3(xs12 md5)
      h6 Pick a date here to see traffic patterns
      v-date-picker(v-model='datePicker')
      div(v-show='true') {{datePicked}}

    chart(:data='meanData' :chartTitle="'Mean and Standard Deviation'" chartId='mean').mt-5
</template>

<script>
import Chart from '../Chart.vue'
import colors from 'nice-color-palettes'

// Load module after Highcharts is loaded

export default {
  name: 'Analytics',
  components: {
    Chart
  },
  data: function () {
    return {
      selected_area_description: null,
      analytics_monitored_area_description_collection: [],
      datePicker: null,
      quantileData: {
        labels: [],
        datasets: [{
          label: 'Jamming Factor',
          data: [],
          borderColor: '#3498db',
          fill: false
        }]
      },
      meanData: {
        labels: [],
        datasets: [{
          label: 'Jamming Factor',
          data: [],
          borderColor: '#3498db',
          fill: false
        }]
      }
    }
  },
  methods: {
    getTrafficPattern(datePicker) {
      /*
        inputs: datePicker: str
        example inputs:
        datePicker = '2017-5-23'

        This funciton will request the traffic pattern of this date from '2017-5-23 0:00' to '2017-5-23 23:59'
        with respect to local time. Then use the traffic pattern data to build a chart
      */
      let self = this
      let day_start = new Date(this.datePicker + 'T00:00')
      let day_end = new Date(this.datePicker + 'T23:59')
      console.log(day_start)
      this.$store.state.ws.send(JSON.stringify(['getTrafficPattern', day_start.toISOString(), day_end.toISOString(), this.selected_area_description]))
      this.$store.state.ws.onmessage = function(event) {
        let traffic_pattern = JSON.parse(event.data)
        console.log(traffic_pattern)
        let labels = traffic_pattern.map((item) => {
          return new Date(item.crawled_timestamp).toLocaleTimeString()
        })
        self.createMeanAndStandardDeviation(traffic_pattern, labels)
        self.createQuantile(traffic_pattern, labels, 0.90, 0.50, 0.10)
      }
    },
    createMeanAndStandardDeviation(traffic_pattern, labels) {
      let data = traffic_pattern.map((item) => item.average_JF)
      let upper = traffic_pattern.map((item) => item.average_JF + item.standard_deviation_JF)
      let lower = traffic_pattern.map((item) => item.average_JF - item.standard_deviation_JF)
      this.meanData = {
        labels: labels,
        datasets: [{
          label: 'Jamming Factor',
          data: data,
          borderColor: '#3498db',
          fill: false
        },
        {
          label: 'Error upper',
          data: upper,
          borderColor: '#FF5733',
          fill: false
        },
        {
          label: 'Error lower',
          data: lower,
          borderColor: '#FF5733',
          fill: false
        }]
      }
    },
    createQuantile(traffic_pattern, labels, percentile1, percentile2, percentile3) {
      let upper = traffic_pattern.map((item) => item['JF_collection'][Math.floor(percentile1 * item['JF_collection'].length)])
      let middle = traffic_pattern.map((item) => item['JF_collection'][Math.floor(percentile2 * item['JF_collection'].length)])
      let lower = traffic_pattern.map((item) => item['JF_collection'][Math.floor(percentile3 * item['JF_collection'].length)])
      this.quantileData = {
        labels: labels,
        datasets: [{
          label: (percentile1 * 100).toFixed(1) + '%',
          data: upper,
          borderColor: '#FF5733',
          fill: false
        },
        {
          label: (percentile2 * 100).toFixed(1) + '%',
          data: middle,
          borderColor: '#3498db',
          fill: false
        },
        {
          label: (percentile3 * 100).toFixed(1) + '%',
          data: lower,
          borderColor: '#FF5733',
          fill: false
        }]
      }
    }
  },
  computed: {
    datePicked() {
      if (!this.datePicker){
        return null
      }
      else {
        this.getTrafficPattern()
        return this.datePicker
      }
    }
  },
  mounted() {
    let self = this
    this.$store.state.ws.send(JSON.stringify(['getAnalyticsMonitoredAreaDescriptionCollection']))
    this.$store.state.ws.onmessage = function (event) {
      self.analytics_monitored_area_description_collection = JSON.parse(event.data)
      console.log(self.analytics_monitored_area_description_collection)
    }
  }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style lang="scss" scoped>

</style>
