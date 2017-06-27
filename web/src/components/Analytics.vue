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
            <div id="container" style="width:100%; height:400px;"></div>
          </v-card-row>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
/* eslint-disable */
var Highcharts = require('highcharts')

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
  created() {
    var myChart = Highcharts.chart('container', {
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Fruit Consumption'
        },
        xAxis: {
            categories: ['Apples', 'Bananas', 'Oranges']
        },
        yAxis: {
            title: {
                text: 'Fruit eaten'
            }
        },
        series: [{
            name: 'Jane',
            data: [1, 0, 4]
        }, {
            name: 'John',
            data: [5, 7, 3]
        }]
    });
  }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style lang="scss" scoped>

</style>
