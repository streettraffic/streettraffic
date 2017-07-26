<template lang="pug">
  v-layout(row wrap)
    v-flex(xs8).my-3
      h6 Run the traffic crawler
      p 
        | congrats! You probably have haved register some routes or cities to crawl, now it's
        | time to run the crawler! There are two ways to run the crawler...
      
</template>

<script>
// import custom components

export default {
  name: 'RunCrawler',
  methods: {
    runCrawler() {
      this.$store.state.ws.send(JSON.stringify(['runCrawler']))
      this.$store.state.ws.onmessage = function (event) { }
    }
  }
}
</script>
