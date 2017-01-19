#!/usr/bin/python3

from scapy.all import Packet
from scapy.all import Dot11ProbeReq
from scapy.all import sniff

from multiprocessing import Process

class DeviceBssidMatcher(Process):
    """Finds probe requests, matches device (addr1) and BSSID (addr3)"""

    def __init__(self):
        """Sets up an empty dictionary that will be filled with
            mac as key and a dictionary as value,
            'bssids' as first key of the sub-dictionary, correspondingly a set of bssids as value
            'ssids' as second key of the sub-dictionary, correspondingly a set of ssids as value
            """

        super(DeviceBssidMatcher, self).__init__()

        self.devices = {}

    def run(self):
        sniff(iface='mon0', prn = self.find_probe_request)

    def find_probe_request(self, pkt):
        """Looks for probe request in captured packets, adds macs, ssids and bssids to the 'devices' dict"""

        if pkt.haslayer(Dot11ProbeReq):
            mac = pkt.addr2

            if mac not in self.devices.keys():
                self.devices[mac] = {'bssids': set(),
                                     'ssids': set()}
                assert mac in self.devices.keys(), "{mac} is not in {devices}".format(mac = mac, devices = self.devices)

            if pkt.addr3 != '' and pkt.addr3 != "FF:FF:FF:FF:FF:FF":
                # empty and broadcast bssids are useless
                self.devices[mac]['bssids'].add(pkt.addr3)
                assert pkt.addr3 in self.devices[mac]['bssids'], "{bssid} could not be added to {device}".format(bssid = pkt.addr3, device = self.devices[mac])
            self.devices[mac]['ssids'].add(pkt.info)
            assert pkt.info in self.devices[mac]['ssids'], "{ssid} could not be added to {device}".format(ssid = pkt.info, device = self.devices[mac])
