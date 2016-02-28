#!/usr/bin/env python
# -*- coding: utf8 -*-
# __author__ = 'M.Frackowiak'
"""
DISTANCE CHECKER BETWEEN DEVICE AND SELECTED POINT via ICLOUD SERVICE


DO ZAIMPLEMTOWANIA
-https://pypi.python.org/pypi/geolocation-python/0.2.2


"""
from __future__ import absolute_import
import json

from pyicloud import PyiCloudService
from geopy.geocoders import Nominatim
from geoip import geolite2
from geoip import open_database

CONSOLE_LOG = True
DEBUGGING = False


def log(text):
    if CONSOLE_LOG is True:
        print text


LOGIN_DATA = {
    'login': '',
    'pass': ''
}


def load_login_data():
    fo = open('login', 'r').read().split(":")
    LOGIN_DATA['login'] = fo[0]
    LOGIN_DATA['pass'] = fo[1]
    print "LOADED ICLOUD PROFILE: ", LOGIN_DATA['login'], ":", LOGIN_DATA['pass']


OUTPUT = """
[api devices:]
 {
    u'Zi9cVH+SMYWAwGV2THGyIEERj4nJLVqnxKDC5qqB6P0KX0GIuayEQOHYVNSUzmWV': <AppleDevice(iPhone 6: Tamcia )>
 }
---------------------------------------------------------
[api iphone:]
iPhone 6: Tamcia
---------------------------------------------------------
[api.iphone.location():]
 {
    u'timeStamp': 1456687186509L,
    u'locationFinished': True,
    u'longitude': 18.5679437779063,
    u'positionType': u'GPS',
    u'locationType': None,
    u'latitude': 54.4446849078447,
    u'isOld': False,
    u'isInaccurate': False,
    u'horizontalAccuracy': 50.0
 }
---------------------------------------------------------
[api.iphone.status():]
 {
    'deviceDisplayName': u'iPhone 6',
    'deviceStatus': u'201',
    'batteryLevel': 0.76,
    'name': u'Tamcia '
 }
"""


def temp_location():
    return {
        'timeStamp': 1456687186509L,
        'locationFinished': True,
        'longitude': 18.5679437779063,
        'positionType': u'GPS',
        'locationType': None,
        'latitude': 54.4446849078447,
        'isOld': False,
        'isInaccurate': False,
        'horizontalAccuracy': 50.0
    }


def temp_status():
    return {
        'deviceDisplayName': u'iPhone 6',
        'deviceStatus': u'201',
        'batteryLevel': 0.76,
        'name': u'Tamcia '
    }


def distance_handler(location_obj):
    geolocator = Nominatim()
    input_data=str(location_obj['latitude'])+", "+str(location_obj['longitude'])
    log("[Input location str:" + input_data)
    location = geolocator.reverse(input_data)
    log("\nLOCATION ADRESS:"+location.address)
    log("\nLOCATION RAW:"+location.address)

#     Here's an example usage of Vincenty distance:
#
# >>> from geopy.distance import vincenty
# >>> newport_ri = (41.49008, -71.312796)
# >>> cleveland_oh = (41.499498, -81.695391)
# >>> print(vincenty(newport_ri, cleveland_oh).miles)
# 538.3904451566326
# Using great-circle distance:
#
# >>> from geopy.distance import great_circle
# >>> newport_ri = (41.49008, -71.312796)
# >>> cleveland_oh = (41.499498, -81.695391)
# >>> print(great_circle(newport_ri, cleveland_oh).miles)
# 537.1485284062816


def geoip():
    """
    ... after downloading the package, you need to import win_inet_pton in \Lib\site-packages\geoip.py and works like a charm.
    :return:

    """
    print "===GEO IP==="
    print geolite2.lookup_mine()
    print "LOOKUP"

    match = geolite2.lookup('46.186.86.99')
    if match is not None:

        print match.country
        print match.continent
        print match.timezone
        print match.subdivisions

def run():
    load_login_data()
    api = PyiCloudService(LOGIN_DATA['login'], LOGIN_DATA['pass'])

    if DEBUGGING is True:
        devices_obj = json.loads(api.devices)
        log("[api devices:]" + devices_obj)
        iphone_obj = json.loads(api.iphone)
        log("[iphone:]" + iphone_obj)
        location = api.iphone.location()
        status = api.iphone.status()
        log("[status:]" + status)
        log("[location:]" + location)
        print "EXIT"

    print "DISTANCE TEST"
    distance_handler(temp_location())



 # \Lib\site-packages\geoip.py
# run()
geoip()