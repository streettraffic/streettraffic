import * as types from './mutations_types.js'

// set up websocket connection
const webSocketAddress = 'ws://localhost:8765/'
const ws = new WebSocket(webSocketAddress)

export const getHistoricBatch = function ({ commit }) {
  ws.send(JSON.stringify(['getHistoricBatch']))
  ws.onmessage = function (event) {
    commit(types.GET_HISTORIC_BATCH, JSON.parse(event.data))
  }
}
