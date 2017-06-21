class TrafficDataConn {
    constructor(webSocketAddress) {
        this.webSocketAddress = webSocketAddress
        this.msgQueue = []
        this.ws = new WebSocket(this.webSocketAddress)
    }
}

export default new TrafficDataConn()