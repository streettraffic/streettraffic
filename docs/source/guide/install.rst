Installation
=========================================

Basically, there are three things you need to get the package running:

* Install StreetTraffic package
* Install RethinkDB server (really easy to setup)
* Acquire credentials at `HERE.com <https://developer.here.com/plans>`_


Install StreetTraffic package
-----------------------------

StreetTraffic is published at `PyPI <https://pypi.org/project/streettraffic/>`_
and can therefore be installed through ``pip``. ::

    pip install streettraffic

**Requirements**: StreetTraffic runs on Python 3.6+ because it uses
``async, await`` syntax and `PEP526 <https://www.python.org/dev/peps/pep-0526/>`_
variable annotation, which are both not supported by Python 3.5 or lower.
If you don't have a Python 3.6+ installed, I highly recommend you to install
`Anaconda Python <https://www.continuum.io/downloads>`_, which inlcudes
many standard and popular python libraries.

Install RethinkDB server
--------------------------

Please don't get intimidated by it. RethinkDB server has the one of the easiest instructions to 
setup. Simply follow their documentation on `Install RethinkDB <https://rethinkdb.com/docs/install/>`_
and you will be ok.


Acquire credentials at `HERE.com <https://developer.here.com/plans>`_
-----------------------------------------------------------------------

You need to register an account at `HERE.com <https://developer.here.com/plans>`_. Their 
BASIC plan is **free** and you can get 15K API requests per month. Follow their procedure
and generate a ``App ID`` and ``App Code``.

Now you are ready to run our hello world!