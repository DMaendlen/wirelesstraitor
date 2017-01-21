from multiprocessing import Process

from wirelesstraitor.observable import Observable
from wirelesstraitor.observer import Observer

from scapy.all import Dot11ProbeReq
from scapy.all import Packet
from scapy.all import sniff

class ProbeRequestFinder(Process):
    """Finds Dot11ProbeReq-objects"""

    def __init__(self):
        super(ProbeRequestFinder, self).__init__()
        self.observable = Observable()

    def __getattr__(self, attr):
        return getattr(self.observable, attr)

    def run(self):
        sniff(iface='mon0', prn = self.find_probe_request)

    def find_probe_request(self, pkt):
        """Find out if pkt is a Dot11ProbeReq and notify observers
        """

        if pkt.haslayer(Dot11ProbeReq):
            self.observable.update_observers(pkt)

class ProbeRequestParser(Observer):
    """Takes Dot11ProbeReq-objects, parses them into usable format and stores
        the info for later use
    """

    def __init__(self):
        super(ProbeRequestParser, self).__init__()
        self.device_data = {}
        self.observable = Observable()

    def __getattr__(self, attr):
        return getattr(self.observable, attr)

    def update(self, *args, **kwargs):
        """If something happened in ProberEquestFinder and we get a packet,
            parse Dot11ProbeReq and throw mac, data-dict to Observers
        """

        self.observable.update_observers(self.parse_probe_request(pkt = args[0]))

    def parse_probe_request(self, pkt):
        """Takes a Dot11ProbeReq packet, parses it and returns a (mac,
            device_data[mac]) tuple
        """

        assert pkt.addr2 is not None
        mac = pkt.addr2

        if mac not in self.device_data.keys():
            self.device_data[mac] = {'bssids': set(),
                                'ssids': set()}

        assert pkt.addr3 is not None
        if pkt.addr3 != '' and pkt.addr3.upper() != "FF:FF:FF:FF:FF:FF":
            self.device_data[mac]['bssids'].add(pkt.addr3)

        assert pkt.info is not None, "SSID is None, packet was broken. See packet {pkt}".format(pkt = str(pkt))
        self.device_data[mac]['ssids'].add(pkt.info.decode('utf-8'))

        return mac, self.device_data[mac]
