from collections import defaultdict
from requests import post
from simplejson import dumps
from wirelesstraitor.observer import Observer
from wirelesstraitor.observable import Observable

class LocationSearcher(Observer):
    """Gets a datadict containing a device mac, bssids and ssids, parses the
        dict and looks up the geolocation of the bssids
    """

    def __init__(self):
        super(LocationSearcher, self).__init__()
        self.locations = defaultdict(dict)
        self.observable = Observable()

        with open('apikey') as f:
            key = f.read().rstrip()

        assert key is not None
        self.parameters = {'key': key}
        self.url = 'https://www.googleapis.com/geolocation/v1/geolocate'

    def __getattr__(self, attr):
        return getattr(self.observable, attr)

    def update(self, *args, **kwargs):
        """If something happened in ProbeRequestParser and we get a data-dict,
            parse it and throw mac, response.json() to Observers
        """

        self.observable.update_observers(self.get_locations(payload = args[0]))

    def get_locations(self, payload):
        """Looks up location for each bssid in data, return mac and
            bssid_location, a dict containing (bssid: location)
        """

        mac = payload[0]
        data = payload[1]

        assert mac is not None
        assert data is not None
        assert isinstance(data, dict)

        if mac not in self.locations.keys():
            self.locations[mac] = {}

        assert isinstance(data['bssids'], set)
        for bssid in data['bssids']:
            ap = {'macAddress': bssid,
                'signalStrength': -10,
                'signalToNoiseRatio': 0
            }
            request = {'wifiAccessPoints': [ap]}
            response = post(self.url, json = request, params = self.parameters)
            location = response.json()['location']
            bssid_location = [bssid, location]
            self.locations[mac] = bssid_location

        return mac, self.locations[mac]
