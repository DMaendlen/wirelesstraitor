#!/usr/bin/python3

from sigint import DeviceBssidMatcher
from requests import post
from json import dumps

class LocationSearcher(Process):
    """Looks up the GPS-coordinates of an AP"""

    def __init__(self):
        """Setup function to make sure we can run a process"""

        super(LocationSearcher, self).__init__()

        with open('apikey') as f:
            self.key = f.read()
        
        self.parameters = {'key': key}
        self.url = 'https://www.googleapis.com/geolocation/v1/geolocate'

        self.locations = {}
        self.matcher = DeviceBssidMatcher

    def run(self):
        self.matcher.start()
        self.get_location(self.matcher.devices)
    
    def get_location(devices):
        """Requests GPS-coordinates from Google's Geolocation db"""

        request = {'considerIp': 'false'}

        for device in devices:
            self.locations[device] = {}
            for bssid in device['bssids']:
                ap = {'macAddress': bssid,
                    'signalStrength': -0,
                    'signalToNoiseRatio': 0}

                request['wifiAccessPoints'] = [ap]
                r = requests.post(url, json = request, params = self.parameters)
                self.locations[device].update(r.json())

