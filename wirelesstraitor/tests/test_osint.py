from unittest import TestCase
from unittest import makeSuite

from wirelesstraitor.osint import LocationSearcher
from wirelesstraitor.observer import Observer

class LocationSearcherObserver(Observer):
    def __init__(self):
        super(LocationSearcherObserver, self).__init__()
        self.mac = None
        self.ssid = None
        self.device_location = None

    def update(self, *args, **kwargs):
        args = args[0]
        self.mac = args[0]
        self.bssid = args[1][0]
        self.ssid = args[1][1]
        self.device_location = args[1][2]

class LocationSearcherTestCase(TestCase):
    """Sending requests to API"""

    def setUp(self):
        """Set up the test with specific BSSID for the request"""
        self.searcher = LocationSearcher()
        self.observer = LocationSearcherObserver()
        self.searcher.observable.register(self.observer)

        self.mac = 'AA:BB:CC:DD:EE:FF'
        self.raw_ssid = 'VPN/WEB'
        self.bssid = 'C2:9F:DB:1B:07:E8'

        self.devices = self.mac, [{self.bssid: self.raw_ssid}]

    def tearDown(self):
        self.devices = None

    def test_get_location(self):
        mac, device_location = self.searcher.get_location(self.devices)
        ssid = device_location[1]
        location = device_location[2]
        assert mac == self.mac
        assert ssid == self.raw_ssid
        assert isinstance(location, dict)
        assert 'lat' in location.keys()
        assert 'lng' in location.keys()

    def test_update(self):
        self.searcher.update(self.devices)
        assert self.observer.mac is not None
        assert self.observer.ssid is not None
        assert self.observer.device_location is not None
        mac = self.observer.mac
        ssid = self.observer.ssid
        device_location = self.observer.device_location
        assert mac == self.mac
        assert ssid == self.raw_ssid
        assert isinstance(device_location, dict)
        assert 'lat' in device_location.keys()
        assert 'lng' in device_location.keys()

osintsuite = makeSuite(LocationSearcherTestCase, 'test')
