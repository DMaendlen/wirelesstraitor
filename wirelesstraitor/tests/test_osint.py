#!/usr/bin/python3

from unittest import TestCase
from unittest import makeSuite

from wirelesstraitor.osint import LocationSearcher
from wirelesstraitor.observer import Observer

class LocationSearcherObserver(Observer):
    def __init__(self):
        super(LocationSearcherObserver, self).__init__()
        self.mac = None
        self.locations = None

    def update(self, *args, **kwargs):
        self.mac = args[0][0]
        self.locations = args[0][1]

class LocationSearcherTestCase(TestCase):
    """Sending requests to API"""

    def setUp(self):
        """Set up the test with specific BSSID for the request"""
        self.searcher = LocationSearcher()
        self.observer = LocationSearcherObserver()
        self.searcher.observable.register(self.observer)

        self.mac = 'AA:BB:CC:DD:EE:FF'
        self.ssid = 'VPN/WEB'
        self.bssid = 'C2:9F:DB:1B:07:E8'

        self.devices = self.mac, {'bssids': set(self.bssid), 'ssids': set(self.ssid)}

    def tearDown(self):
        self.devices = None

    def test_get_location(self):
        mac, locations = self.searcher.get_locations(self.devices)
        location = locations[1]
        assert mac == self.mac
        assert location['lat'] == 50.110922099999996
        assert location['lng'] == 8.6821267

    def test_update(self):
        self.searcher.update(self.devices)
        assert self.observer.mac is not None
        assert self.observer.locations is not None
        mac = self.observer.mac
        locations = self.observer.locations
        assert mac == self.mac
        assert locations[1]['lat'] == 50.110922099999996
        assert locations[1]['lng'] == 8.6821267

osintsuite = makeSuite(LocationSearcherTestCase, 'test')
