from wirelesstraitor.observer import Observer

class CommandLineLocationDisplay(Observer):

    def __init__(self):
        super(CommandLineLocationDisplay, self).__init__()

    def update(self, *args, **kwargs):
        """Continuously print new mac-location pairs"""

        argtuple = args[0]
        mac = argtuple[0]
        bssid = argtuple[1][0]
        ssid = argtuple[1][1]
        location = argtuple[1][2]
        lat = location['lat']
        lng = location['lng']

        self.display_location(mac = mac, bssid = bssid, ssid = ssid, lat = lat, lng = lng)

    def display_location(self, mac, bssid, ssid, lat, lng):
        """Take json-formatted location and print it together with mac"""

        print("Device {mac} has seen {ssid} ({bssid}) at location {lat}, {lng}".format(
                    mac = mac,
                    ssid = ssid,
                    bssid = bssid,
                    lat = lat,
                    lng = lng))
