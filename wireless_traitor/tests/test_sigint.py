#!/usr/bin/python3

from unittest import TestCase
from unittest import makeSuite
from scapy.all import Packet
from wireless_traitor.sigint import DeviceBssidMatcher

class DeviceBssidMatcherTestCase(TestCase):

    def setUp(self):
        """Create an instance of DeviceBssidMatcher and a probe request package containing an obvious BSSID, SSID and MAC-Addr"""
        self.matcher = DeviceBssidMatcher()
        # create a probe request packet with known, working bssid
        self.src = 'AA:BB:CC:DD:EE:FF'
        self.dest = '00:00:00:00:00:00'
        self.ssid = 'testssid'
        self.bssid = '00:11:22:33:44:55'
        self.proberequest = Packet(addr1 = self.dest, addr2 = self.src, addr3 = self.bssid, info = self.ssid)

    def tearDown(self):
        self.matcher = None
        self.packet = None

    def testFindProbeRequestBssid(self):
        self.matcher.find_probe_request(self.proberequest)
        assert self.bssid in matcher.devices[self.src]['bssids'], "{bssid} not in devices".format(bssid = self.bssid)

    def testFindProbeRequestSsid(self):
        self.matcher.find_probe_request(self.proberequest)
        assert self.ssid in matcher.devices[self.src]['ssids'], "{ssid} not in devices".format(ssid = self.ssid)

    def testFindProbeRequestRandom(self):
        self.matcher.find_probe_request(self.proberequest)
        assert 'random' not in matcher.devices[self.src]['bssids'], "random in devices"

sigintsuite = makeSuite(DeviceBssidMatcherTestCase, 'test')

#class SigintTestSuite(unittest.TestSuite):
#    """Testsuite to make sure sigint works"""
#
#    def __init__(self):
#        unittest.TestSuite.__init__(self,map(DeviceBssidMatcherTestCase,
#                                            ("testFindProbeRequestBssid",
#                                            "testFindProbeRequestSsid",
#                                            "testFindProbeRequestRandom")))
