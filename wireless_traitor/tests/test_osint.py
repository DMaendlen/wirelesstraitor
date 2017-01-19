#!/usr/bin/python3

from unittest import TestCase
from unittest import makeSuite

from wireless_traitor.osint import LocationSearcher

class LocationSearcherTestCase(TestCase):
    """Test case to test LocationSearcher by sending defined requests to the API"""

    def setUp(self):
        """Set up the test with specific BSSID for the request"""
        self.searcher = LocationSearcher()
        self.src = 'AA:BB:CC:DD:EE:FF'
        self.ssid = 'VPN/WEB'
        self.bssid = 'C2:9F:DB:1B:07:E8'

        self.devices = {self.src: {'bssids': set(self.bssid), 'ssids': set(self.ssid)}}

    def tearDown(self):
        self.devices = None

    def testGetLocationLat(self):
        self.searcher.get_location(self.devices)
        assert self.searcher.locations[self.src]['location']['lat'] == 50.110922099999996

    def testGetLocationLng(self):
        self.searcher.get_location(self.devices)
        assert self.searcher.locations[self.src]['location']['lng'] == 8.6821267

osintsuite = makeSuite(LocationSearcherTestCase, 'test')

#class OsintTestSuite(unittest.TestSuite):
#
#    """Testsuite to make sure osint works"""
#
#    def __init__(self):
#        unittest.TestSuite.__init__(self,map(LocationSearcherTestCase,
#                                            ("testFindLocationLat",
#                                            "testFindLocationLng")))
