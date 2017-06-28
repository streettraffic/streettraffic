<template>
  <v-layout row wrap>
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
      <h6>Pick a date here to see traffic pattern</h6>
      <v-date-picker v-model="datePicker"></v-date-picker>
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
      datePicker: null
    }
  },
  methods: {
    getRandomColor() {
      let letters = '0123456789ABCDEF'.split('')
      let color = '#'
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)]
      }
      return color
    }
  },
  mounted() {
    var ctx = document.getElementById('myChart').getContext('2d')
    var myChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
          label: '# of Votes',
          data: [12, 19, 3, 5, 2, 3],
          backgroundColor: colors[0].concat(colors[1]),
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
  },
  created() {
    console.log(this)
  }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style lang="scss" scoped>

</style>
