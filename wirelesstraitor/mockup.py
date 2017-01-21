from scapy.all import Dot11, Dot11Elt, Dot11ProbeReq

class PacketMockup(object):
    """Mock Dot11ProbeReq packets"""

    def __init__(self):
        super(PacketMockup, self).__init__()

    def create_packet(self, dst = '', src = '', bssid = '', ssid = ''):
        pkt = Dot11(addr1 = dst, addr2 = src, addr3 = bssid)
        ssid = Dot11Elt(ID = 'SSID', info = ssid)
        pkt.add_payload(ssid)
        pkt.decode_payload_as(Dot11ProbeReq)

        return pkt

    def mockHse(self):
        """Creates a Dot11ProbeReq for HS Esslingen WLAN 'VPN/WEB' with random src and dst"""

        dst = '32:d5:a8:5d:a7:53'
        src = '05:ad:ae:ee:ab:39'
        bssid = '18:8B:9D:D3:6A:AE'
        ssid = 'VPN/WEB'

        return self.create_packet(dst = dst, src = src, bssid = bssid, ssid = ssid)
