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
import time
from pyicloud import PyiCloudService
from geopy.geocoders import Nominatim
from geoip import geolite2
from geoip import open_database
from geopy.distance import vincenty
from geopy.distance import great_circle
import os
import sys
import time
import mp3play

CONSOLE_LOG = False
DEBUGGING = False
SYRKOMLI = {
    'latitude': 54.503501,
    'longitude': 18.542396
}

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
    adres = location.address
    log("\nLOCATION ADRESS:" + adres)
    # log("\nLOCATION RAW:"+location.address)

    POINT_A = (SYRKOMLI['latitude'], SYRKOMLI['longitude'])
    POINT_B = (location_obj['latitude'], location_obj['longitude'])

    vincentkm = (vincenty(POINT_A, POINT_B).kilometers)
    circlekm = (great_circle(POINT_A, POINT_B).kilometers)
    log("VINCENT KM:" + str(vincentkm))
    log("CIRCLE KM:")
    log(circlekm)

    vincent = (vincenty(POINT_A, POINT_B).meters)
    circle = (great_circle(POINT_A, POINT_B).meters)
    log("\nVINCENT meters:" + str(vincent))
    log("CIRCLE meters:")
    log(circle)
    return {
        'vincent': vincent,
        'circle': circle,
        'adres': adres
    }

#
# def geoip():
#     """
#     ... after downloading the package, you need to import win_inet_pton in \Lib\site-packages\geoip.py and works like a charm.
#     :return:
#     """
#     print "===GEO IP==="
#     print geolite2.lookup_mine()
#     print "LOOKUP"
#     match = geolite2.lookup('46.186.86.99')
#     if match is not None:
#         print match.country
#         print match.continent
#         print match.timezone
#         print match.subdivisions
#         from geoip import open_database
#         with open_database('data/GeoLite2-City.mmdb') as db:
#             match = db.lookup_mine()
#             print 'My IP info:', match
#
# def run():
#     # load_login_data()
#     # api = PyiCloudService(LOGIN_DATA['login'], LOGIN_DATA['pass'])
#
#     if DEBUGGING is True:
#         devices_obj = json.loads(api.devices)
#         log("[api devices:]" + devices_obj)
#         iphone_obj = json.loads(api.iphone)
#         log("[iphone:]" + iphone_obj)
#         location = api.iphone.location()
#         status = api.iphone.status()
#         log("[status:]" + status)
#         log("[location:]" + location)
#         print "EXIT"
#
#     print "DISTANCE TEST"
#     distance_handler(temp_location())

FIRSTRUN = True
COUNTER = 0
LAST_DIST = {}


def alarm(sound):
    SOUNDS_NAMES = [
        '24483^pchick-alarm.mp3',
        '35752^CarAlarmSet.mp3',
        '44216^alarm.mp3',
        '71766^alarm.mp3',
        '86502^alarm.mp3',
        '91540^caralarm.mp3',
        '97744^ALARM.mp3',
    ]

    filename = SOUNDS_NAMES[int(sound)]
    clip = mp3play.load(filename)
    clip.play()
    time.sleep(min(30, clip.seconds()))
    clip.stop()


def sleeper():
    load_login_data()
    api = PyiCloudService(LOGIN_DATA['login'], LOGIN_DATA['pass'])
    global COUNTER, LAST_DIST, FIRSTRUN
    while True:
        COUNTER += 1
        location = api.iphone.location()
        if FIRSTRUN is True:
            LAST_DIST = distance_handler(location)
            FIRSTRUN = False

        CURR_DIST = distance_handler(location)
        ROZNICA = abs(CURR_DIST['vincent'] - LAST_DIST['vincent'])

        # OBJECT IS MOVING FAST!
        if float(ROZNICA) > 100.0:
            print 20 * "---"
            print "\n\n" + 20 * "!X![ROZNICA>100!X!" + "\n\n"
            alarm(2)

        # OBJECT IS NOT MOVING
        if float(ROZNICA) < 5.0:
            print "[", str(COUNTER), "][R<1m][BEZ ZMIAN][ODLEGLOSC:", str(CURR_DIST['vincent']), "ROZNICA:  ", str(
                ROZNICA), "  ]", "   >", CURR_DIST['adres']
            alarm(1)
        else:
            # OBJECT IS APPROACHING
            if CURR_DIST['vincent'] < LAST_DIST['vincent']:

                if float(ROZNICA) < 20.0:
                    alarm(3)
                    print "!PONAD 20 METROW!!!UWAGA[", str(COUNTER), "][R>1m][OBJEKT SIE ZBLIZA!!!!],[ODLEGLOSC:", str(
                        CURR_DIST['vincent']), " [ROZNICA::::>  ", str(ROZNICA), "  ]   >", CURR_DIST['adres'], "\n"
                elif float(ROZNICA) < 30.0:
                    print "\n!!!!!!!!!!!!!! 20- 30 METROW)\nUWAGA[", str(
                        COUNTER), "][R>1m][OBJEKT SIE ZBLIZA!!!!],[ODLEGLOSC:", str(
                        CURR_DIST['vincent']), " [ROZNICA::::>  ", str(ROZNICA), "  ]   >", CURR_DIST['adres']
                    alarm(0)
                else:

                    alarm(4)
                    print "\n\n" + 500 * "!!!" + "\n\n"
                    print "UWAGA PONAD 30M na minute[", str(COUNTER), "][R>1m][OBJEKT SIE ZBLIZA!!!!],[ODLEGLOSC:", str(
                        CURR_DIST['vincent']), " [ROZNICA::::>  ", str(ROZNICA), "  ]   >", CURR_DIST['adres']

                # UNDER 2000 METER
                if CURR_DIST['vincent'] < 2000:
                    alarm(6)
                    print "\n MNIEJ NIZ 2 KM ZOSTALO!!!!\n"

            # OBJECT IS MOVING AWAY!
            else:
                print "UWAGA[", str(COUNTER), "][R>1m][OBJEKT SIE ODDALA!][ODLEGLOSC:", str(
                    CURR_DIST['vincent']), "  [ROZNICA:  ", str(ROZNICA), "  ]   >", CURR_DIST['adres']
                alarm(5)

        time.sleep(60)
        LAST_DIST = CURR_DIST

# run()
# geoip()
sleeper()
