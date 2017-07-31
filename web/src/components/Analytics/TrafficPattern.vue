<template lang="pug">
  v-layout(row wrap)
    v-flex.my-3(xs8)
      h6 StreetTraffic Traffic Pattern
      p
        | In this section, you can pick a date at the calendar below and the site will generate a graph of average jamming factor of the city you are monitoring
      p Now pick a city that we monitored
      v-select.input-group--focused(v-bind:items='analytics_monitored_area_description_collection' v-model='selected_area_description' label='Select')
    v-flex(xs12 md6)
      v-card
        v-card-row.green.darken-1
          v-card-title
            span.white--text Quartile
            v-spacer
        v-card-text
          v-card-row(height='auto' center)
            canvas#quartile(width='400' height='400')
    v-flex.ma-3(xs12 md5)
      h6 Pick a date here to see traffic patterns
      v-date-picker(v-model='datePicker')
      div(v-show='true') {{datePicked}}
    
    
    v-flex(xs12 md6).mt-5
      v-card
        v-card-row.green.darken-1
          v-card-title
            span.white--text Mean and Standard Deviation
            v-spacer
        v-card-text
          v-card-row(height='auto' center)
            canvas#std(width='400' height='400')
</template>

<script>
import Chart from 'chart.js'
import colors from 'nice-color-palettes'

// Load module after Highcharts is loaded

export default {
  name: 'Analytics',
  data: function () {
    return {
      selected_area_description: null,
      analytics_monitored_area_description_collection: [],
      data: {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        series: [
            [12, 9, 7, 8, 5],
            [2, 1, 3.5, 7, 3],
            [1, 3, 4, 5, 6]
        ]
      },
      options: {
        fullWidth: true,
        chartPadding: {
          right: 40
        }
      },
      datePicker: null,
      chart: null   // initiated by mounted, a Chart.js chart
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
        let data = traffic_pattern.map((item) => item.average_JF)
        let upper = traffic_pattern.map((item) => item.average_JF + item.standard_deviation_JF)
        let lower = traffic_pattern.map((item) => item.average_JF - item.standard_deviation_JF)
        self.buildChart('std', labels, data, upper, lower)
      }
    },
    buildChart(id, labels, data, upper, lower) {
      let ctx = document.getElementById(id).getContext('2d')
      if (this.chart) {
        this.chart.destroy()
      }
      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
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
        },
        options: {
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true
              }
            }]
          }
        }
      })
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
    this.buildChart('std', [], [])
    this.buildChart('quartile', [], [])
  }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style lang="scss" scoped>

</style>
