==============
ziptimezone
==============


..
    Note: can't include the badges file from the docs here, as it won't render on PyPI -> sync manually

.. image:: https://readthedocs.org/projects/ziptimezone/badge/?version=latest
    :alt: documentation status
    :target: https://ziptimezone.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/pypi/wheel/ziptimezone.svg
    :target: https://pypi.python.org/pypi/ziptimezone

.. image:: https://pepy.tech/badge/ziptimezone
    :alt: total PyPI downloads
    :target: https://pepy.tech/project/ziptimezone

.. image:: https://img.shields.io/pypi/v/ziptimezone.svg
    :alt: latest version on PyPI
    :target: https://pypi.python.org/pypi/ziptimezone

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black


This is a python package with US Zip Code convenience functions such as those listed in the examples below. 
It uses the geonames data, coupled with the timezonefinder package. It uses a mapping of the popular 
timezone regions in US, and returns the outputs accordingly. Latest release includes dependency fixes and 
documentation updates.


Quick Guide:

.. code-block:: console

    pip install ziptimezone


.. code-block:: python

    import ziptimezone as zpt

    # returns a tuple (42.377, -71.1256)
    zpt.get_lat_long_for_zip('02138')

    # returns 'Eastern' the timezone has been reduced to the more popular zones 
    # for United States Regions
    zpt.get_timezone_by_zip('02138') 

    # returns a dictionary, {'02138': 'Eastern', '85260': 'Mountain'}
    zpt.get_timezone_for_many_zips(['02138', '85260']) 

    # returns a string, '02138 is ahead of 72201 by 1.00 hours."}
    zpt.calculate_time_difference(['02138', '72201']) 

    # returns a dictionary, for 5/30/24 {'sunrise_time': '05:11:13', 'sunset_time': '20:13:31'}
    today_sun_times = get_sunrise_sunset("02138")

    # Get sunrise and sunset times for ZIP code 02138 on July 4, 2024
    # will return {'sunrise_time': '05:13:42', 'sunset_time': '20:24:10'}
    july4_sun_times = get_sunrise_sunset("02138", datetime(2024, 7, 4).date())

For more refer to the `Documentation <https://ziptimezone.readthedocs.io/en/latest/>`__.

Also check:

`PyPI <https://pypi.python.org/pypi/ziptimezone/>`__
