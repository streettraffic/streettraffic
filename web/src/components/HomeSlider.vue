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