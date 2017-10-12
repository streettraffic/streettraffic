.. title:: StreetTraffic Package

.. image:: https://api.codacy.com/project/badge/Grade/adacea14777f4fa2b8df5584b1c44823    :target: https://www.codacy.com/app/vwxyzjn/streettraffic?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=streettraffic/streettraffic&amp;utm_campaign=Badge_Grade

StreetTraffic Package
=======================

StreetTraffic is a Python package that crawls the traffic flow data of
your favorite routes, cities by using the API provided by  
`HERE.com <https://developer.here.com/rest-apis/documentation/traffic/topics/quick-start.html>`_

StreetTraffic also provides a front end Web UI to visualize historical traffic data
by utilizing `Vuejs <https://vuejs.org/>`_ and `Vuetify <https://vuetifyjs.com/>`_


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
