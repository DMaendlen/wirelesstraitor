from wirelesstraitor.observer import Observer

class CommandLineLocationDisplay(Observer):

    def __init__(self):
        super(CommandLineLocationDisplay, self).__init__()

    def update(self, *args, **kwargs):
        """Continuously print new mac-location pairs"""

        argtuple = args[0]
        mac = argtuple[0]
        bssid = argtuple[1][0]
        location = argtuple[1][1]
        lat = location['lat']
        lng = location['lng']

        self.display_location(mac = mac, bssid = bssid, lat = lat, lng = lng)

    def display_location(self, mac, bssid, lat, lng):
        """Take json-formatted location and print it together with mac"""

        print("Device {mac} has seen {bssid} at location {lat}, {lng}".format(
                    mac = mac,
                    bssid = bssid,
                    lat = lat,
                    lng = lng))
