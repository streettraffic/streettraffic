.. title:: StreetTraffic Package

StreetTraffic Package
=======================

StreetTraffic is a Python package that monitors the traffic flow data of
your favorite routes, cities and more. By using the API provided by  
`HERE.com <https://developer.here.com/rest-apis/documentation/traffic/topics/quick-start.html>`_
, we are able to crawl the traffic data of areas of interest. Then
by utilizing `Vuejs <https://vuejs.org/>`_ and `Vuetify <https://vuetifyjs.com/>`_, we built a front 
end Web UI to visualize historical traffic data and more.


`Read Documentation <https://streettraffic.github.io/docs/docindex.html>`_

Visualize traffic flow history
------------------------------------

After crawling data of some regions or routes, you may query the historical
traffic flow of a given route from the Web UI

.. image:: docs\source\_static\traffic_slider.gif
    :alt: traffic_slider

Query the traffic pattern of a region
-----------------------------------------

You may sample many roads within a given region and calculate
the average jamming factor(a measurement of traffic flow) of those roads

.. image:: docs\source\_static\TrafficPattern.gif
    :alt: TrafficPattern


Directly interact with database
--------------------------------------------
StreetTraffic uses RethinkDB as its datastore, which
is very easy to setup and do queries.

.. image:: docs\source\_static\RethinkDB.gif
    :alt: RethinkDB
