import * as types from './mutations_types.js'

// set up websocket connection

export const setWsConnection = function ({ commit, state, dispatch }) {
  let temp_ws = new WebSocket(state.ws_address)
  temp_ws.onopen = function () {
    commit(types.SET_WS_CONNECTION_STATUS, temp_ws)
    dispatch('getHistoricBatch')
  }
}

export const getHistoricBatch = function ({ commit, state }) {
  state.ws.send(JSON.stringify(['getHistoricBatch']))
  state.ws.onmessage = function (event) {
    commit(types.GET_HISTORIC_BATCH, JSON.parse(event.data))
  }
}
