import Vue from 'vue'
import Vuex from 'vuex'
import createLogger from 'vuex/dist/logger'
import * as actions from './actions'
// import * as getters from './getters'
import * as types from './mutations_types.js'

Vue.use(Vuex)

const state = {
  historic_batch: ['A', 'B', 'C']
}

const mutations = {
  [types.GET_HISTORIC_BATCH] (state, historic_batch) {
    state.historic_batch = historic_batch
  }
}

export default new Vuex.Store({
  state,
  mutations,
  actions,
  // getters,
  strict: true,
  plugins: [createLogger()]
})
