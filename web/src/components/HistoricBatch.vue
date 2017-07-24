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
