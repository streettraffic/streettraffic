class TrafficDataConn {

  constructor(webSocketAddress) {
    // connection and server settings
    this.webSocketAddress = webSocketAddress
    this.ws = null  // will be initiated in startConnection()

    // data section
    this.historic_batch = null

    // finally start setting up connections
  }

  getHistoricBatch(){
    `
    This function makes the connection to TrafficServer and ask for historic_batch information, which is 
    a collection of crawled_batch information
    `
    let self = this
    self.ws = new WebSocket(this.webSocketAddress)
    self.ws.onopen = function (){
      self.ws.send(JSON.stringify(['getHistoricBatch']))
    }
    self.ws.onmessage = function (event) {
      console.log(JSON.parse(event.data))
      self.historic_batch = JSON.parse(event.data)
    }
  }
}

export default new TrafficDataConn('ws://localhost:8765/')
