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

        self.observable.update_observers(self.get_location(payload = args[0]))

    def get_location(self, payload):
        """Looks up location for each bssid in data, return mac and
            bssid_location, a list containing (bssid, ssid, location)
        """

        mac = payload[0]
        data = payload[1]

        assert mac is not None
        assert data is not None
        assert isinstance(data, list), "data: {type_}, {data}".format(type_ = type(data), data = data)

        if mac not in self.locations.keys():
            self.locations[mac] = {}

        for seen_dict in data:
            assert isinstance(seen_dict, dict)
            for bssid, ssid in seen_dict.items():
                ap = {'macAddress': bssid,
                      'signalStrength': -10,
                      'signalToNoiseRatio': 0
                     }
                request = {'considerIp': 'false', 'wifiAccessPoints': [ap]}
                response = post(self.url, json = request, params = self.parameters)

                if response.status_code == 200:
                    location = response.json()['location']
                elif response.status_code == 404:
                    location = {'lat': 'not known', 'lng': 'not known'}
                elif response.status_code == 403:
                    location = {'lat': 'daily limit or', 'lng': 'user rate limit exceeded'}
                elif response.status_code == 400:
                    location = {'lat': 'key invalid or', 'lng': 'parse error'}
                else:
                    raise Exception('Something went wrong. Statuscode: {code}, dump: {dump}'.format(code = response.status_code, dump = response.json()))

                bssid_location = [bssid, ssid, location]
                self.locations[mac] = bssid_location

        return mac, self.locations[mac]
