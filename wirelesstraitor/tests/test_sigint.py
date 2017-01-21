from unittest import TestCase
from unittest import makeSuite

from scapy.all import Dot11
from scapy.all import Dot11Elt
from scapy.all import Dot11ProbeReq

from wirelesstraitor.sigint import ProbeRequestFinder, ProbeRequestParser
from wirelesstraitor.observer import Observer

class ProbeRequestFinderObserver(Observer):
    def __init__(self):
        super(ProbeRequestFinderObserver, self).__init__()
        self.packet = None

    def update(self, *args, **kwargs):
        self.packet = args[0]

class ProbeRequestParserObserver(Observer):
    def __init__(self):
        super(ProbeRequestParserObserver, self).__init__()
        self.mac = None
        self.device_data = None

    def update(self, *args, **kwargs):
        self.mac = args[0][0]
        self.device_data = args[0][1]

class ProbeRequestFinderTestCase(TestCase):
    """Tests finding Dot11ProbeReqs and notifying observers"""

    def setUp(self):
        self.finder = ProbeRequestFinder()
        self.observer = ProbeRequestFinderObserver()
        self.finder.observable.register(self.observer)

        self.src = 'AA:BB:CC:DD:EE:FF'
        self.dest = '00:00:00:00:00:00'
        self.ssid_raw = 'testssid'
        self.ssid = Dot11Elt(ID = 'SSID', info = self.ssid_raw)
        self.bssid = '00:11:22:33:44:55'

        self.proberequest = Dot11(addr1 = self.dest, addr2 = self.src, addr3= self.bssid)
        self.proberequest.add_payload(self.ssid)
        self.proberequest.decode_payload_as(Dot11ProbeReq)

    def tearDown(self):
        self.packet = None

    def test_find_probe_request(self):
        """Test the notifying-mechanism of ProbeRequestFinder by creating a
            Dot11ProbeReq-Packet and 'finding' it.
        """
        assert self.proberequest is not None
        assert self.proberequest.haslayer(Dot11ProbeReq)
        self.finder.find_probe_request(self.proberequest)
        assert self.observer.packet.haslayer(Dot11ProbeReq)

class ProbeRequestParserTestCase(TestCase):
    """Tests parsing of Dot11ProbeReqs"""

    def setUp(self):
        self.parser = ProbeRequestParser()
        self.observer = ProbeRequestParserObserver()
        self.parser.observable.register(self.observer)

        self.mac = 'AA:BB:CC:DD:EE:FF'
        self.dst = '00:00:00:00:00:00'
        self.ssid_raw = 'testssid'
        self.ssid = Dot11Elt(ID = 'SSID', info = self.ssid_raw)
        self.bssid = '00:11:22:33:44:55'

        self.proberequest = Dot11(addr1 = self.dst, addr2 = self.mac, addr3= self.bssid)
        self.proberequest.add_payload(self.ssid)
        self.proberequest.decode_payload_as(Dot11ProbeReq)

    def test_parse_probe_request(self):
        mac, device_data = self.parser.parse_probe_request(self.proberequest)
        assert mac is not None
        assert device_data is not None
        assert self.bssid in device_data[0]
        assert device_data[0][self.bssid] == self.ssid_raw

    def test_update(self):
        self.parser.update(self.proberequest)
        assert self.observer.mac is not None
        assert self.observer.device_data is not None

        mac = self.observer.mac
        device_data = self.observer.device_data
        assert self.bssid in device_data[0]
        ssid = device_data[0][self.bssid]

        assert mac == self.mac
        assert ssid == self.ssid_raw

sigintsuite = makeSuite(ProbeRequestFinderTestCase, 'test')
sigintsuite.addTest(makeSuite(ProbeRequestParserTestCase, 'test'))
