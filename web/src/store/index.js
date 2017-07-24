import Vue from 'vue'
import Vuex from 'vuex'
import createLogger from 'vuex/dist/logger'
import * as actions from './actions'
// import * as getters from './getters'
import * as types from './mutations_types.js'

Vue.use(Vuex)

const state = {
  ws_connection_status: false,
  ws_address: 'ws://localhost:8765/',
  ws: null,
  historic_batch: ['A', 'B', 'C']
}

const mutations = {
  [types.SET_WS_CONNECTION_STATUS] (state, ws) {
    state.ws = ws
    state.ws_connection_status = true
  },
  [types.GET_HISTORIC_BATCH] (state, historic_batch) {
    state.historic_batch = historic_batch
  }
}

export default new Vuex.Store({
  state,
  mutations,
  actions,
  // getters,
  strict: true
})
