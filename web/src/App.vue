<template lang="pug">
  v-app
    transition(name="slide" mode="out-in")
      router-view
</template>

<script>

export default {
  created() {
    this.$store.dispatch('setWsConnection')
  }
}
</script>

<style lang="scss">
.slide-enter-active, .slide-enter {
  transition: all .3s ease
}
  
.slide-enter, .slide-leave-to{
  opacity: 0
}
  
.slide-enter{
  transform: translateX(-3rem)
}
  
.slide-leave, .slide-leave-active{
  transition: all .4s ease
}
  
.slide-leave-to{
  transform: translateX(3rem)
}

</style>
