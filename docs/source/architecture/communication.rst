Communication between Back-end and Front-end
===================================================

We used a websocket server to communicate the back-end 
and the front-end. The front end Javascript would establish a connection and 
send a message to the back-end in the following format
::

    JSON.stringify(['instruction_name', parameters1, ..., parametersN])

and the ``server.py`` would need to define what it should do if ``message[0] == 'instruction_name'``

For example:

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
        <title>test</title>
    </head>
    <body>
        This is testing websocket connection to the server and call a function
        <script type="text/javascript">
            // Create WebSocket connection.
            const socket = new WebSocket('ws://localhost:8765');

            // Connection opened
            socket.addEventListener('open', function (event) {
                console.log('connection opened')
                socket.send(JSON.stringify(['getRoadData', {lat: 33.760035, lng: -84.379316}, 10000, 10]));
            });

            // Listen for messages
            socket.addEventListener('message', function (event) {
                console.log('Message from server ', event.data);
            });
        </script>
    </body>
    </html>

And ``server.py`` knows what to do if the ``message[0] == "getRoadData"``
(in this case, ``message = ['getRoadData', {lat: 33.760035, lng: -84.379316}, 10000, 10]``)
::

    async def consumer_handler(self, websocket):
        while True:
            try:
                message = await websocket.recv()
                # print("received", message)
                message = json.loads(message)

                ......

                elif message[0] == "getRoadData":
                    data = self.traffic_data.get_nearest_road(location_data = (message[1]['lat'], message[1]['lng']), max_dist = message[2])
                    distance = data['dist']  # did not used, maybe used later
                    road_data_id = data['doc']['road_data_id']
                    road_data_geojson = self.traffic_data.fetch_geojson_item(road_data_id)
                    await websocket.send(json.dumps(road_data_geojson))
                    print('sent data')

and now if we open the html in the browser, we would see the following result
if we have traffic flow data around ``{lat: 33.760035, lng: -84.379316}``

.. image:: wrapper.png
    :alt: wrapper

For more detailed information, please refer to the **source code** of
:meth:`streettraffic.server.TrafficServer`