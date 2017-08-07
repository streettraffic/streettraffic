<template lang="pug">
  v-flex.my-3(xs8)
    h6 StreetTraffic History Batch Section
    p
      | In this section, you can see the data you have collected
    v-divider.my-4
    div
      v-data-table(v-bind:headers='headers' v-bind:items='historic_batch' v-model='selected' selected-key='crawled_batch_id' select-all='')
        template(slot='headers', scope='props')
          span(v-tooltip:bottom="{ 'html': props.item.text }")
            | {{ props.item.text }}
        template(slot='items' scope='props')
          td
            v-checkbox(primary hide-details v-model='props.selected')
          td {{ props.item.crawled_batch_id }}
          td.text-xs-right {{ props.item.crawled_timestamp }}
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
  computed: {
    historic_batch() {
      return this.$store.state.historic_batch
    }
  }
}
</script>
