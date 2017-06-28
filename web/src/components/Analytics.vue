<template>
  <v-layout>
    <v-flex xs12>
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
  </v-layout>
</template>

<script>
/* eslint-disable */
import Chart from 'chart.js'
import colors from 'nice-color-palettes'
console.log(colors[0])

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
          }
      }
  },
  methods: {
    getRandomColor() {
      let letters = '0123456789ABCDEF'.split('')
      let color = '#'
      for (let i = 0; i < 6; i++ ) {
          color += letters[Math.floor(Math.random() * 16)]
      }
      return color
    }
  },
  mounted() {
    var ctx = document.getElementById("myChart").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: colors[0].concat(colors[1]),
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
  }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style lang="scss" scoped>

</style>
