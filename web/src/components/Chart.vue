<template>
  <v-card>
    <v-card-row class="green darken-1">
      <v-card-title>
        <span class="white--text">{{chartTitle}}</span>
        <v-spacer></v-spacer>
      </v-card-title>
    </v-card-row>
    <v-card-text>
      <v-card-row height="auto" center>
        <canvas :id="chartId" width="400" height="400"></canvas>
      </v-card-row>
    </v-card-text>
  </v-card>
</template>

<script>
import Chart from 'chart.js'
import colors from 'nice-color-palettes'

export default {
  name: 'Chart',
  data: function () {
    return {
      chart: null   // initiated by mounted, a Chart.js chart
    }
  },
  props: {
    data: {
      type: Object,
      default: () => {}
    },
    chartTitle: {
      type: String
    },
    chartId: {
      type: String
    }
  },
  methods: {
    buildChart(data) {
      let ctx = document.getElementById(this.chartId).getContext('2d')
      if (this.chart) {
        this.chart.destroy()
      }
      this.chart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
          maintainAspectRatio: false,
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
  mounted() {
    console.log('mounted')
    this.buildChart(this.data)
    console.log('finished')
  },
  watch: {
    labels(val) {
      this.buildChart(this.data)
    },
    data(val) {
      console.log(val)
      this.buildChart(this.data)
    }
  }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style lang="scss" scoped>

</style>
