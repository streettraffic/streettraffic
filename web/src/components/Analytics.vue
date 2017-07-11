<template>
  <v-layout row wrap>
    <v-flex xs8 class="my-3">
      <h6>Histraffic Analytics section</h6>
      <p>In this section, you can pick a date at the calendar below and the site will generate a graph of average jamming factor of the city you are monitoring</p>
    </v-flex>
    <v-flex xs12 md6>
      <v-card>
        <v-card-row class="green darken-1">
          <v-card-title>
            <span class="white--text">Analytics</span>
            <v-spacer></v-spacer>
          </v-card-title>
        </v-card-row>
        <v-card-text>
          <v-card-row height="auto" center>
            <canvas id="myChart" width="400" height="400"></canvas>
          </v-card-row>
        </v-card-text>
      </v-card>
    </v-flex>
    <v-flex xs12 md5 class="ma-3">
      <h6>Pick a date here to see traffic patterns</h6>
      <v-date-picker v-model="datePicker"></v-date-picker>
      <div v-show="true">{{datePicked}}</div>
    </v-flex>
  </v-layout>
</template>

<script>
import Chart from 'chart.js'
import colors from 'nice-color-palettes'

// Load module after Highcharts is loaded

export default {
  name: 'Analytics',
  data: function () {
    return {
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
      this.$store.state.ws.send(JSON.stringify(['getTrafficPattern', day_start.toISOString(), day_end.toISOString()]))
      this.$store.state.ws.onmessage = function(event) {
        let traffic_pattern = JSON.parse(event.data)
        let time = null
        self.buildChart(traffic_pattern.map((item) => { time = new Date(item.crawled_timestamp)
          return time.getHours() }),
          traffic_pattern.map((item) => item.average_JF))
      }
    },
    buildChart(labels, data) {
      let ctx = document.getElementById('myChart').getContext('2d')
      if (this.chart) {
        this.chart.destroy()
      }
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Jamming Factor',
            data: data,
            backgroundColor: colors[0].concat(colors[1]).concat(colors[2]).concat(colors[3]).concat(colors[4]).concat(colors[5]).concat(colors[6]).concat(colors[7]),
            borderWidth: 1
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
    this.buildChart([], [])
  },
  created() {
    // pass
  }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style lang="scss" scoped>

</style>
